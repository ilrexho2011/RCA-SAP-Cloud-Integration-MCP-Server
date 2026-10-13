from __future__ import annotations

import json
import re
import textwrap
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from app.config import Settings
from app.services.iflow_parser import IFlowParser
from app.services.interface_catalog_formatter import InterfaceCatalogFormatter
from app.services.sap_client import SAPClient
from app.services.mpl_semantic_coverage_service import MPLSemanticCoverageService
from app.services.scoring_service import ScoringService


@dataclass
class ScenarioFamily:
    code: str
    title: str
    taxonomy: str
    symptom: str
    priority: str
    root_causes: list[str]
    diagnosis: list[str]
    resolution: list[str]
    validation: list[str]
    workaround: str
    monitoring_hint: str
    component: str
    protocol_family: str
    affected_interfaces: set[str] = field(default_factory=set)
    package_names: set[str] = field(default_factory=set)
    flow_names: set[str] = field(default_factory=set)
    runtime_evidence: list[str] = field(default_factory=list)
    example_error_messages: list[str] = field(default_factory=list)
    occurrence_count: int = 0
    last_seen: str | None = None
    document_id: str | None = None
    source_catalog_ids: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)


class KnowledgeGenerationService:
    def __init__(
        self,
        settings: Settings,
        sap_client: SAPClient,
        iflow_parser: IFlowParser,
        scoring_service: ScoringService,
        mpl_semantic_service: MPLSemanticCoverageService,
    ) -> None:
        self.settings = settings
        self.sap_client = sap_client
        self.iflow_parser = iflow_parser
        self.scoring_service = scoring_service
        self.mpl_semantic_service = mpl_semantic_service
        self.interface_catalog_formatter = InterfaceCatalogFormatter()
        self.base_output_dir = Path(settings.knowledge_output_dir)
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        self.examples_dir = Path(settings.knowledge_examples_dir)
        self.staging_dir = Path(settings.knowledge_staging_dir)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self._package_name_cache: dict[str, str] | None = None
        self._inventory_cache: dict[str, Any] | None = None

    async def generate_interface_catalogs(
        self,
        version: str,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
    ) -> dict[str, Any]:
        """Generate one interface catalog markdown file per iFlow."""
        version = self._normalize_version(version)
        target_dir = self._resolve_output_dir(output_dir, "interface_catalogs", version)
        target_dir.mkdir(parents=True, exist_ok=True)

        iflows = await self._collect_iflows(package_id=package_id, iflow_ids=iflow_ids)
        generated_files: list[str] = []

        for item in iflows:
            iflow_id = str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW")
            artifact = await self.sap_client.get_iflow_content(
                iflow_id=iflow_id,
                package_id=package_id or str(item.get("PackageId") or item.get("Package") or "") or None,
                lookup_item=item,
            )
            analysis = self.iflow_parser.parse(artifact)
            quality = self.scoring_service.score_iflow(iflow_id=iflow_id, analysis=analysis)

            priority = self._priority_from_score(int(quality.get("score", 70)))
            package_name = self._resolve_package_name(item)
            title = str(item.get("Name") or iflow_id)
            object_name = self._normalize_object_name(iflow_id)
            filename = f"DOC_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{object_name}_{version}.md"
            doc_id = f"CAT-{self.settings.default_sap_sid}-{object_name}"

            key_terms = self._dedupe_preserve(
                [
                    title,
                    object_name,
                    package_name,
                    str(item.get("PackageId") or ""),
                    *analysis.get("protocols", []),
                    *analysis.get("sender_systems", []),
                    *analysis.get("receiver_systems", []),
                    *analysis.get("dependencies", []),
                ]
            )

            raw_content = textwrap.dedent(
                f"""\
                # {title}

                environment: \"{self.settings.default_environment}\"
                customer_id: \"{self.settings.default_customer_id}\"
                system_id: \"{self.settings.default_system_id}\"
                sap_sid: \"{self.settings.default_sap_sid}\"
                artifact_type: \"documentation\"
                object_name: \"{object_name}\"
                priority: \"{priority}\"
                interface_id: \"{iflow_id}\"
                integration_flow_id: \"{iflow_id}\"
                integration_flow_name: \"{title}\"
                package_name: \"{package_name}\"
                review_cycle: \"{self.settings.default_review_cycle}\"

                DOC ID
                {doc_id}

                DOC TITLE
                {title}

                1. PURPOSE
                - Atomic integration catalog reference for interface {title}.
                - Artifact kind: integration_flow.
                                2. SCOPE
                - Package: {package_name}
                - Package ID: {item.get('PackageId') or 'unknown'}
                - Design-time present: True
                - Runtime present: {bool(item.get('Deployed', True))}
                - Evidence coverage level: {quality.get('evidence_coverage', 'medium')}
                - Operational class: integration

                3. KEY TERMS
                {self._bullet_block(key_terms)}

                4. CORE EXPLANATION
                - Runtime binding: {title}
                - Participants: {', '.join(self._dedupe_preserve([*analysis.get('sender_systems', []), *analysis.get('receiver_systems', [])])) or 'Not fully exposed by tenant metadata'}
                - Activities: {self._shorten(analysis.get('summary', 'No summary available'), 250)}
                - Resources: {', '.join(analysis.get('dependencies', [])[:8]) or 'No additional resources detected'}
                - Deployed versions: {item.get('Version') or artifact.get('metadata', {}).get('ResolvedVersion') or 'unknown'}

                5. OPERATIONAL RELEVANCE
                - Runtime observation level: {'observed_started' if item.get('Deployed', True) else 'design_only'}
                - Failed messages observed: unknown
                - Deployment state: {'STARTED' if item.get('Deployed', True) else 'NOT_DEPLOYED'}
                - Credential aliases: {', '.join(analysis.get('authentication', [])) or 'Unknown'}
                - Quality score: {quality.get('score', 'n/a')}/{quality.get('max_score', 100)}

                6. RELATED ARTIFACTS
                - Catalog object ID: {doc_id}
                - Sibling interfaces: {self._guess_sibling_interfaces(iflows, iflow_id)}
                - Recommended KEDB family seeds: {self._recommended_kedb_seeds(analysis)}
                """
            ).strip() + "\n"
            content = self.interface_catalog_formatter.format_document(raw_content)

            out_path = target_dir / filename
            out_path.write_text(content, encoding="utf-8")
            generated_files.append(str(out_path))

        archive_path = self._zip_directory(target_dir)
        return {
            "artifact_type": "interface_catalog",
            "version": version,
            "count": len(generated_files),
            "output_dir": str(target_dir),
            "archive_path": str(archive_path),
            "files": generated_files,
        }

    async def generate_kedb_documents(
        self,
        version: str,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
        use_mpl: bool = True,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
    ) -> dict[str, Any]:
        version = self._normalize_version(version)
        target_dir = self._resolve_output_dir(output_dir, "kedb", version)
        target_dir.mkdir(parents=True, exist_ok=True)

        scenarios = await self._derive_scenarios(
            package_id=package_id,
            iflow_ids=iflow_ids,
            use_mpl=use_mpl,
            mpl_hours=mpl_hours,
            mpl_limit=mpl_limit,
        )
        files: list[str] = []
        for scenario in scenarios.values():
            filename = f"KB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{scenario.code}_{scenario.priority}_{version}.md"
            content = self._render_kedb(scenario=scenario, version=version)
            out_path = target_dir / filename
            out_path.write_text(content, encoding="utf-8")
            files.append(str(out_path))

        archive_path = self._zip_directory(target_dir)
        return {
            "artifact_type": "kedb",
            "version": version,
            "count": len(files),
            "output_dir": str(target_dir),
            "archive_path": str(archive_path),
            "files": files,
        }

    async def generate_runbook_documents(
        self,
        version: str,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
        use_mpl: bool = True,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
    ) -> dict[str, Any]:
        version = self._normalize_version(version)
        target_dir = self._resolve_output_dir(output_dir, "runbooks", version)
        target_dir.mkdir(parents=True, exist_ok=True)

        scenarios = await self._derive_scenarios(
            package_id=package_id,
            iflow_ids=iflow_ids,
            use_mpl=use_mpl,
            mpl_hours=mpl_hours,
            mpl_limit=mpl_limit,
        )
        files: list[str] = []
        for scenario in scenarios.values():
            filename = f"RB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{scenario.code}_{scenario.priority}_{version}.md"
            content = self._render_runbook(scenario=scenario, version=version)
            out_path = target_dir / filename
            out_path.write_text(content, encoding="utf-8")
            files.append(str(out_path))

        archive_path = self._zip_directory(target_dir)
        return {
            "artifact_type": "runbook",
            "version": version,
            "count": len(files),
            "output_dir": str(target_dir),
            "archive_path": str(archive_path),
            "files": files,
        }

    def update_kedb_documents(
        self,
        version: str,
        source_dir: str | None = None,
        source_zip_path: str | None = None,
        output_dir: str | None = None,
    ) -> dict[str, Any]:
        version = self._normalize_version(version)
        source_path = self._resolve_markdown_source(
            artifact_type="kedb",
            source_dir=source_dir,
            source_zip_path=source_zip_path,
        )
        target_dir = self._resolve_output_dir(output_dir, "kedb_updated", version)
        target_dir.mkdir(parents=True, exist_ok=True)

        files: list[str] = []
        for path in sorted(source_path.glob("*.md")):
            parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
            metadata = self._normalize_metadata(parsed["metadata"], artifact_type="kedb")
            metadata["artifact_type"] = "kedb"
            metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
            metadata["object_name"] = metadata.get("object_name") or self._object_from_filename(path.name)
            metadata["review_cycle"] = metadata.get("review_cycle") or self.settings.default_review_cycle
            metadata["package_name"] = metadata.get("package_name") or "Multiple packages"
            title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
            metadata["document_id"] = parsed.get("document_id") or f"KEDB-{metadata['priority']}-{metadata['object_name']}"

            sections = parsed["sections"]
            ordered = {
                "SYMPTOM": sections.get("1. SYMPTOM") or sections.get("SYMPTOM") or ["- Symptom requires expert refinement."],
                "ERROR PATTERN": [self._normalize_taxonomy_line(x) for x in (sections.get("2. ERROR PATTERN") or sections.get("ERROR PATTERN") or [f"- {self._taxonomy_from_object_name(metadata['object_name'])}"])],
                "ROOT CAUSE": sections.get("3. ROOT CAUSE") or sections.get("ROOT CAUSE") or ["- Root cause needs confirmation from runtime evidence."],
                "DIAGNOSIS SIGNALS": sections.get("4. DIAGNOSIS SIGNALS") or sections.get("DIAGNOSIS SIGNALS") or ["- Check MPL and compare failing step against last successful message."],
                "RESOLUTION": sections.get("5. RESOLUTION") or sections.get("RESOLUTION") or ["- Apply the least risky corrective change and redeploy."],
                "VALIDATION": sections.get("6. VALIDATION") or sections.get("VALIDATION") or ["- Confirm the message completes successfully after the change."],
                "WORKAROUND": sections.get("7. WORKAROUND") or sections.get("WORKAROUND") or ["- Escalate if no safe workaround is available."],
                "RELATED ARTIFACTS": sections.get("8. RELATED ARTIFACTS") or sections.get("RELATED ARTIFACTS") or [f"- Primary runbook: RB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{metadata['object_name']}_{metadata['priority']}_{version}.md"],
            }

            ordered = self._refine_sections_with_policy(artifact_type="kedb", title=title, metadata=metadata, sections=ordered)
            filename = f"KB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{metadata['object_name']}_{metadata['priority']}_{version}.md"
            out_path = target_dir / filename
            out_path.write_text(self._render_kedb_from_sections(title, metadata, ordered), encoding="utf-8")
            files.append(str(out_path))

        archive_path = self._zip_directory(target_dir)
        return {
            "artifact_type": "kedb_update",
            "version": version,
            "source_dir": str(source_path),
            "count": len(files),
            "output_dir": str(target_dir),
            "archive_path": str(archive_path),
            "files": files,
        }

    def update_runbook_documents(
        self,
        version: str,
        source_dir: str | None = None,
        source_zip_path: str | None = None,
        output_dir: str | None = None,
    ) -> dict[str, Any]:
        version = self._normalize_version(version)
        source_path = self._resolve_markdown_source(
            artifact_type="runbooks",
            source_dir=source_dir,
            source_zip_path=source_zip_path,
        )
        target_dir = self._resolve_output_dir(output_dir, "runbooks_updated", version)
        target_dir.mkdir(parents=True, exist_ok=True)

        files: list[str] = []
        for path in sorted(source_path.glob("*.md")):
            parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
            metadata = self._normalize_metadata(parsed["metadata"], artifact_type="runbook")
            metadata["artifact_type"] = "runbook"
            metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
            metadata["object_name"] = metadata.get("object_name") or self._object_from_filename(path.name)
            metadata["review_cycle"] = metadata.get("review_cycle") or self.settings.default_review_cycle
            metadata["package_name"] = metadata.get("package_name") or "Multiple packages"
            title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
            metadata["document_id"] = parsed.get("document_id") or f"RB-{metadata['priority']}-{metadata['object_name']}"
            sections = parsed["sections"]
            ordered = {
                "PURPOSE": sections.get("1. PURPOSE") or sections.get("PURPOSE") or [f"This runbook supports the canonical incident pattern {metadata['object_name']}."],
                "BUSINESS CONTEXT": sections.get("2. BUSINESS CONTEXT") or sections.get("BUSINESS CONTEXT") or ["- Business impact requires confirmation from the owning interface team."],
                "TECHNICAL LANDSCAPE": sections.get("3. TECHNICAL LANDSCAPE") or sections.get("TECHNICAL LANDSCAPE") or ["- Package: Multiple packages"],
                "MONITORING AND MPL EVIDENCE": sections.get("4. MONITORING AND MPL EVIDENCE") or sections.get("MONITORING AND MPL EVIDENCE") or ["- Review MPL entries in the affected time window and preserve MessageGuid evidence."],
                "ERROR SIGNATURE": sections.get("5. ERROR SIGNATURE") or sections.get("ERROR SIGNATURE") or [f"- Normalized object name: {metadata['object_name']}"],
                "KNOWN ROOT CAUSES": sections.get("6. KNOWN ROOT CAUSES") or sections.get("KNOWN ROOT CAUSES") or ["- Root cause requires technical verification."],
                "PREREQUISITES FOR INVESTIGATION": sections.get("7. PREREQUISITES FOR INVESTIGATION") or sections.get("PREREQUISITES FOR INVESTIGATION") or ["- Access to CPI Monitor, Security Material, and deployment history."],
                "DIAGNOSIS STEPS": sections.get("8. DIAGNOSIS STEPS") or sections.get("DIAGNOSIS STEPS") or sections.get("DIAGNOSIS PROCEDURE") or ["- Check MPL and compare the failure with the last successful message."],
                "RECOVERY STEPS": sections.get("9. RECOVERY STEPS") or sections.get("RECOVERY STEPS") or sections.get("RECOVERY / FIX ACTIONS") or ["- Apply the least risky corrective change, redeploy, and replay one controlled message."],
                "ESCALATION CRITERIA": sections.get("10. ESCALATION CRITERIA") or sections.get("ESCALATION CRITERIA") or sections.get("ESCALATION") or ["- Escalate when the issue is reproducible and cannot be stabilized with standard operational handling."],
                "POST-FIX VALIDATION": sections.get("11. POST-FIX VALIDATION") or sections.get("POST-FIX VALIDATION") or sections.get("VALIDATION AFTER FIX") or ["- Confirm that the same error signature does not reappear after controlled replay."],
            }
            ordered = self._refine_sections_with_policy(artifact_type="runbook", title=title, metadata=metadata, sections=ordered)
            filename = f"RB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{metadata['object_name']}_{metadata['priority']}_{version}.md"
            out_path = target_dir / filename
            out_path.write_text(self._render_runbook_from_sections(title, metadata, ordered), encoding="utf-8")
            files.append(str(out_path))

        archive_path = self._zip_directory(target_dir)
        return {
            "artifact_type": "runbook_update",
            "version": version,
            "source_dir": str(source_path),
            "count": len(files),
            "output_dir": str(target_dir),
            "archive_path": str(archive_path),
            "files": files,
        }

    async def generate_knowledge_output_bundle(
        self,
        version: str,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        kedb_zip_path: str | None = None,
        runbook_zip_path: str | None = None,
        output_dir: str | None = None,
        use_mpl: bool = True,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
        include_interface_catalogs: bool = True,
        include_new_kedb: bool = True,
        include_new_runbooks: bool = True,
        include_updated_kedb: bool = True,
        include_updated_runbooks: bool = True,
    ) -> dict[str, Any]:
        version = self._normalize_version(version)
        bundle_dir = self._resolve_output_dir(output_dir, "knowledge_output", version)
        bundle_dir.mkdir(parents=True, exist_ok=True)

        manifest: dict[str, Any] = {
            "bundle_name": f"knowledge_output_{version}",
            "generated_at": self._now_iso(),
            "version": version,
            "features": {
                "use_mpl": use_mpl,
                "mpl_hours": mpl_hours or self.settings.mpl_default_lookback_hours,
                "mpl_limit": mpl_limit or self.settings.mpl_default_limit,
                "kedb_zip_path": kedb_zip_path,
                "runbook_zip_path": runbook_zip_path,
            },
            "artifacts": {},
        }

        if include_interface_catalogs:
            manifest["artifacts"]["interface_catalogs"] = await self.generate_interface_catalogs(
                version=version,
                package_id=package_id,
                iflow_ids=iflow_ids,
                output_dir=str(bundle_dir / "interface_catalogs"),
            )
        if include_new_kedb:
            manifest["artifacts"]["generated_kedb"] = await self.generate_kedb_documents(
                version=version,
                package_id=package_id,
                iflow_ids=iflow_ids,
                output_dir=str(bundle_dir / "kedb_generated"),
                use_mpl=use_mpl,
                mpl_hours=mpl_hours,
                mpl_limit=mpl_limit,
            )
        if include_new_runbooks:
            manifest["artifacts"]["generated_runbooks"] = await self.generate_runbook_documents(
                version=version,
                package_id=package_id,
                iflow_ids=iflow_ids,
                output_dir=str(bundle_dir / "runbooks_generated"),
                use_mpl=use_mpl,
                mpl_hours=mpl_hours,
                mpl_limit=mpl_limit,
            )
        if include_updated_kedb:
            manifest["artifacts"]["updated_kedb"] = self.update_kedb_documents(
                version=version,
                source_zip_path=kedb_zip_path,
                output_dir=str(bundle_dir / "kedb_updated"),
            )
        if include_updated_runbooks:
            manifest["artifacts"]["updated_runbooks"] = self.update_runbook_documents(
                version=version,
                source_zip_path=runbook_zip_path,
                output_dir=str(bundle_dir / "runbooks_updated"),
            )

        manifest_path = bundle_dir / "knowledge_output_manifest.json"
        import json
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        archive_path = self._zip_directory(bundle_dir)
        return {
            "artifact_type": "knowledge_output_bundle",
            "version": version,
            "output_dir": str(bundle_dir),
            "manifest_path": str(manifest_path),
            "archive_path": str(archive_path),
            "artifacts": manifest["artifacts"],
        }

    async def _collect_iflows(
        self,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        try:
            raw = await self.sap_client.list_iflows(package_id=package_id)
            items = raw.get("items", [])
        except Exception:
            items = self._get_inventory_iflows()

        if not items:
            items = self._get_inventory_iflows()

        if package_id:
            items = [x for x in items if str(x.get("PackageId") or "") == package_id]
        if iflow_ids:
            allowed = set(iflow_ids)
            items = [x for x in items if str(x.get("Id")) in allowed]

        deduped: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for item in items:
            iflow_id = str(item.get("Id") or item.get("iflow_id") or "")
            if iflow_id and iflow_id not in seen_ids:
                seen_ids.add(iflow_id)
                deduped.append(item)
        items = deduped

        package_map = await self._get_package_name_map()
        for item in items:
            pkg_id = str(item.get("PackageId") or item.get("Package") or "").strip()
            if not pkg_id:
                continue
            resolved_name = package_map.get(pkg_id) or package_map.get(pkg_id.lower()) or package_map.get(pkg_id.upper())
            current_name = str(item.get("PackageName") or item.get("PackageNameDisplay") or "").strip()
            if resolved_name and (not current_name or current_name == pkg_id):
                item["PackageName"] = resolved_name
                item.setdefault("PackageNameDisplay", resolved_name)
        return items

    async def _get_package_name_map(self) -> dict[str, str]:
        if self._package_name_cache is not None:
            return self._package_name_cache
        package_map: dict[str, str] = {}
        try:
            raw = await self.sap_client.list_packages()
            for item in raw.get("items", []):
                pkg_id = str(item.get("Id") or "").strip()
                pkg_name = str(item.get("Name") or "").strip()
                if pkg_id and pkg_name:
                    package_map[pkg_id] = pkg_name
        except Exception:
            package_map = {}
        if not package_map:
            package_map = self._get_inventory_package_map()
        self._package_name_cache = package_map
        return package_map

    def _resolve_package_name(self, item: dict[str, Any]) -> str:
        package_id = str(item.get("PackageId") or item.get("Package") or "").strip()
        candidate = str(item.get("PackageName") or item.get("PackageNameDisplay") or "").strip()
        if candidate and candidate != package_id:
            return candidate
        if self._package_name_cache and package_id:
            resolved = self._package_name_cache.get(package_id) or self._package_name_cache.get(package_id.lower()) or self._package_name_cache.get(package_id.upper())
            if resolved:
                return resolved
        if package_id:
            return package_id
        return str(item.get("Package") or "Unknown Package")

    async def _derive_scenarios(
        self,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        use_mpl: bool = True,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
    ) -> dict[str, ScenarioFamily]:
        scenarios: dict[str, ScenarioFamily] = {}
        iflows = await self._collect_iflows(package_id=package_id, iflow_ids=iflow_ids)
        iflows_by_id: dict[str, dict[str, Any]] = {
            str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW"): item for item in iflows
        }

        for item in iflows:
            iflow_id = str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW")
            artifact = await self.sap_client.get_iflow_content(
                iflow_id=iflow_id,
                package_id=package_id or str(item.get("PackageId") or item.get("Package") or "") or None,
                lookup_item=item,
            )
            analysis = self.iflow_parser.parse(artifact)
            flow_name = str(item.get("Name") or iflow_id)
            package_name = self._resolve_package_name(item)
            for scenario in self._candidate_scenarios(analysis):
                family = scenarios.setdefault(scenario.code, scenario)
                family.affected_interfaces.add(iflow_id)
                family.flow_names.add(flow_name)
                family.package_names.add(package_name)

        if use_mpl:
            signals = await self.mpl_semantic_service.collect_failure_signals(
                hours_back=mpl_hours or self.settings.mpl_default_lookback_hours,
                limit=mpl_limit or self.settings.mpl_default_limit,
            )
            summary = self.mpl_semantic_service.summarize_signals(signals)
            self._merge_mpl_summary_into_scenarios(
                scenarios=scenarios,
                mpl_summary=summary,
                iflows_by_id=iflows_by_id,
            )
        return scenarios

    def _merge_mpl_summary_into_scenarios(
        self,
        *,
        scenarios: dict[str, ScenarioFamily],
        mpl_summary: dict[str, Any],
        iflows_by_id: dict[str, dict[str, Any]],
    ) -> None:
        for code, data in mpl_summary.items():
            scenario = scenarios.get(code)
            if scenario is None:
                scenario = self._build_generic_scenario_from_mpl(code=code, data=data)
                scenarios[code] = scenario

            scenario.occurrence_count += int(data.get("count") or 0)
            scenario.last_seen = str(data.get("last_seen") or scenario.last_seen or self._now_iso())
            for error_text in data.get("example_errors", []):
                if error_text not in scenario.example_error_messages:
                    scenario.example_error_messages.append(error_text)
            for guid in data.get("example_message_guids", []):
                evidence_line = f"- MPL sample {guid}: {self._shorten(data.get('example_errors', [''])[0], 220)}"
                if evidence_line not in scenario.runtime_evidence:
                    scenario.runtime_evidence.append(evidence_line)
            for iflow_id in data.get("iflow_ids", []):
                scenario.affected_interfaces.add(iflow_id)
                item = iflows_by_id.get(iflow_id, {})
                scenario.flow_names.add(str(item.get("Name") or iflow_id))
                scenario.package_names.add(self._resolve_package_name(item))

            runtime_summary = (
                f"- Observed failed MPL messages: {data.get('count', 0)} | "
                f"Last seen: {data.get('last_seen', 'unknown')}"
            )
            if runtime_summary not in scenario.runtime_evidence:
                scenario.runtime_evidence.insert(0, runtime_summary)

    def _build_generic_scenario_from_mpl(self, code: str, data: dict[str, Any]) -> ScenarioFamily:
        taxonomy = str(data.get("taxonomy") or self._taxonomy_from_object_name(code))
        title = self._humanize_object_name(code)
        symptom = self._shorten((data.get("example_errors") or ["Runtime failure detected in MPL."])[0], 180)
        return ScenarioFamily(
            code=code,
            title=title,
            taxonomy=taxonomy,
            symptom=symptom,
            priority="P2",
            root_causes=[
                "Runtime error was observed in MPL and needs design-time plus runtime correlation.",
                "The exact failure family should be confirmed against payload, endpoint, and configuration evidence.",
            ],
            diagnosis=[
                "Check the referenced MessageGuid samples in MPL.",
                "Compare the failing execution with the last successful execution.",
                "Correlate the error text with the owning adapter, script, or mapping step.",
            ],
            resolution=[
                "Stabilize the interface with the least risky corrective action.",
                "Replay one controlled message after the root cause is confirmed.",
            ],
            validation=[
                "Confirm that the same MPL signature does not reappear after the fix.",
                "Confirm that the affected business transaction completes successfully.",
            ],
            workaround="Use controlled containment and replay while the root cause is under investigation.",
            monitoring_hint="SAP CPI MPL API",
            component="CPI Runtime",
            protocol_family="Scenario-dependent",
        )

    def _candidate_scenarios(self, analysis: dict[str, Any]) -> list[ScenarioFamily]:
        protocols = {p.upper() for p in analysis.get("protocols", [])}
        auth = {a.upper() for a in analysis.get("authentication", [])}
        dependencies = {d.upper() for d in analysis.get("dependencies", [])}
        candidates: list[ScenarioFamily] = []

        def add(code: str, title: str, taxonomy: str, symptom: str, priority: str, root_causes: list[str], diagnosis: list[str], resolution: list[str], validation: list[str], workaround: str, monitoring_hint: str, component: str, protocol_family: str) -> None:
            candidates.append(
                ScenarioFamily(
                    code=code,
                    title=title,
                    taxonomy=taxonomy,
                    symptom=symptom,
                    priority=priority,
                    root_causes=root_causes,
                    diagnosis=diagnosis,
                    resolution=resolution,
                    validation=validation,
                    workaround=workaround,
                    monitoring_hint=monitoring_hint,
                    component=component,
                    protocol_family=protocol_family,
                )
            )

        add(
            "MPL_OBSERVABILITY_ERROR_DETAILS_MISSING",
            "MPL error details are missing for failed CPI messages",
            "CPI | OBSERVABILITY | ERROR_DETAILS_MISSING | MPL",
            "Failed CPI messages do not expose sufficient error details for diagnosis.",
            "P2",
            [
                "Error details endpoint is not queried correctly.",
                "Tenant metadata-only mode hides detailed exception evidence.",
                "Logging level or trace coverage is insufficient for the failing path.",
            ],
            [
                "Check MessageGuid, CorrelationId, and failing step in MPL.",
                "Verify that ErrorInformation retrieval is enabled and accessible.",
                "Compare one failing MPL entry with one successful execution in the same time window.",
            ],
            [
                "Re-run controlled retrieval of ErrorInformation for the failing MessageGuid.",
                "Increase trace or logging only for a controlled diagnostic window.",
                "Persist the normalized error payload into the knowledge ingestion pipeline.",
            ],
            [
                "Verify that MessageGuid, error text, and failing step are now visible.",
                "Confirm that the support team can classify the incident from the captured evidence.",
            ],
            "Use metadata-based triage while detailed MPL evidence is being restored.",
            "SAP CPI MPL API",
            "MPL Observability",
            "CPI",
        )

        if {"HTTP/HTTPS", "HTTP", "HTTPS", "ODATA", "SOAP"} & protocols:
            add(
                "HTTP_AUTHENTICATION_UNAUTHORIZED_401",
                "HTTP 401 Unauthorized on outbound receiver call",
                "HTTP | AUTHENTICATION | UNAUTHORIZED | 401",
                "Receiver rejects authentication on outbound call.",
                "P1",
                [
                    "Invalid credential alias.",
                    "Expired secret or password.",
                    "Wrong token or authentication endpoint.",
                ],
                [
                    "Check receiver response body and authorization headers.",
                    "Validate credential alias, credential type, and expiry.",
                    "Confirm that the destination points to the correct authentication endpoint.",
                ],
                [
                    "Review Security Material and the configured alias.",
                    "Correct the secret, password, certificate, or token endpoint.",
                    "Redeploy and replay one controlled message.",
                ],
                [
                    "Expect HTTP 2xx from the receiver.",
                    "Confirm that the business object is posted exactly once.",
                    "Verify that no repeated 401 errors appear in MPL.",
                ],
                "Temporarily switch to a known-good credential alias if one is already approved.",
                "Receiver HTTP response evidence in MPL",
                "Receiver Authentication",
                "HTTP/REST/OData/SOAP",
            )
            add(
                "DOWNSTREAM_SERVER_INTERNAL_ERROR_500",
                "Downstream system returns HTTP 500 Internal Server Error",
                "HTTP | DOWNSTREAM | INTERNAL_SERVER_ERROR | 500",
                "Receiver endpoint responds with internal server error on outbound call.",
                "P1",
                [
                    "Receiver-side application defect.",
                    "Unexpected payload structure or field value.",
                    "Downstream dependency outage or backend exception.",
                ],
                [
                    "Check exact HTTP 500 response body and correlation identifiers.",
                    "Compare the failing payload with the last successful message.",
                    "Validate whether a recent deployment changed the outbound structure.",
                ],
                [
                    "Contain retries if they create noise or duplication risk.",
                    "Coordinate with the downstream owner using MessageGuid and payload evidence.",
                    "Replay one controlled message only after the receiver confirms readiness.",
                ],
                [
                    "Receiver returns HTTP 2xx after the fix.",
                    "No duplicate business posting is observed.",
                    "The same 500 signature does not recur in the immediate monitoring window.",
                ],
                "Queue or hold business traffic until the downstream owner confirms recovery.",
                "HTTP receiver status and correlation evidence",
                "Receiver Processing",
                "HTTP/REST/OData/SOAP",
            )
            add(
                "DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503",
                "Downstream system returns HTTP 503 Service Unavailable",
                "HTTP | AVAILABILITY | SERVICE_UNAVAILABLE | 503",
                "Receiver endpoint is temporarily unavailable.",
                "P2",
                [
                    "Downstream maintenance window or outage.",
                    "Network path instability between CPI and receiver.",
                    "Connection pool exhaustion or upstream throttling.",
                ],
                [
                    "Check the exact time window and retry behavior in MPL.",
                    "Confirm whether the endpoint was under maintenance or rate limited.",
                    "Verify if the same issue affects multiple interfaces.",
                ],
                [
                    "Avoid blind mass replay while the receiver is unavailable.",
                    "Coordinate a recovery window with the receiver owner.",
                    "Replay backlog gradually after stability is confirmed.",
                ],
                [
                    "Receiver is reachable and returns success responses.",
                    "No retry backlog remains after controlled replay.",
                    "MPL does not show repeated 503 signatures.",
                ],
                "Pause or throttle non-critical traffic until the receiver is reachable again.",
                "Receiver HTTP availability evidence in MPL",
                "Connectivity / Availability",
                "HTTP/REST/OData/SOAP",
            )

        if "MAIL" in protocols or "SMTP" in protocols:
            add(
                "MAIL_SMTP_CONFIG_OR_AUTH_FAILURE",
                "SMTP notification delivery fails due to configuration or authentication issue",
                "MAIL | SMTP | CONFIG_OR_AUTH_FAILURE | DELIVERY",
                "Mail adapter cannot deliver the notification message.",
                "P3",
                [
                    "SMTP host or port is wrong.",
                    "Credential alias is invalid or expired.",
                    "TLS or network policy blocks the outbound mail session.",
                ],
                [
                    "Check SMTP host, port, and TLS configuration.",
                    "Validate the mail credential alias and expiry.",
                    "Compare the failing notification path with a last successful execution.",
                ],
                [
                    "Correct SMTP connection parameters or credential alias.",
                    "Redeploy the integration flow if adapter configuration changed.",
                    "Replay one controlled notification message.",
                ],
                [
                    "Mail adapter sends the message successfully.",
                    "The notification reaches the agreed recipient list.",
                ],
                "Use an approved fallback notification channel during the incident.",
                "Mail adapter error text in MPL",
                "Mail Adapter",
                "MAIL/SMTP",
            )

        if "SFTP" in protocols:
            add(
                "FILE_POLLING_INTERVAL_TOO_LONG",
                "SFTP polling interval or pickup strategy causes delayed file processing",
                "FILE | POLLING | INTERVAL_TOO_LONG | LATENCY",
                "File-based integration is healthy but reacts too slowly to new files.",
                "P3",
                [
                    "Polling interval is configured too conservatively.",
                    "File pickup strategy creates avoidable delay.",
                    "Operational expectation is closer to near-real-time than batch.",
                ],
                [
                    "Check sender polling interval and file pickup configuration.",
                    "Compare file arrival time with actual processing start time.",
                    "Confirm the expected SLA for this interface.",
                ],
                [
                    "Reduce the polling interval if the business SLA requires it.",
                    "Separate high-frequency files from low-priority batch processing.",
                    "Validate that the file server can handle the revised polling profile.",
                ],
                [
                    "Processing starts within the agreed SLA window.",
                    "No backlog grows in the source directory.",
                ],
                "Run a short temporary polling interval during critical business windows.",
                "SFTP sender scheduling evidence",
                "SFTP Sender",
                "SFTP",
            )

        if any(x.endswith("XSLT") or x.endswith("GROOVY") or "MAPPING" in x for x in dependencies):
            add(
                "MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED",
                "Mapping or transformation fails due to data type conversion error",
                "MAPPING | TRANSFORMATION | TYPE_CONVERSION_FAILED | DATA",
                "Transformation step rejects a value because the expected data type is not met.",
                "P2",
                [
                    "Source payload contains an unexpected value or format.",
                    "Mapping logic assumes a type that is not guaranteed by the sender.",
                    "Groovy or XSLT transformation lacks defensive conversion logic.",
                ],
                [
                    "Check the failing field value in the source payload.",
                    "Review the affected mapping or script line for strict conversion logic.",
                    "Compare the failing payload with a previously successful example.",
                ],
                [
                    "Correct the source value or adjust the mapping logic.",
                    "Add defensive conversion, defaulting, or validation before the transformation step.",
                    "Redeploy and replay one controlled message.",
                ],
                [
                    "The transformation step completes successfully.",
                    "The expected target structure is produced without truncation or data loss.",
                ],
                "Skip or quarantine the failing payload if business rules allow controlled continuation.",
                "Transformation exception evidence in MPL",
                "Message Mapping / Script",
                "Mapping",
            )
            add(
                "MAPPING_SOURCE_MANDATORY_VALUE_MISSING",
                "Mapping fails because a mandatory source value is missing",
                "MAPPING | DATA_QUALITY | MANDATORY_VALUE_MISSING | SOURCE",
                "A mandatory source field is empty or absent at runtime.",
                "P2",
                [
                    "Sender omitted a mandatory field.",
                    "Pre-validation is missing before the mapping step.",
                    "Payload version drift changed field presence semantics.",
                ],
                [
                    "Identify the mandatory field that is missing in the source payload.",
                    "Check mapping assumptions and source schema version.",
                    "Review whether a router or validator should stop the payload earlier.",
                ],
                [
                    "Correct the sender payload or enrich the missing value before mapping.",
                    "Add validation and clear error handling for missing mandatory fields.",
                    "Replay one controlled message after the correction.",
                ],
                [
                    "Mandatory source fields are present for the replayed message.",
                    "No repeat of the same mapping failure is observed.",
                ],
                "Route the payload to an exception path with explicit business notification.",
                "Mapping failure evidence in MPL",
                "Message Mapping / Validation",
                "Mapping",
            )

        if "UNKNOWN" in auth or not auth:
            add(
                "CLOUD_AUTH_SESSION_EXPIRED",
                "Cloud authentication session or token context expires during integration processing",
                "CLOUD | AUTHENTICATION | SESSION_EXPIRED | TOKEN",
                "Authentication context is no longer valid when the outbound call is executed.",
                "P2",
                [
                    "OAuth token lifetime is shorter than expected.",
                    "Session propagation or credential refresh is missing.",
                    "Authentication hint is not consistently exposed by the tenant metadata.",
                ],
                [
                    "Check token acquisition and expiry handling.",
                    "Compare token lifetime with actual processing duration.",
                    "Validate whether the same issue appears only after long-running flows or retries.",
                ],
                [
                    "Refresh the token before the critical receiver call.",
                    "Adjust authentication handling or retry behavior.",
                    "Redeploy and replay one controlled message.",
                ],
                [
                    "Authentication succeeds without reusing an expired context.",
                    "No repeated session-expired symptom remains in MPL.",
                ],
                "Reduce processing delay before the authenticated receiver call.",
                "Authentication error text and timing evidence",
                "Authentication Handling",
                "Cloud Authentication",
            )

        unique: dict[str, ScenarioFamily] = {}
        for candidate in candidates:
            unique.setdefault(candidate.code, candidate)
        return list(unique.values())

    def _render_kedb(self, scenario: ScenarioFamily, version: str) -> str:
        object_name = f"CPI_{scenario.code}"
        metadata = {
            "environment": self.settings.default_environment,
            "customer_id": self.settings.default_customer_id,
            "system_id": self.settings.default_system_id,
            "sap_sid": self.settings.default_sap_sid,
            "artifact_type": "kedb",
            "object_name": object_name,
            "priority": scenario.priority,
            "interface_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
            "integration_flow_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
            "integration_flow_name": sorted(scenario.flow_names)[0] if scenario.flow_names else "Multiple interfaces",
            "package_name": ", ".join(sorted(scenario.package_names)) or "Multiple packages",
            "review_cycle": self.settings.default_review_cycle,
        }
        related = [
            f"Primary runbook: RB_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{object_name}_{scenario.priority}_{version}.md",
            f"Affected interfaces: {', '.join(sorted(scenario.affected_interfaces)[:10]) or 'None detected'}",
            f"Runtime occurrences observed in MPL: {scenario.occurrence_count}",
            f"Last seen in MPL: {scenario.last_seen or 'unknown'}",
            "Owner: IntegrationTeam",
        ]
        diagnosis_signals = list(scenario.diagnosis)
        diagnosis_signals.extend(self._strip_bullet_prefix(x) for x in scenario.runtime_evidence[:4])
        sections = {
            "SYMPTOM": [scenario.symptom],
            "ERROR PATTERN": [scenario.taxonomy],
            "ROOT CAUSE": scenario.root_causes,
            "DIAGNOSIS SIGNALS": diagnosis_signals,
            "RESOLUTION": scenario.resolution,
            "VALIDATION": scenario.validation,
            "WORKAROUND": [scenario.workaround],
            "RELATED ARTIFACTS": related,
        }
        sections = self._refine_sections_with_policy(artifact_type="kedb", title=scenario.title, metadata=metadata, sections=sections)
        return self._render_kedb_from_sections(scenario.title, metadata, sections)

    def _render_runbook(self, scenario: ScenarioFamily, version: str) -> str:
        object_name = f"CPI_{scenario.code}"
        metadata = {
            "environment": self.settings.default_environment,
            "customer_id": self.settings.default_customer_id,
            "system_id": self.settings.default_system_id,
            "sap_sid": self.settings.default_sap_sid,
            "artifact_type": "runbook",
            "object_name": object_name,
            "priority": scenario.priority,
            "interface_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
            "integration_flow_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
            "integration_flow_name": sorted(scenario.flow_names)[0] if scenario.flow_names else "Multiple interfaces",
            "package_name": ", ".join(sorted(scenario.package_names)) or "Multiple packages",
            "review_cycle": self.settings.default_review_cycle,
        }
        sections = {
            "PURPOSE": [
                f"Support triage, diagnosis, containment, recovery, and validation for the canonical issue **{object_name}**.",
                "Keep the procedure concise, evidence-led, and safe for controlled replay.",
            ],
            "BUSINESS CONTEXT": [
                "Business process: Scenario-dependent CPI integration processing",
                f"Description: Representative affected interfaces include {', '.join(sorted(scenario.affected_interfaces)[:5]) or 'tenant-wide interfaces'}.",
                f"Business criticality: {self._criticality_from_priority(scenario.priority)}",
                f"Impact: {scenario.symptom}",
                f"Affected interfaces count: {len(scenario.affected_interfaces)}",
            ],
            "TECHNICAL LANDSCAPE": [
                f"Package: {', '.join(sorted(scenario.package_names)) or 'Multiple packages'}",
                f"Integration flow ID: {sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE'}",
                f"Integration flow name: {sorted(scenario.flow_names)[0] if scenario.flow_names else 'Multiple interfaces'}",
                f"Processing component: {scenario.component}",
                f"Protocol family: {scenario.protocol_family}",
                f"Error pattern: {scenario.taxonomy}",
                "System type: cpi",
            ],
            "MONITORING AND MPL EVIDENCE": [
                f"Monitoring source: {scenario.monitoring_hint}",
                f"Observed failed MPL messages for this family: {scenario.occurrence_count}",
                f"Last seen in MPL: {scenario.last_seen or 'unknown'}",
                "Preserve MessageGuid, CorrelationId, Sender, Receiver, and IntegrationFlowName when available.",
                "Compare the failing execution with the last successful run in the same window.",
                *[self._strip_bullet_prefix(x) for x in scenario.runtime_evidence[:5]],
            ],
            "ERROR SIGNATURE": [
                f"Title: {scenario.title}",
                f"Short symptom: {scenario.symptom}",
                f"Normalized object name: {object_name}",
            ],
            "KNOWN ROOT CAUSES": scenario.root_causes,
            "PREREQUISITES FOR INVESTIGATION": [
                "Access to SAP CPI Monitor / MPL and trace where applicable.",
                f"Access to the owning package(s): {', '.join(sorted(scenario.package_names)) or 'Multiple packages'}.",
                "Deployment history, security material access, and one representative failing payload.",
            ],
            "DIAGNOSIS STEPS": scenario.diagnosis,
            "RECOVERY STEPS": [
                "Contain the incident and preserve reproducible evidence before changing configuration.",
                *scenario.resolution,
                f"Rollback option: {scenario.workaround}",
            ],
            "ESCALATION CRITERIA": [
                "Support owner: IntegrationTeam",
                "Escalation group: RCMO-CPI-L2",
                "Escalate when the issue is reproducible, business impact expands, or controlled recovery fails.",
                "Evidence required: MessageGuid, time window, failing step, error text, configuration delta, and replay outcome.",
            ],
            "POST-FIX VALIDATION": scenario.validation,
        }
        sections = self._refine_sections_with_policy(artifact_type="runbook", title=scenario.title, metadata=metadata, sections=sections)
        return self._render_runbook_from_sections(scenario.title, metadata, sections)

    def _render_kedb_from_sections(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
        return self._render_structured_markdown(
            title=title,
            metadata=metadata,
            id_label="KEDB ID",
            doc_id=metadata.get("document_id") or f"KEDB-{metadata['priority']}-{metadata['object_name']}",
            title_label="KEDB TITLE",
            title_value=title,
            section_order=[
                "1. SYMPTOM",
                "2. ERROR PATTERN",
                "3. ROOT CAUSE",
                "4. DIAGNOSIS SIGNALS",
                "5. RESOLUTION",
                "6. VALIDATION",
                "7. WORKAROUND",
                "8. RELATED ARTIFACTS",
            ],
            section_map={
                "1. SYMPTOM": sections.get("SYMPTOM", ["None"]),
                "2. ERROR PATTERN": sections.get("ERROR PATTERN", ["None"]),
                "3. ROOT CAUSE": sections.get("ROOT CAUSE", ["None"]),
                "4. DIAGNOSIS SIGNALS": sections.get("DIAGNOSIS SIGNALS", ["None"]),
                "5. RESOLUTION": sections.get("RESOLUTION", ["None"]),
                "6. VALIDATION": sections.get("VALIDATION", ["None"]),
                "7. WORKAROUND": sections.get("WORKAROUND", ["None"]),
                "8. RELATED ARTIFACTS": sections.get("RELATED ARTIFACTS", ["None"]),
            },
            bullet="-",
            escape_underscores=False,
            plain_sections={"1. PURPOSE"},
        )

    def _render_runbook_from_sections(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
        return self._render_structured_markdown(
            title=title,
            metadata=metadata,
            id_label="RUNBOOK ID",
            doc_id=metadata.get("document_id") or f"RB-{metadata['priority']}-{metadata['object_name']}",
            title_label="RUNBOOK TITLE",
            title_value=title,
            section_order=[
                "1. PURPOSE",
                "2. BUSINESS CONTEXT",
                "3. TECHNICAL LANDSCAPE",
                "4. MONITORING AND MPL EVIDENCE",
                "5. ERROR SIGNATURE",
                "6. KNOWN ROOT CAUSES",
                "7. PREREQUISITES FOR INVESTIGATION",
                "8. DIAGNOSIS STEPS",
                "9. RECOVERY STEPS",
                "10. ESCALATION CRITERIA",
                "11. POST-FIX VALIDATION",
            ],
            section_map={
                "1. PURPOSE": sections.get("PURPOSE", ["None"]),
                "2. BUSINESS CONTEXT": sections.get("BUSINESS CONTEXT", ["None"]),
                "3. TECHNICAL LANDSCAPE": sections.get("TECHNICAL LANDSCAPE", ["None"]),
                "4. MONITORING AND MPL EVIDENCE": sections.get("MONITORING AND MPL EVIDENCE", ["None"]),
                "5. ERROR SIGNATURE": sections.get("ERROR SIGNATURE", ["None"]),
                "6. KNOWN ROOT CAUSES": sections.get("KNOWN ROOT CAUSES", ["None"]),
                "7. PREREQUISITES FOR INVESTIGATION": sections.get("PREREQUISITES FOR INVESTIGATION", ["None"]),
                "8. DIAGNOSIS STEPS": sections.get("DIAGNOSIS STEPS", ["None"]),
                "9. RECOVERY STEPS": sections.get("RECOVERY STEPS", ["None"]),
                "10. ESCALATION CRITERIA": sections.get("ESCALATION CRITERIA", ["None"]),
                "11. POST-FIX VALIDATION": sections.get("POST-FIX VALIDATION", ["None"]),
            },
            bullet="-",
            escape_underscores=False,
            plain_sections={"1. PURPOSE"},
        )

    def _parse_markdown_sections(self, text: str) -> dict[str, Any]:
        lines = text.splitlines()
        title = ""
        metadata: dict[str, str] = {}
        sections: dict[str, list[str]] = {}
        document_id = ""
        title_label = ""
        current_section: str | None = None

        for idx, line in enumerate(lines):
            stripped = line.strip()
            if idx == 0 and stripped.startswith("# "):
                title = stripped[2:].strip()
                continue
            if re.match(r"^[a-z_]+:\s*\"?.+\"?$", stripped):
                key, val = stripped.split(":", 1)
                metadata[key.strip()] = val.strip().strip('"')
                continue
            if stripped in {"KEDB ID", "RUNBOOK ID", "DOC ID"}:
                title_label = stripped
                current_section = None
                continue
            if stripped in {"KEDB TITLE", "RUNBOOK TITLE", "DOC TITLE"}:
                current_section = None
                continue
            if not document_id and title_label in {"KEDB ID", "RUNBOOK ID", "DOC ID"}:
                document_id = stripped
                title_label = ""
                continue
            if re.match(r"^\d+\.\s+", stripped):
                current_section = stripped
                sections[current_section] = []
                continue
            if current_section and stripped:
                sections[current_section].append(stripped)
        return {"title": title, "metadata": metadata, "sections": sections, "document_id": document_id}

    def _normalize_metadata(self, metadata: dict[str, str], artifact_type: str) -> dict[str, str]:
        return {
            "environment": metadata.get("environment", self.settings.default_environment),
            "customer_id": metadata.get("customer_id", self.settings.default_customer_id),
            "system_id": metadata.get("system_id", self.settings.default_system_id),
            "sap_sid": metadata.get("sap_sid", self.settings.default_sap_sid),
            "artifact_type": metadata.get("artifact_type", artifact_type),
            "object_name": self._normalize_object_name(metadata.get("object_name", "UNKNOWN_OBJECT")),
            "priority": metadata.get("priority", "P3"),
            "interface_id": metadata.get("interface_id", "UNKNOWN_INTERFACE"),
            "integration_flow_id": metadata.get("integration_flow_id", metadata.get("interface_id", "UNKNOWN_INTERFACE")),
            "integration_flow_name": metadata.get("integration_flow_name", metadata.get("interface_id", "UNKNOWN_INTERFACE")),
            "package_name": metadata.get("package_name", "Multiple packages"),
            "review_cycle": metadata.get("review_cycle", self.settings.default_review_cycle),
        }

    def _priority_from_score(self, score: int) -> str:
        if score < 55:
            return "P1"
        if score < 70:
            return "P2"
        if score < 85:
            return "P3"
        return "P4"

    def _criticality_from_priority(self, priority: str) -> str:
        return {"P1": "critical", "P2": "high", "P3": "medium", "P4": "low"}.get(priority, "medium")

    def _normalize_version(self, version: str) -> str:
        version = version.strip()
        return version if version.lower().startswith("v") else f"v{version}"

    def _normalize_object_name(self, value: str) -> str:
        value = re.sub(r"[^A-Za-z0-9]+", "_", value or "UNKNOWN_OBJECT")
        value = re.sub(r"_+", "_", value).strip("_")
        return value.upper() or "UNKNOWN_OBJECT"

    def _humanize_object_name(self, value: str) -> str:
        return value.replace("_", " ").title()

    def _taxonomy_from_object_name(self, value: str) -> str:
        return " | ".join([x for x in value.split("_") if x])

    def _normalize_taxonomy_line(self, line: str) -> str:
        cleaned = line.lstrip("- ").strip()
        cleaned = re.sub(r"\s*\|\s*", " | ", cleaned)
        return f"- {cleaned}"

    def _priority_from_filename(self, filename: str) -> str:
        match = re.search(r"_(P[1-4])_", filename)
        return match.group(1) if match else "P3"

    def _object_from_filename(self, filename: str) -> str:
        stem = Path(filename).stem
        parts = stem.split("_")
        if len(parts) >= 6:
            return "_".join(parts[3:-2])
        return self._normalize_object_name(stem)

    def _recommended_kedb_seeds(self, analysis: dict[str, Any]) -> str:
        seeds = []
        protocols = [p.upper() for p in analysis.get("protocols", [])]
        if any(x in protocols for x in ["HTTP/HTTPS", "HTTP", "HTTPS", "ODATA", "SOAP"]):
            seeds.extend(["HTTP_AUTHENTICATION_UNAUTHORIZED_401", "DOWNSTREAM_SERVER_INTERNAL_ERROR_500"])
        if "SFTP" in protocols:
            seeds.append("FILE_POLLING_INTERVAL_TOO_LONG")
        if any("MAIL" in p or "SMTP" in p for p in protocols):
            seeds.append("MAIL_SMTP_CONFIG_OR_AUTH_FAILURE")
        if not seeds:
            seeds.append("MPL_OBSERVABILITY_ERROR_DETAILS_MISSING")
        return ", ".join(self._dedupe_preserve(seeds))

    def _guess_sibling_interfaces(self, iflows: list[dict[str, Any]], current_id: str) -> str:
        siblings = [str(x.get("Id")) for x in iflows if str(x.get("Id")) != current_id][:5]
        return ", ".join(siblings) or "None"

    def _render_structured_markdown(
        self,
        *,
        title: str,
        metadata: dict[str, str],
        id_label: str,
        doc_id: str,
        title_label: str,
        title_value: str,
        section_order: list[str],
        section_map: dict[str, list[str]],
        bullet: str,
        escape_underscores: bool,
        plain_sections: set[str] | None = None,
    ) -> str:
        def esc(value: str) -> str:
            value = str(value)
            return value.replace("_", r"\_") if escape_underscores else value

        parts: list[str] = [f"# {esc(title)}", ""]
        for key, value in metadata.items():
            if key == "document_id":
                continue
            parts.append(f'{esc(key)}: "{esc(value)}"')
        parts.extend(["", id_label, esc(doc_id), "", title_label, esc(title_value), ""])
        plain_sections = plain_sections or set()
        for section_name in section_order:
            parts.append(section_name)
            lines = section_map.get(section_name, []) or ["None"]
            for idx, line in enumerate(lines):
                cleaned = self._strip_bullet_prefix(line)
                if section_name in plain_sections and idx == 0:
                    parts.append(esc(cleaned))
                else:
                    parts.append(f"{bullet} {esc(cleaned)}")
            parts.append("")
        return "\n".join(parts).rstrip() + "\n"

    def _strip_bullet_prefix(self, line: str) -> str:
        stripped = str(line).strip()
        stripped = re.sub(r"^[*-]\s*", "", stripped)
        return stripped.strip()

    def _refine_sections_with_policy(self, artifact_type: str, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> dict[str, list[str]]:
        refined: dict[str, list[str]] = {}
        for sec, lines in sections.items():
            bucket: list[str] = []
            seen: set[str] = set()
            for line in lines:
                cleaned = self._normalize_action_line(line, artifact_type=artifact_type, section_name=sec)
                if not cleaned:
                    continue
                key = cleaned.lower()
                if key not in seen:
                    seen.add(key)
                    bucket.append(cleaned)
            refined[sec] = bucket or ["None"]
        ai_refined = self._maybe_refine_with_openai(artifact_type=artifact_type, title=title, metadata=metadata, sections=refined)
        return ai_refined or refined

    def _normalize_action_line(self, line: str, *, artifact_type: str, section_name: str) -> str:
        text = self._strip_bullet_prefix(line)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"^Generated by .*", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"^Generated at:.*", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"No directly matching MPL sample was found in the provided export\. ?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"The MPL ID for the failed message is\s*:\s*[A-Za-z0-9_\-]+", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"^[A-Za-z0-9_.:$]+(?:Exception|Error):\s*", "", text)
        if not text:
            return ""
        if artifact_type == "runbook" and section_name in {"DIAGNOSIS STEPS", "RECOVERY STEPS", "POST-FIX VALIDATION", "ESCALATION CRITERIA"}:
            text = text[0].upper() + text[1:]
            if not re.match(r"^(Check|Verify|Confirm|Review|Capture|Compare|Collect|Preserve|Reduce|Apply|Replay|Lower|Schedule|Escalate|Contain|Inspect|Coordinate|Use|Document|Re-run|Increase|Persist)", text):
                text = f"Check {text[0].lower() + text[1:]}" if section_name == "DIAGNOSIS STEPS" else text
        return text

    def _maybe_refine_with_openai(self, artifact_type: str, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> dict[str, list[str]] | None:
        if not self.settings.openai_api_key:
            return None
        payload = {
            "model": self.settings.openai_model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Refine SAP CPI markdown section bullets. Keep the same section keys and order. "
                                "Be concrete, concise, action-led, and fact-preserving. Do not invent metadata. "
                                "Return strict JSON: {\"sections\": {section: [bullets]}}."
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": json.dumps({"artifact_type": artifact_type, "title": title, "metadata": metadata, "sections": sections}, ensure_ascii=False),
                        }
                    ],
                },
            ],
            "text": {"format": {"type": "json_object"}},
        }
        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(
                    f"{self.settings.openai_base_url.rstrip('/')}/responses",
                    headers={
                        "Authorization": f"Bearer {self.settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
            output_text = data.get("output_text") or ""
            if not output_text:
                for item in data.get("output", []):
                    for content in item.get("content", []):
                        if content.get("type") in {"output_text", "text"} and content.get("text"):
                            output_text += content.get("text", "")
            parsed = json.loads(output_text) if output_text else {}
            result = parsed.get("sections") if isinstance(parsed, dict) else None
            if isinstance(result, dict):
                normalized: dict[str, list[str]] = {}
                alias_map: dict[str, str] = {}
                for expected_key in sections.keys():
                    alias_map[expected_key.casefold()] = expected_key
                    alias_map[re.sub(r"^\d+\.\s*", "", expected_key).casefold()] = expected_key
                for key, value in result.items():
                    mapped_key = alias_map.get(str(key).casefold()) or alias_map.get(re.sub(r"^\d+\.\s*", "", str(key)).casefold())
                    if not mapped_key:
                        continue
                    if isinstance(value, list):
                        cleaned_values = [self._strip_bullet_prefix(str(x)) for x in value if str(x).strip()]
                    elif isinstance(value, str) and value.strip():
                        cleaned_values = [self._strip_bullet_prefix(value)]
                    else:
                        cleaned_values = []
                    if cleaned_values:
                        normalized[mapped_key] = cleaned_values
                merged: dict[str, list[str]] = {}
                for expected_key, original_values in sections.items():
                    merged[expected_key] = normalized.get(expected_key) or list(original_values)
                return merged or None
        except Exception:
            return None
        return None

    def _load_inventory_cache(self) -> dict[str, Any]:
        if self._inventory_cache is not None:
            return self._inventory_cache
        cache = {"iflows": [], "packages": []}
        raw_path = (self.settings.knowledge_inventory_path or "").strip()
        if not raw_path:
            self._inventory_cache = cache
            return cache
        path = Path(raw_path)
        try:
            if path.is_file() and path.suffix.lower() == ".zip":
                with zipfile.ZipFile(path) as zf:
                    for name in zf.namelist():
                        if name.endswith("/odata/iflows.json"):
                            data = json.loads(zf.read(name).decode("utf-8"))
                            cache["iflows"].extend(self._extract_odata_results(data))
                        elif name.endswith("/odata/packages.json"):
                            data = json.loads(zf.read(name).decode("utf-8"))
                            cache["packages"].extend(self._extract_odata_results(data))
            elif path.is_dir():
                for file in path.rglob("iflows.json"):
                    cache["iflows"].extend(self._extract_odata_results(json.loads(file.read_text(encoding="utf-8"))))
                for file in path.rglob("packages.json"):
                    cache["packages"].extend(self._extract_odata_results(json.loads(file.read_text(encoding="utf-8"))))
        except Exception:
            cache = {"iflows": [], "packages": []}
        self._inventory_cache = cache
        return cache

    def _extract_odata_results(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        if isinstance(data.get("d"), dict) and isinstance(data["d"].get("results"), list):
            return [x for x in data["d"]["results"] if isinstance(x, dict)]
        if isinstance(data.get("items"), list):
            return [x for x in data["items"] if isinstance(x, dict)]
        return []

    def _get_inventory_iflows(self) -> list[dict[str, Any]]:
        return list(self._load_inventory_cache().get("iflows", []))

    def _get_inventory_package_map(self) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for item in self._load_inventory_cache().get("packages", []):
            pkg_id = str(item.get("Id") or "").strip()
            pkg_name = str(item.get("Name") or "").strip()
            if pkg_id and pkg_name:
                mapping[pkg_id] = pkg_name
        return mapping

    def _resolve_markdown_source(
        self,
        *,
        artifact_type: str,
        source_dir: str | None,
        source_zip_path: str | None,
    ) -> Path:
        if source_dir:
            return Path(source_dir)
        if source_zip_path:
            zip_path = Path(source_zip_path)
            extract_dir = self.staging_dir / artifact_type / zip_path.stem
            if extract_dir.exists():
                return extract_dir
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
            nested_dirs = [p for p in extract_dir.iterdir() if p.is_dir()]
            md_files_here = list(extract_dir.glob("*.md"))
            if not md_files_here and len(nested_dirs) == 1:
                return nested_dirs[0]
            return extract_dir
        return self.examples_dir / artifact_type

    def _resolve_output_dir(self, output_dir: str | None, family: str, version: str) -> Path:
        if output_dir:
            return Path(output_dir)
        return self.base_output_dir / family / version

    def _zip_directory(self, directory: Path) -> Path:
        archive_path = directory.with_suffix(".zip")
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(directory.rglob("*")):
                if path.is_file():
                    zf.write(path, arcname=path.relative_to(directory.parent))
        return archive_path

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _bullet_block(self, items: list[str]) -> str:
        items = [x for x in items if x]
        return "\n".join(f"- {x}" for x in items) if items else "- None"

    def _block(self, lines: list[str]) -> str:
        normalized = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            normalized.append(stripped if stripped.startswith("-") else f"- {stripped}")
        return "\n".join(normalized) if normalized else "- None"

    def _shorten(self, text: str, max_len: int) -> str:
        text = re.sub(r"\s+", " ", str(text)).strip()
        return text if len(text) <= max_len else text[: max_len - 3].rstrip() + "..."

    def _dedupe_preserve(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            item = str(item).strip()
            if not item:
                continue
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

# -----------------------------------------------------------------------------
# v2.1.6 patch layer
# -----------------------------------------------------------------------------
_original_kgs_init = KnowledgeGenerationService.__init__


def _kgs_init_v216(self, *args, **kwargs):
    _original_kgs_init(self, *args, **kwargs)
    self._enterprise_error_catalog_cache = None
    self.project_root = Path(__file__).resolve().parents[2]


def _kgs_today_iso(self) -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _kgs_canonical_object_name(self, value: str) -> str:
    normalized = self._normalize_object_name(value)
    sid = self._normalize_object_name(self.settings.default_sap_sid)
    if normalized == sid:
        return sid
    base = normalized
    while base.startswith(f"{sid}_"):
        base = base[len(sid) + 1:]
    return f"{sid}_{base}" if base else sid


def _kgs_filename_object_name(self, object_name: str) -> str:
    normalized = self._normalize_object_name(object_name)
    sid = self._normalize_object_name(self.settings.default_sap_sid)
    base = normalized
    while base.startswith(f"{sid}_"):
        base = base[len(sid) + 1:]
    return base or normalized


def _kgs_artifact_filename(self, prefix: str, object_name: str, priority: str, version: str) -> str:
    return f"{prefix}_{self.settings.default_customer_id}_{self.settings.default_sap_sid}_{self._filename_object_name(object_name)}_{priority}_{version}.md"


def _kgs_sentence_case(self, value: str) -> str:
    text = re.sub(r"\s+", " ", (value or "").strip())
    return text[:1].upper() + text[1:] if text else ""


def _kgs_split_action_text(self, value: str) -> list[str]:
    text = (value or "").replace(";", ",")
    parts = [self._sentence_case(x.strip()) for x in text.split(",") if x.strip()]
    return parts or ["Check the issue with the owning integration team and preserve runtime evidence."]


def _kgs_compact_kedb_reference(self, document_id: str | None) -> str:
    if not document_id:
        return "KEDB-UNKNOWN"
    match = re.search(r"(\d{4})\b", document_id)
    return f"KEDB-{match.group(1)}" if match else document_id


def _kgs_resolve_enterprise_error_catalog_path(self) -> Path | None:
    raw = getattr(self.settings, "knowledge_enterprise_error_catalog_path", None) or ""
    if raw and Path(raw).exists():
        return Path(raw)
    bundled = self.project_root / "resources" / "reference_materials" / "AI4BIZ_Enterprise_Error_Catalog_CPI.json"
    return bundled if bundled.exists() else None


def _kgs_load_enterprise_error_catalog(self) -> list[dict[str, Any]]:
    if self._enterprise_error_catalog_cache is not None:
        return self._enterprise_error_catalog_cache
    data: list[dict[str, Any]] = []
    path = self._resolve_enterprise_error_catalog_path()
    try:
        if path and path.exists():
            parsed = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(parsed, list):
                data = [x for x in parsed if isinstance(x, dict)]
    except Exception:
        data = []
    self._enterprise_error_catalog_cache = data
    return data


def _kgs_resolve_local_mpl_dir(self) -> Path | None:
    raw = (self.settings.mpl_local_json_dir or "").strip()
    if raw and Path(raw).exists():
        return Path(raw)
    bundled = self.project_root / "resources" / "reference_materials" / "mpl"
    return bundled if bundled.exists() else None


def _kgs_normalized_code_from_catalog_entry(self, entry: dict[str, Any]) -> str:
    pattern = str(entry.get("error_pattern") or "").upper().replace(" ", "")
    title = str(entry.get("title") or "").upper()
    if pattern == "HTTP|401" or "401" in title:
        return "HTTP_AUTHENTICATION_UNAUTHORIZED_401"
    if pattern == "HTTP|403" or "403" in title:
        return "HTTP_AUTHORIZATION_FORBIDDEN_403"
    if "TIMEOUT" in pattern or "TIMEOUT" in title:
        return "HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT"
    if pattern == "ODATA|404" or ("404" in title and "ODATA" in title):
        return "ODATA_SERVICE_NOT_FOUND_404"
    if pattern == "ODATA|400" or ("400" in title and "ODATA" in title):
        return "ODATA_PAYLOAD_BAD_REQUEST_400"
    base = pattern or self._normalize_object_name(str(entry.get("title") or "UNKNOWN_ERROR")).replace("_", "|")
    tokens = [x for x in re.split(r"[^A-Z0-9]+", base) if x]
    return "_".join(tokens[:6]) or "UNKNOWN_ENTERPRISE_ERROR"


def _kgs_taxonomy_from_catalog_entry(self, entry: dict[str, Any], code: str) -> str:
    pattern = str(entry.get("error_pattern") or "").strip()
    if pattern:
        mapping = {
            "HTTP|401": "HTTP | AUTHENTICATION | UNAUTHORIZED | 401",
            "HTTP|403": "HTTP | AUTHORIZATION | FORBIDDEN | 403",
            "HTTP|TIMEOUT": "HTTP | AVAILABILITY | REQUEST_TIMEOUT | TIMEOUT",
            "ODATA|404": "ODATA | SERVICE | NOT_FOUND | 404",
            "ODATA|400": "ODATA | PAYLOAD | BAD_REQUEST | 400",
        }
        return mapping.get(pattern.upper().replace(" ", ""), re.sub(r"\s*\|\s*", " | ", pattern))
    return self._taxonomy_from_object_name(code)


def _kgs_catalog_title_for_code(self, code: str, entry: dict[str, Any]) -> str:
    mapping = {
        "HTTP_AUTHENTICATION_UNAUTHORIZED_401": "HTTP 401 Unauthorized on outbound receiver call",
        "HTTP_AUTHORIZATION_FORBIDDEN_403": "HTTP 403 Forbidden on outbound receiver call",
        "HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT": "HTTP receiver request times out before a valid response",
        "ODATA_SERVICE_NOT_FOUND_404": "OData service or endpoint is not found on receiver side",
        "ODATA_PAYLOAD_BAD_REQUEST_400": "OData receiver rejects payload with HTTP 400 Bad Request",
    }
    return mapping.get(code, self._sentence_case(str(entry.get("title") or self._humanize_object_name(code)).split(" - ")[0]))


def _kgs_merge_catalog_entries_into_existing_scenario(self, scenario: ScenarioFamily, entries: list[dict[str, Any]], *, iflows_by_id: dict[str, dict[str, Any]]) -> None:
    for entry in entries:
        interface_name = str(entry.get("interface_name") or "").strip()
        if interface_name:
            scenario.affected_interfaces.add(interface_name)
            item = iflows_by_id.get(interface_name, {})
            scenario.flow_names.add(str(item.get("Name") or interface_name))
            scenario.package_names.add(self._resolve_package_name(item) if item else "Multiple packages")
        known_error_id = str(entry.get("known_error_id") or "").strip()
        if known_error_id:
            scenario.source_catalog_ids.add(known_error_id)
        root = self._sentence_case(str(entry.get("root_cause") or "").strip())
        if root and root not in scenario.root_causes:
            scenario.root_causes.append(root)
        for step in self._split_action_text(str(entry.get("fix_steps") or "")):
            if step not in scenario.resolution:
                scenario.resolution.append(step)
        updated_at = str(entry.get("updated_at") or "").strip()
        if updated_at and (not scenario.last_seen or updated_at > scenario.last_seen):
            scenario.last_seen = updated_at


def _kgs_scenario_from_catalog_entries(self, code: str, entries: list[dict[str, Any]], *, iflows_by_id: dict[str, dict[str, Any]]) -> ScenarioFamily:
    first = entries[0]
    priority = str(first.get("priority") or "P2").upper()
    scenario = ScenarioFamily(
        code=code,
        title=self._catalog_title_for_code(code, first),
        taxonomy=self._taxonomy_from_catalog_entry(first, code),
        symptom=self._sentence_case(str(first.get("symptom") or first.get("title") or self._humanize_object_name(code))),
        priority=priority if re.match(r"P[1-4]", priority) else "P2",
        root_causes=[self._sentence_case(str(first.get("root_cause") or "Root cause requires validation against the affected adapter and endpoint."))],
        diagnosis=self._split_action_text(str(first.get("detectable_via") or "Check MPL, adapter configuration, and security material evidence.")),
        resolution=self._split_action_text(str(first.get("fix_steps") or "Apply the least risky corrective change and replay one controlled message.")),
        validation=[
            "Verify that the same error signature does not reappear after the change.",
            "Confirm that the representative business message completes successfully.",
        ],
        workaround=self._sentence_case(str(first.get("workaround") or "Use a temporary operational workaround only while the permanent fix is prepared.")),
        monitoring_hint=self._sentence_case(str(first.get("detectable_via") or "MPL API")),
        component=self._sentence_case(str(first.get("component") or "CPI Runtime")),
        protocol_family=self._sentence_case(str(first.get("adapter_type") or first.get("system_type") or "CPI")),
        last_seen=str(first.get("updated_at") or self._today_iso()),
    )
    self._merge_catalog_entries_into_existing_scenario(scenario, entries, iflows_by_id=iflows_by_id)
    return scenario


def _kgs_merge_enterprise_catalog_into_scenarios(self, *, scenarios: dict[str, ScenarioFamily], iflows_by_id: dict[str, dict[str, Any]], iflow_ids: list[str] | None = None) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    allowed = {str(x) for x in (iflow_ids or []) if str(x)}
    for entry in self._load_enterprise_error_catalog():
        if not isinstance(entry, dict):
            continue
        interface_name = str(entry.get("interface_name") or "").strip()
        if allowed and interface_name and interface_name not in allowed and self._normalize_object_name(interface_name) not in allowed:
            continue
        code = self._normalized_code_from_catalog_entry(entry)
        grouped[code].append(entry)
    for code, entries in grouped.items():
        scenario = scenarios.get(code)
        if scenario is None:
            scenarios[code] = self._scenario_from_catalog_entries(code, entries, iflows_by_id=iflows_by_id)
        else:
            self._merge_catalog_entries_into_existing_scenario(scenario, entries, iflows_by_id=iflows_by_id)


def _kgs_discover_existing_kedb_state(self) -> tuple[int, set[str]]:
    max_id = 0
    objects: set[str] = set()
    scan_dirs = [self.project_root / "resources" / "examples" / "kedb", self.project_root / "resources" / "reference_materials"]
    for directory in scan_dirs:
        if not directory.exists():
            continue
        for path in directory.rglob("KB_*.md"):
            try:
                parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            object_name = parsed.get("metadata", {}).get("object_name") or self._object_from_filename(path.name)
            objects.add(self._canonical_object_name(object_name))
            match = re.search(r"KEDB(?:-[A-Z0-9]+)?-(\d{4})\b", parsed.get("document_id") or "")
            if match:
                max_id = max(max_id, int(match.group(1)))
    for entry in self._load_enterprise_error_catalog():
        known_error_id = str(entry.get("known_error_id") or "")
        match = re.search(r"KEDB(?:-[A-Z0-9]+)?-(\d{4})\b", known_error_id)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id, objects


def _kgs_prepare_new_kedb_scenarios(self, package_id: str | None = None, iflow_ids: list[str] | None = None, use_mpl: bool = True, mpl_hours: int | None = None, mpl_limit: int | None = None):
    async def inner():
        scenarios = await self._derive_scenarios(package_id=package_id, iflow_ids=iflow_ids, use_mpl=use_mpl, mpl_hours=mpl_hours, mpl_limit=mpl_limit)
        last_id, existing_objects = self._discover_existing_kedb_state()
        prepared: list[ScenarioFamily] = []
        next_id = last_id + 1
        for code in sorted(scenarios):
            scenario = scenarios[code]
            object_name = self._canonical_object_name(code)
            if object_name in existing_objects:
                continue
            scenario.document_id = f"KEDB-{scenario.priority}-{next_id:04d}"
            next_id += 1
            prepared.append(scenario)
        return prepared
    return inner()


async def _kgs_generate_kedb_documents(self, version: str, package_id: str | None = None, iflow_ids: list[str] | None = None, output_dir: str | None = None, use_mpl: bool = True, mpl_hours: int | None = None, mpl_limit: int | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    target_dir = self._resolve_output_dir(output_dir, "kedb", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    scenarios = await self._prepare_new_kedb_scenarios(package_id=package_id, iflow_ids=iflow_ids, use_mpl=use_mpl, mpl_hours=mpl_hours, mpl_limit=mpl_limit)
    files: list[str] = []
    for scenario in scenarios:
        object_name = self._canonical_object_name(scenario.code)
        filename = self._artifact_filename("KB", object_name, scenario.priority, version)
        out_path = target_dir / filename
        out_path.write_text(self._render_kedb(scenario=scenario, version=version), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "kedb", "version": version, "count": len(files), "generated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


async def _kgs_generate_runbook_documents(self, version: str, package_id: str | None = None, iflow_ids: list[str] | None = None, output_dir: str | None = None, use_mpl: bool = True, mpl_hours: int | None = None, mpl_limit: int | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    target_dir = self._resolve_output_dir(output_dir, "runbooks", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    scenarios = await self._prepare_new_kedb_scenarios(package_id=package_id, iflow_ids=iflow_ids, use_mpl=use_mpl, mpl_hours=mpl_hours, mpl_limit=mpl_limit)
    files: list[str] = []
    for scenario in scenarios:
        object_name = self._canonical_object_name(scenario.code)
        filename = self._artifact_filename("RB", object_name, scenario.priority, version)
        out_path = target_dir / filename
        out_path.write_text(self._render_runbook(scenario=scenario, version=version), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "runbook", "version": version, "count": len(files), "generated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


async def _kgs_derive_scenarios(self, package_id: str | None = None, iflow_ids: list[str] | None = None, use_mpl: bool = True, mpl_hours: int | None = None, mpl_limit: int | None = None) -> dict[str, ScenarioFamily]:
    scenarios: dict[str, ScenarioFamily] = {}
    iflows = await self._collect_iflows(package_id=package_id, iflow_ids=iflow_ids)
    iflows_by_id: dict[str, dict[str, Any]] = {str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW"): item for item in iflows}
    for item in iflows:
        iflow_id = str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW")
        artifact = await self.sap_client.get_iflow_content(iflow_id=iflow_id)
        analysis = self.iflow_parser.parse(artifact)
        flow_name = str(item.get("Name") or iflow_id)
        package_name = self._resolve_package_name(item)
        for scenario in self._candidate_scenarios(analysis):
            family = scenarios.setdefault(scenario.code, scenario)
            family.affected_interfaces.add(iflow_id)
            family.flow_names.add(flow_name)
            family.package_names.add(package_name)
    self._merge_enterprise_catalog_into_scenarios(scenarios=scenarios, iflows_by_id=iflows_by_id, iflow_ids=iflow_ids)
    if use_mpl:
        local_mpl_dir = self._resolve_local_mpl_dir()
        signals = await self.mpl_semantic_service.collect_failure_signals(hours_back=mpl_hours or self.settings.mpl_default_lookback_hours, limit=mpl_limit or self.settings.mpl_default_limit, local_json_dir=str(local_mpl_dir) if local_mpl_dir else None)
        summary = self.mpl_semantic_service.summarize_signals(signals)
        self._merge_mpl_summary_into_scenarios(scenarios=scenarios, mpl_summary=summary, iflows_by_id=iflows_by_id)
    return scenarios


def _kgs_render_kedb(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    metadata = {
        "environment": self.settings.default_environment,
        "customer_id": self.settings.default_customer_id,
        "system_id": self.settings.default_system_id,
        "sap_sid": self.settings.default_sap_sid,
        "artifact_type": "kedb",
        "object_name": object_name,
        "priority": scenario.priority,
        "interface_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
        "integration_flow_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
        "integration_flow_name": sorted(scenario.flow_names)[0] if scenario.flow_names else "Multiple interfaces",
        "package_name": ", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages",
        "review_cycle": self.settings.default_review_cycle,
        "document_id": scenario.document_id or f"KEDB-{scenario.priority}-0000",
    }
    related = [
        f"Primary runbook: {self._artifact_filename('RB', object_name, scenario.priority, version)}",
        f"Catalog objects: {', '.join(sorted(scenario.affected_interfaces)[:10]) or 'None detected'}",
        f"Updated at: {self._today_iso()}",
        "Owner: IntegrationTeam",
        "Notes: Expanded official document links with SAP Help.",
    ]
    if scenario.source_catalog_ids:
        related.insert(1, f"Enterprise catalog IDs: {', '.join(sorted(scenario.source_catalog_ids)[:8])}")
    diagnosis_signals = list(scenario.diagnosis)
    diagnosis_signals.extend(self._strip_bullet_prefix(x) for x in scenario.runtime_evidence[:4])
    sections = {"SYMPTOM": [scenario.symptom], "ERROR PATTERN": [scenario.taxonomy], "ROOT CAUSE": scenario.root_causes, "DIAGNOSIS SIGNALS": diagnosis_signals, "RESOLUTION": scenario.resolution, "VALIDATION": scenario.validation, "WORKAROUND": [scenario.workaround], "RELATED ARTIFACTS": related}
    sections = self._refine_sections_with_policy(artifact_type="kedb", title=scenario.title, metadata=metadata, sections=sections)
    return self._render_kedb_from_sections(scenario.title, metadata, sections)


def _kgs_render_runbook(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    source_kedb_id = self._compact_kedb_reference(scenario.document_id)
    rb_numeric = re.search(r"(\d{4})$", scenario.document_id or "")
    metadata = {
        "environment": self.settings.default_environment,
        "customer_id": self.settings.default_customer_id,
        "system_id": self.settings.default_system_id,
        "sap_sid": self.settings.default_sap_sid,
        "artifact_type": "runbook",
        "object_name": object_name,
        "priority": scenario.priority,
        "interface_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
        "integration_flow_id": sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE",
        "integration_flow_name": sorted(scenario.flow_names)[0] if scenario.flow_names else "Multiple interfaces",
        "package_name": ", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages",
        "review_cycle": self.settings.default_review_cycle,
        "document_id": f"RB-{scenario.priority}-{rb_numeric.group(1) if rb_numeric else '0000'}",
    }
    sections = {
        "PURPOSE": [f"This runbook supports incident triage, diagnosis, containment, recovery, and post-fix validation for the KEDB scenario **{object_name}**. It is intended for SAP CPI operations and RAG-based incident guidance."],
        "BUSINESS CONTEXT": ["Business process: Scenario-dependent CPI integration processing", f"Description: Primary reference interface is **{sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE'}**. The same error family may also affect other interfaces listed in the affected-interface set.", "Message direction: scenario-dependent", f"Business criticality: {self._criticality_from_priority(scenario.priority)}", f"Impact: {scenario.symptom}", f"Affected interfaces count: {len(scenario.affected_interfaces)}", f"Representative affected interfaces: {', '.join(sorted(scenario.affected_interfaces)[:5]) or 'MULTI_INTERFACE'}"],
        "TECHNICAL LANDSCAPE": [f"Package: {', '.join(sorted(x for x in scenario.package_names if x)) or 'Multiple packages'}", f"Integration flow ID: {sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE'}", f"Integration flow name: {sorted(scenario.flow_names)[0] if scenario.flow_names else 'Multiple interfaces'}", f"Processing component: {scenario.component}", f"Protocol family: {scenario.protocol_family}", f"Error pattern: {scenario.taxonomy}", "System type: cpi", f"Source KEDB ID(s): {source_kedb_id}"],
        "MONITORING AND MPL EVIDENCE": [f"Monitoring source: {scenario.monitoring_hint}", f"Observed failed MPL messages for this family: {scenario.occurrence_count}", f"Last seen in MPL: {scenario.last_seen or 'unknown'}", "Preserve MessageGuid, CorrelationId, Sender, Receiver, and IntegrationFlowName when available.", "Compare the failing execution with the last successful run in the same window.", *[self._strip_bullet_prefix(x) for x in scenario.runtime_evidence[:5]]],
        "ERROR SIGNATURE": [f"Title: {scenario.title}", f"Short symptom: {scenario.symptom}", f"Normalized object name: {object_name}"],
        "KNOWN ROOT CAUSES": scenario.root_causes,
        "PREREQUISITES FOR INVESTIGATION": ["Access to SAP CPI Monitor / MPL and trace where applicable.", f"Access to the owning package(s): {', '.join(sorted(x for x in scenario.package_names if x)) or 'Multiple packages'}.", "Deployment history, security material access, and one representative failing payload."],
        "DIAGNOSIS STEPS": scenario.diagnosis,
        "RECOVERY STEPS": ["Contain the incident and preserve reproducible evidence before changing configuration.", *scenario.resolution, f"Rollback option: {scenario.workaround}"],
        "ESCALATION CRITERIA": ["Support owner: IntegrationTeam", "Escalation group: RCMO-CPI-L2", "Escalate when the issue is reproducible, business impact expands, or controlled recovery fails.", "Evidence required: MessageGuid, time window, failing step, error text, configuration delta, and replay outcome."],
        "POST-FIX VALIDATION": scenario.validation,
    }
    sections = self._refine_sections_with_policy(artifact_type="runbook", title=scenario.title, metadata=metadata, sections=sections)
    return self._render_runbook_from_sections(scenario.title, metadata, sections)


def _kgs_normalize_metadata(self, metadata: dict[str, str], artifact_type: str) -> dict[str, str]:
    object_name = metadata.get("object_name", "UNKNOWN_OBJECT")
    if artifact_type in {"kedb", "runbook"}:
        object_name = self._canonical_object_name(object_name)
    return {
        "environment": metadata.get("environment", self.settings.default_environment),
        "customer_id": metadata.get("customer_id", self.settings.default_customer_id),
        "system_id": metadata.get("system_id", self.settings.default_system_id),
        "sap_sid": metadata.get("sap_sid", self.settings.default_sap_sid),
        "artifact_type": metadata.get("artifact_type", artifact_type),
        "object_name": object_name,
        "priority": metadata.get("priority", "P3"),
        "interface_id": metadata.get("interface_id", "UNKNOWN_INTERFACE"),
        "integration_flow_id": metadata.get("integration_flow_id", metadata.get("interface_id", "UNKNOWN_INTERFACE")),
        "integration_flow_name": metadata.get("integration_flow_name", metadata.get("interface_id", "UNKNOWN_INTERFACE")),
        "package_name": metadata.get("package_name", "Multiple packages"),
        "review_cycle": metadata.get("review_cycle", self.settings.default_review_cycle),
    }


def _kgs_enrich_update_kedb_sections(self, metadata: dict[str, str], sections: dict[str, list[str]], version: str) -> dict[str, list[str]]:
    related = [self._strip_bullet_prefix(x) for x in sections.get("RELATED ARTIFACTS", [])]
    updated = [line for line in related if not line.lower().startswith("updated at:") and "sap help summaries" not in line.lower()]
    primary_runbook = f"Primary runbook: {self._artifact_filename('RB', metadata['object_name'], metadata['priority'], version)}"
    if not any(line.startswith("Primary runbook:") for line in updated):
        updated.insert(0, primary_runbook)
    else:
        updated = [primary_runbook if line.startswith("Primary runbook:") else line for line in updated]
    updated.append(f"Updated at: {self._today_iso()}")
    if not any(line.startswith("Owner:") for line in updated):
        updated.append("Owner: IntegrationTeam")
    updated.append("Notes: Expanded official document links with SAP Help.")
    sections["RELATED ARTIFACTS"] = self._dedupe_preserve(updated)
    return sections


def _kgs_enrich_update_runbook_sections(self, metadata: dict[str, str], sections: dict[str, list[str]]) -> dict[str, list[str]]:
    technical = [self._strip_bullet_prefix(x) for x in sections.get("TECHNICAL LANDSCAPE", [])]
    source_ref = f"Source KEDB ID(s): {self._compact_kedb_reference(metadata.get('document_id'))}"
    if not any(line.startswith("Source KEDB ID") for line in technical):
        technical.append(source_ref)
    sections["TECHNICAL LANDSCAPE"] = self._dedupe_preserve(technical)
    return sections


def _kgs_update_kedb_documents(self, version: str, source_dir: str | None = None, source_zip_path: str | None = None, output_dir: str | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    source_path = self._resolve_markdown_source(artifact_type="kedb", source_dir=source_dir, source_zip_path=source_zip_path)
    target_dir = self._resolve_output_dir(output_dir, "kedb_updated", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for path in sorted(source_path.glob("*.md")):
        parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
        metadata = self._normalize_metadata(parsed["metadata"], artifact_type="kedb")
        metadata["artifact_type"] = "kedb"
        metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
        metadata["object_name"] = self._canonical_object_name(metadata.get("object_name") or self._object_from_filename(path.name))
        metadata["review_cycle"] = metadata.get("review_cycle") or self.settings.default_review_cycle
        metadata["package_name"] = metadata.get("package_name") or "Multiple packages"
        title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
        metadata["document_id"] = parsed.get("document_id") or f"KEDB-{metadata['priority']}-{metadata['object_name']}"
        sections = parsed["sections"]
        ordered = {
            "SYMPTOM": sections.get("1. SYMPTOM") or sections.get("SYMPTOM") or ["- Symptom requires expert refinement."],
            "ERROR PATTERN": [self._normalize_taxonomy_line(x) for x in (sections.get("2. ERROR PATTERN") or sections.get("ERROR PATTERN") or [f"- {self._taxonomy_from_object_name(metadata['object_name'])}"])],
            "ROOT CAUSE": sections.get("3. ROOT CAUSE") or sections.get("ROOT CAUSE") or ["- Root cause needs confirmation from runtime evidence."],
            "DIAGNOSIS SIGNALS": sections.get("4. DIAGNOSIS SIGNALS") or sections.get("DIAGNOSIS SIGNALS") or ["- Check MPL and compare failing step against last successful message."],
            "RESOLUTION": sections.get("5. RESOLUTION") or sections.get("RESOLUTION") or ["- Apply the least risky corrective change and redeploy."],
            "VALIDATION": sections.get("6. VALIDATION") or sections.get("VALIDATION") or ["- Confirm the message completes successfully after the change."],
            "WORKAROUND": sections.get("7. WORKAROUND") or sections.get("WORKAROUND") or ["- Escalate if no safe workaround is available."],
            "RELATED ARTIFACTS": sections.get("8. RELATED ARTIFACTS") or sections.get("RELATED ARTIFACTS") or [f"Primary runbook: {self._artifact_filename('RB', metadata['object_name'], metadata['priority'], version)}"],
        }
        ordered = self._enrich_update_kedb_sections(metadata=metadata, sections=ordered, version=version)
        ordered = self._refine_sections_with_policy(artifact_type="kedb", title=title, metadata=metadata, sections=ordered)
        out_path = target_dir / self._artifact_filename("KB", metadata['object_name'], metadata['priority'], version)
        out_path.write_text(self._render_kedb_from_sections(title, metadata, ordered), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "kedb_update", "version": version, "source_dir": str(source_path), "count": len(files), "updated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


def _kgs_update_runbook_documents(self, version: str, source_dir: str | None = None, source_zip_path: str | None = None, output_dir: str | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    source_path = self._resolve_markdown_source(artifact_type="runbooks", source_dir=source_dir, source_zip_path=source_zip_path)
    target_dir = self._resolve_output_dir(output_dir, "runbooks_updated", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for path in sorted(source_path.glob("*.md")):
        parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
        metadata = self._normalize_metadata(parsed["metadata"], artifact_type="runbook")
        metadata["artifact_type"] = "runbook"
        metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
        metadata["object_name"] = self._canonical_object_name(metadata.get("object_name") or self._object_from_filename(path.name))
        metadata["review_cycle"] = metadata.get("review_cycle") or self.settings.default_review_cycle
        metadata["package_name"] = metadata.get("package_name") or "Multiple packages"
        title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
        metadata["document_id"] = parsed.get("document_id") or f"RB-{metadata['priority']}-{metadata['object_name']}"
        sections = parsed["sections"]
        ordered = {
            "PURPOSE": sections.get("1. PURPOSE") or sections.get("PURPOSE") or [f"This runbook supports the canonical incident pattern {metadata['object_name']}."],
            "BUSINESS CONTEXT": sections.get("2. BUSINESS CONTEXT") or sections.get("BUSINESS CONTEXT") or ["- Business impact requires confirmation from the owning interface team."],
            "TECHNICAL LANDSCAPE": sections.get("3. TECHNICAL LANDSCAPE") or sections.get("TECHNICAL LANDSCAPE") or ["- Package: Multiple packages"],
            "MONITORING AND MPL EVIDENCE": sections.get("4. MONITORING AND MPL EVIDENCE") or sections.get("MONITORING AND MPL EVIDENCE") or ["- Review MPL entries in the affected time window and preserve MessageGuid evidence."],
            "ERROR SIGNATURE": sections.get("5. ERROR SIGNATURE") or sections.get("ERROR SIGNATURE") or [f"- Normalized object name: {metadata['object_name']}"],
            "KNOWN ROOT CAUSES": sections.get("6. KNOWN ROOT CAUSES") or sections.get("KNOWN ROOT CAUSES") or ["- Root cause requires technical verification."],
            "PREREQUISITES FOR INVESTIGATION": sections.get("7. PREREQUISITES FOR INVESTIGATION") or sections.get("PREREQUISITES FOR INVESTIGATION") or ["- Access to CPI Monitor, Security Material, and deployment history."],
            "DIAGNOSIS STEPS": sections.get("8. DIAGNOSIS STEPS") or sections.get("DIAGNOSIS STEPS") or sections.get("DIAGNOSIS PROCEDURE") or ["- Check MPL and compare the failure with the last successful message."],
            "RECOVERY STEPS": sections.get("9. RECOVERY STEPS") or sections.get("RECOVERY STEPS") or sections.get("RECOVERY / FIX ACTIONS") or ["- Apply the least risky corrective change, redeploy, and replay one controlled message."],
            "ESCALATION CRITERIA": sections.get("10. ESCALATION CRITERIA") or sections.get("ESCALATION CRITERIA") or sections.get("ESCALATION") or ["- Escalate when the issue is reproducible and cannot be stabilized with standard operational handling."],
            "POST-FIX VALIDATION": sections.get("11. POST-FIX VALIDATION") or sections.get("POST-FIX VALIDATION") or sections.get("VALIDATION AFTER FIX") or ["- Confirm that the same error signature does not reappear after controlled replay."],
        }
        ordered = self._enrich_update_runbook_sections(metadata=metadata, sections=ordered)
        ordered = self._refine_sections_with_policy(artifact_type="runbook", title=title, metadata=metadata, sections=ordered)
        out_path = target_dir / self._artifact_filename("RB", metadata['object_name'], metadata['priority'], version)
        out_path.write_text(self._render_runbook_from_sections(title, metadata, ordered), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "runbook_update", "version": version, "source_dir": str(source_path), "count": len(files), "updated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


def _kgs_normalize_action_line(self, line: str, *, artifact_type: str, section_name: str) -> str:
    text = self._strip_bullet_prefix(line)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^Generated by .*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^Generated at:.*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^No directly matching MPL sample was found in the provided export\.?\s*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"The MPL ID for the failed message is\s*:\s*[A-Za-z0-9_\-]+", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^[A-Za-z0-9_.:$]+(?:Exception|Error):\s*", "", text)
    if not text:
        return ""
    if artifact_type == "runbook" and section_name in {"DIAGNOSIS STEPS", "RECOVERY STEPS", "POST-FIX VALIDATION", "ESCALATION CRITERIA"}:
        text = text[0].upper() + text[1:]
        if not re.match(r"^(Check|Verify|Confirm|Review|Capture|Compare|Collect|Preserve|Reduce|Apply|Replay|Lower|Schedule|Escalate|Contain|Inspect|Coordinate|Use|Document|Re-run|Increase|Persist|Open|Validate)", text):
            text = f"Check {text[0].lower() + text[1:]}" if section_name == "DIAGNOSIS STEPS" else text
    return text


def _kgs_policy_context_excerpt(self) -> str:
    candidates = [self.project_root / "resources" / "reference_materials" / "AI4BIZ_Knowledge_Ingestion_Guide.txt", self.project_root / "resources" / "reference_materials" / "BM25_Runbook_Authoring_Guideline.txt"]
    chunks: list[str] = []
    for path in candidates:
        if path.exists():
            try:
                chunks.append(path.read_text(encoding="utf-8")[:2000])
            except Exception:
                continue
    return "\n\n".join(chunks)


def _kgs_maybe_refine_with_openai(self, artifact_type: str, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> dict[str, list[str]] | None:
    if not self.settings.openai_api_key:
        return None
    payload = {
        "model": self.settings.openai_model,
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": "Refine SAP CPI markdown section bullets. Keep the same section keys and order. Use the enterprise ingestion policies for atomicity, stable terminology, and BM25-friendly phrasing. Be concrete, concise, action-led, realistic, and fact-preserving. Do not invent metadata. Return strict JSON: {\"sections\": {section: [bullets]}}.\n\n" + self._policy_context_excerpt()}]},
            {"role": "user", "content": [{"type": "input_text", "text": json.dumps({"artifact_type": artifact_type, "title": title, "metadata": metadata, "sections": sections}, ensure_ascii=False)}]},
        ],
        "text": {"format": {"type": "json_object"}},
    }
    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.post(f"{self.settings.openai_base_url.rstrip('/')}/responses", headers={"Authorization": f"Bearer {self.settings.openai_api_key}", "Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            data = response.json()
        output_text = data.get("output_text") or ""
        if not output_text:
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"} and content.get("text"):
                        output_text += content.get("text", "")
        parsed = json.loads(output_text) if output_text else {}
        result = parsed.get("sections") if isinstance(parsed, dict) else None
        if isinstance(result, dict):
            normalized: dict[str, list[str]] = {}
            for key, value in result.items():
                if isinstance(value, list):
                    normalized[key] = [self._strip_bullet_prefix(str(x)) for x in value if str(x).strip()]
            return normalized or None
    except Exception:
        return None
    return None


def _kgs_load_inventory_cache(self) -> dict[str, Any]:
    if self._inventory_cache is not None:
        return self._inventory_cache
    cache = {"iflows": [], "packages": []}
    raw_path = (self.settings.knowledge_inventory_path or "").strip()
    if raw_path:
        path = Path(raw_path)
    else:
        path = self.project_root / "resources" / "reference_materials" / "sap-ci-design-and-configuration-inventory.zip"
    if not path.exists():
        self._inventory_cache = cache
        return cache
    try:
        if path.is_file() and path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as zf:
                for name in zf.namelist():
                    if name.endswith("/odata/iflows.json"):
                        data = json.loads(zf.read(name).decode("utf-8"))
                        cache["iflows"].extend(self._extract_odata_results(data))
                    elif name.endswith("/odata/packages.json"):
                        data = json.loads(zf.read(name).decode("utf-8"))
                        cache["packages"].extend(self._extract_odata_results(data))
        elif path.is_dir():
            for file in path.rglob("iflows.json"):
                cache["iflows"].extend(self._extract_odata_results(json.loads(file.read_text(encoding="utf-8"))))
            for file in path.rglob("packages.json"):
                cache["packages"].extend(self._extract_odata_results(json.loads(file.read_text(encoding="utf-8"))))
    except Exception:
        cache = {"iflows": [], "packages": []}
    self._inventory_cache = cache
    return cache


KnowledgeGenerationService.__init__ = _kgs_init_v216
KnowledgeGenerationService._today_iso = _kgs_today_iso
KnowledgeGenerationService._canonical_object_name = _kgs_canonical_object_name
KnowledgeGenerationService._filename_object_name = _kgs_filename_object_name
KnowledgeGenerationService._artifact_filename = _kgs_artifact_filename
KnowledgeGenerationService._sentence_case = _kgs_sentence_case
KnowledgeGenerationService._split_action_text = _kgs_split_action_text
KnowledgeGenerationService._compact_kedb_reference = _kgs_compact_kedb_reference
KnowledgeGenerationService._resolve_enterprise_error_catalog_path = _kgs_resolve_enterprise_error_catalog_path
KnowledgeGenerationService._load_enterprise_error_catalog = _kgs_load_enterprise_error_catalog
KnowledgeGenerationService._resolve_local_mpl_dir = _kgs_resolve_local_mpl_dir
KnowledgeGenerationService._normalized_code_from_catalog_entry = _kgs_normalized_code_from_catalog_entry
KnowledgeGenerationService._taxonomy_from_catalog_entry = _kgs_taxonomy_from_catalog_entry
KnowledgeGenerationService._catalog_title_for_code = _kgs_catalog_title_for_code
KnowledgeGenerationService._merge_catalog_entries_into_existing_scenario = _kgs_merge_catalog_entries_into_existing_scenario
KnowledgeGenerationService._scenario_from_catalog_entries = _kgs_scenario_from_catalog_entries
KnowledgeGenerationService._merge_enterprise_catalog_into_scenarios = _kgs_merge_enterprise_catalog_into_scenarios
KnowledgeGenerationService._discover_existing_kedb_state = _kgs_discover_existing_kedb_state
KnowledgeGenerationService._prepare_new_kedb_scenarios = _kgs_prepare_new_kedb_scenarios
KnowledgeGenerationService.generate_kedb_documents = _kgs_generate_kedb_documents
KnowledgeGenerationService.generate_runbook_documents = _kgs_generate_runbook_documents
KnowledgeGenerationService._derive_scenarios = _kgs_derive_scenarios
KnowledgeGenerationService._render_kedb = _kgs_render_kedb
KnowledgeGenerationService._render_runbook = _kgs_render_runbook
KnowledgeGenerationService._normalize_metadata = _kgs_normalize_metadata
KnowledgeGenerationService._enrich_update_kedb_sections = _kgs_enrich_update_kedb_sections
KnowledgeGenerationService._enrich_update_runbook_sections = _kgs_enrich_update_runbook_sections
KnowledgeGenerationService.update_kedb_documents = _kgs_update_kedb_documents
KnowledgeGenerationService.update_runbook_documents = _kgs_update_runbook_documents
KnowledgeGenerationService._normalize_action_line = _kgs_normalize_action_line
KnowledgeGenerationService._policy_context_excerpt = _kgs_policy_context_excerpt
KnowledgeGenerationService._maybe_refine_with_openai = _kgs_maybe_refine_with_openai
KnowledgeGenerationService._load_inventory_cache = _kgs_load_inventory_cache


# -----------------------------------------------------------------------------
# v2.1.7 patch layer
# -----------------------------------------------------------------------------
def _kgs_render_structured_markdown_v217(
    self,
    *,
    title: str,
    metadata: dict[str, str],
    id_label: str,
    doc_id: str,
    title_label: str,
    title_value: str,
    section_order: list[str],
    section_map: dict[str, list[str]],
    bullet: str,
    escape_underscores: bool,
    plain_sections: set[str] | None = None,
) -> str:
    def esc(value: str) -> str:
        value = str(value)
        return value.replace('_', r'\_') if escape_underscores else value

    ordered_meta_keys = [
        'environment',
        'customer_id',
        'system_id',
        'sap_sid',
        'artifact_type',
        'object_name',
        'priority',
        'interface_id',
        'integration_flow_id',
        'integration_flow_name',
        'package_name',
        'review_cycle',
        'version',
    ]
    parts: list[str] = [f"# {esc(title)}", '']
    for key in ordered_meta_keys:
        if key in metadata and metadata.get(key) not in {None, ''}:
            parts.append(f'{esc(key)}: "{esc(metadata[key])}"')
    for key, value in metadata.items():
        if key in {'document_id', *ordered_meta_keys}:
            continue
        if value not in {None, ''}:
            parts.append(f'{esc(key)}: "{esc(value)}"')

    parts.extend([
        '',
        id_label,
        esc(doc_id),
        '',
        title_label,
        esc(title_value),
        '',
        'CUSTOMER',
        esc(metadata.get('customer_id', self.settings.default_customer_id)),
        '',
        'SYSTEM',
        esc(metadata.get('sap_sid', self.settings.default_sap_sid)),
        '',
        'PRIORITY',
        esc(metadata.get('priority', 'P3')),
        '',
        'VERSION',
        esc(metadata.get('version', 'v1')),
        '',
    ])
    plain_sections = plain_sections or set()
    for section_name in section_order:
        parts.append(section_name)
        lines = section_map.get(section_name, []) or ['None']
        for idx, line in enumerate(lines):
            cleaned = self._strip_bullet_prefix(line).replace(r'\_', '_')
            if section_name in plain_sections and idx == 0:
                parts.append(esc(cleaned))
            else:
                parts.append(f"{bullet} {esc(cleaned)}")
        parts.append('')
    return '\n'.join(parts).rstrip() + '\n'


def _kgs_parse_markdown_sections_v217(self, text: str) -> dict[str, Any]:
    lines = text.splitlines()
    title = ''
    metadata: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    document_id = ''
    title_label = ''
    current_section: str | None = None

    for idx, line in enumerate(lines):
        stripped = line.strip()
        normalized = stripped.replace(r'\_', '_')
        if idx == 0 and normalized.startswith('# '):
            title = normalized[2:].strip()
            continue
        if re.match(r'^[a-z_\\]+:\s*"?.+"?$', stripped):
            key, val = stripped.split(':', 1)
            key = key.strip().replace(r'\_', '_')
            value = val.strip().strip('"').replace(r'\_', '_')
            metadata[key] = value
            continue
        if normalized in {'KEDB ID', 'RUNBOOK ID', 'DOC ID'}:
            title_label = normalized
            current_section = None
            continue
        if normalized in {'KEDB TITLE', 'RUNBOOK TITLE', 'DOC TITLE', 'CUSTOMER', 'SYSTEM', 'PRIORITY', 'VERSION'}:
            current_section = None
            continue
        if not document_id and title_label in {'KEDB ID', 'RUNBOOK ID', 'DOC ID'}:
            document_id = normalized
            title_label = ''
            continue
        if re.match(r'^\d+\.\s+', normalized):
            current_section = normalized
            sections[current_section] = []
            continue
        if current_section and normalized:
            sections[current_section].append(normalized)
    return {'title': title, 'metadata': metadata, 'sections': sections, 'document_id': document_id}


def _kgs_normalize_metadata_v217(self, metadata: dict[str, str], artifact_type: str) -> dict[str, str]:
    object_name = metadata.get('object_name', 'UNKNOWN_OBJECT').replace(r'\_', '_')
    if artifact_type in {'kedb', 'runbook'}:
        object_name = self._canonical_object_name(object_name)
    return {
        'environment': metadata.get('environment', self.settings.default_environment).replace(r'\_', '_'),
        'customer_id': metadata.get('customer_id', self.settings.default_customer_id).replace(r'\_', '_'),
        'system_id': metadata.get('system_id', self.settings.default_system_id).replace(r'\_', '_'),
        'sap_sid': metadata.get('sap_sid', self.settings.default_sap_sid).replace(r'\_', '_'),
        'artifact_type': metadata.get('artifact_type', artifact_type).replace(r'\_', '_'),
        'object_name': object_name,
        'priority': metadata.get('priority', 'P3').replace(r'\_', '_'),
        'interface_id': metadata.get('interface_id', 'UNKNOWN_INTERFACE').replace(r'\_', '_'),
        'integration_flow_id': metadata.get('integration_flow_id', metadata.get('interface_id', 'UNKNOWN_INTERFACE')).replace(r'\_', '_'),
        'integration_flow_name': metadata.get('integration_flow_name', metadata.get('interface_id', 'UNKNOWN_INTERFACE')).replace(r'\_', '_'),
        'package_name': metadata.get('package_name', 'Multiple packages').replace(r'\_', '_'),
        'review_cycle': metadata.get('review_cycle', self.settings.default_review_cycle).replace(r'\_', '_'),
        'version': self._normalize_version(metadata.get('version', 'v1').replace(r'\_', '_')),
    }


def _kgs_render_kedb_from_sections_v217(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
    metadata = dict(metadata)
    metadata['version'] = self._normalize_version(metadata.get('version', 'v1'))
    return self._render_structured_markdown(
        title=title,
        metadata=metadata,
        id_label='KEDB ID',
        doc_id=metadata.get('document_id') or f"KEDB-{metadata['priority']}-{metadata['object_name']}",
        title_label='KEDB TITLE',
        title_value=title,
        section_order=[
            '1. SYMPTOM',
            '2. ERROR PATTERN',
            '3. ROOT CAUSE',
            '4. DIAGNOSIS SIGNALS',
            '5. RESOLUTION',
            '6. VALIDATION',
            '7. WORKAROUND',
            '8. RELATED ARTIFACTS',
        ],
        section_map={
            '1. SYMPTOM': sections.get('SYMPTOM', ['None']),
            '2. ERROR PATTERN': sections.get('ERROR PATTERN', [self._taxonomy_from_object_name(metadata['object_name'])]),
            '3. ROOT CAUSE': sections.get('ROOT CAUSE', ['None']),
            '4. DIAGNOSIS SIGNALS': sections.get('DIAGNOSIS SIGNALS', ['None']),
            '5. RESOLUTION': sections.get('RESOLUTION', ['None']),
            '6. VALIDATION': sections.get('VALIDATION', ['None']),
            '7. WORKAROUND': sections.get('WORKAROUND', ['None']),
            '8. RELATED ARTIFACTS': sections.get('RELATED ARTIFACTS', ['None']),
        },
        bullet='*',
        escape_underscores=True,
        plain_sections=set(),
    )


def _kgs_render_runbook_from_sections_v217(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
    metadata = dict(metadata)
    metadata['version'] = self._normalize_version(metadata.get('version', 'v1'))
    return self._render_structured_markdown(
        title=title,
        metadata=metadata,
        id_label='RUNBOOK ID',
        doc_id=metadata.get('document_id') or f"RB-{metadata['priority']}-{metadata['object_name']}",
        title_label='RUNBOOK TITLE',
        title_value=title,
        section_order=[
            '1. PURPOSE',
            '2. BUSINESS CONTEXT',
            '3. TECHNICAL LANDSCAPE',
            '4. MONITORING AND MPL EVIDENCE',
            '5. ERROR SIGNATURE',
            '6. KNOWN ROOT CAUSES',
            '7. PREREQUISITES FOR INVESTIGATION',
            '8. DIAGNOSIS STEPS',
            '9. RECOVERY STEPS',
            '10. ESCALATION CRITERIA',
            '11. POST-FIX VALIDATION',
        ],
        section_map={
            '1. PURPOSE': sections.get('PURPOSE', ['This runbook supports incident triage, diagnosis, recovery, and validation for the referenced scenario.']),
            '2. BUSINESS CONTEXT': sections.get('BUSINESS CONTEXT', ['None']),
            '3. TECHNICAL LANDSCAPE': sections.get('TECHNICAL LANDSCAPE', ['None']),
            '4. MONITORING AND MPL EVIDENCE': sections.get('MONITORING AND MPL EVIDENCE', ['No directly matching MPL evidence was attached during generation.']),
            '5. ERROR SIGNATURE': sections.get('ERROR SIGNATURE', ['None']),
            '6. KNOWN ROOT CAUSES': sections.get('KNOWN ROOT CAUSES', ['None']),
            '7. PREREQUISITES FOR INVESTIGATION': sections.get('PREREQUISITES FOR INVESTIGATION', ['Access to SAP CPI Monitor / MPL and the affected iFlow.']),
            '8. DIAGNOSIS STEPS': sections.get('DIAGNOSIS STEPS', ['Check MPL for the failing time window and compare with the last successful run.']),
            '9. RECOVERY STEPS': sections.get('RECOVERY STEPS', ['Stabilize the flow, apply the corrective change, and replay one controlled message.']),
            '10. ESCALATION CRITERIA': sections.get('ESCALATION CRITERIA', ['Escalate when the issue is reproducible or business impact expands.']),
            '11. POST-FIX VALIDATION': sections.get('POST-FIX VALIDATION', ['Confirm that the same signature no longer appears in the immediate post-fix window.']),
        },
        bullet='*',
        escape_underscores=True,
        plain_sections={'1. PURPOSE'},
    )


def _kgs_render_kedb_v217(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    metadata = {
        'environment': self.settings.default_environment,
        'customer_id': self.settings.default_customer_id,
        'system_id': self.settings.default_system_id,
        'sap_sid': self.settings.default_sap_sid,
        'artifact_type': 'kedb',
        'object_name': object_name,
        'priority': scenario.priority,
        'interface_id': sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE',
        'integration_flow_id': sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE',
        'integration_flow_name': sorted(scenario.flow_names)[0] if scenario.flow_names else 'Multiple interfaces',
        'package_name': ', '.join(sorted(x for x in scenario.package_names if x)) or 'Multiple packages',
        'review_cycle': self.settings.default_review_cycle,
        'version': self._normalize_version(version),
        'document_id': scenario.document_id or f'KEDB-{scenario.priority}-0000',
    }
    related = [
        f"Primary runbook: {self._artifact_filename('RB', object_name, scenario.priority, version)}",
        f"Catalog objects: {', '.join(sorted(scenario.affected_interfaces)[:10]) or 'None detected'}",
        f'Updated at: {self._today_iso()}',
        'Owner: IntegrationTeam',
        'Notes: Expanded official document links with SAP Help.',
    ]
    if scenario.source_catalog_ids:
        related.insert(1, f"Enterprise catalog IDs: {', '.join(sorted(scenario.source_catalog_ids)[:8])}")
    diagnosis_signals = list(scenario.diagnosis)
    diagnosis_signals.extend(self._strip_bullet_prefix(x) for x in scenario.runtime_evidence[:4])
    sections = {
        'SYMPTOM': [scenario.symptom],
        'ERROR PATTERN': [scenario.taxonomy],
        'ROOT CAUSE': scenario.root_causes,
        'DIAGNOSIS SIGNALS': diagnosis_signals,
        'RESOLUTION': scenario.resolution,
        'VALIDATION': scenario.validation,
        'WORKAROUND': [scenario.workaround],
        'RELATED ARTIFACTS': related,
    }
    sections = self._refine_sections_with_policy(artifact_type='kedb', title=scenario.title, metadata=metadata, sections=sections)
    return self._render_kedb_from_sections(scenario.title, metadata, sections)


def _kgs_render_runbook_v217(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    source_kedb_id = self._compact_kedb_reference(scenario.document_id)
    rb_numeric = re.search(r'(\d{4})$', scenario.document_id or '')
    metadata = {
        'environment': self.settings.default_environment,
        'customer_id': self.settings.default_customer_id,
        'system_id': self.settings.default_system_id,
        'sap_sid': self.settings.default_sap_sid,
        'artifact_type': 'runbook',
        'object_name': object_name,
        'priority': scenario.priority,
        'interface_id': sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE',
        'integration_flow_id': sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else 'MULTI_INTERFACE',
        'integration_flow_name': sorted(scenario.flow_names)[0] if scenario.flow_names else 'Multiple interfaces',
        'package_name': ', '.join(sorted(x for x in scenario.package_names if x)) or 'Multiple packages',
        'review_cycle': self.settings.default_review_cycle,
        'version': self._normalize_version(version),
        'document_id': f"RB-{scenario.priority}-{rb_numeric.group(1) if rb_numeric else '0000'}",
    }
    sections = {
        'PURPOSE': [f'This runbook supports incident triage, diagnosis, containment, recovery, and post-fix validation for the KEDB scenario **{object_name}**. It is intended for SAP CPI operations and RAG-based incident guidance.'],
        'BUSINESS CONTEXT': [
            'Business process: Scenario-dependent CPI integration processing',
            f'Description: Primary reference interface is **{sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE"}**. The same error family may also affect other interfaces listed in the affected-interface set.',
            'Message direction: scenario-dependent',
            f'Business criticality: {self._criticality_from_priority(scenario.priority)}',
            f'Impact: {scenario.symptom}',
            f'Affected interfaces count: {len(scenario.affected_interfaces)}',
            f'Representative affected interfaces: {", ".join(sorted(scenario.affected_interfaces)[:5]) or "MULTI_INTERFACE"}',
        ],
        'TECHNICAL LANDSCAPE': [
            f'Package: {", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages"}',
            f'Integration flow ID: {sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE"}',
            f'Integration flow name: {sorted(scenario.flow_names)[0] if scenario.flow_names else "Multiple interfaces"}',
            f'Processing component: {scenario.component}',
            f'Protocol family: {scenario.protocol_family}',
            f'Error pattern: {scenario.taxonomy}',
            'System type: cpi',
            f'Source KEDB ID(s): {source_kedb_id}',
        ],
        'MONITORING AND MPL EVIDENCE': [
            'No directly matching MPL sample was found in the provided export. The runbook is grounded mainly in the KEDB taxonomy and should be enriched further when additional MPL samples become available.' if not scenario.runtime_evidence else f'Observed failed MPL messages for this family: {scenario.occurrence_count}',
            *([f'Sample {idx + 1}: {self._strip_bullet_prefix(sample)}' for idx, sample in enumerate(scenario.runtime_evidence[:3])] or ['Sample 1: No directly matching MPL example available in the provided export.']),
        ],
        'ERROR SIGNATURE': [
            f'Title: {scenario.title}',
            f'Short symptom: {scenario.symptom}',
            f'Normalized object name: {object_name}',
        ],
        'KNOWN ROOT CAUSES': scenario.root_causes,
        'PREREQUISITES FOR INVESTIGATION': [
            'Access to SAP CPI Monitor / MPL and trace where applicable.',
            f'Access to the owning package **{", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages"}** and the interface **{sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "MULTI_INTERFACE"}**.',
            'Deployment/runtime version reference and recent transport/deployment history.',
            'Security material and endpoint configuration access when authentication, connectivity, or certificate topics are involved.',
            'Representative failing payload or reproducible test message where available.',
        ],
        'DIAGNOSIS STEPS': scenario.diagnosis,
        'RECOVERY STEPS': [
            'Contain the incident and preserve reproducible evidence before changing configuration.',
            f'Contain noise, document the pattern, and keep the scenario stable enough to capture trace and reproducible evidence. Apply the documented workaround where appropriate: {scenario.workaround}',
            *scenario.resolution,
            f'Create a {scenario.priority} incident when the issue is business-visible, recurrent, or affects productive test execution; otherwise log a tracked support ticket and notify the interface owner with the failing evidence.',
            'Apply permanent hardening after the incident is stabilized.',
            'Rollback options:',
            'Revert the latest change that amplified the condition if applicable.',
            'Pause replay if the receiver or downstream system continues to fail under the same signature.',
        ],
        'ESCALATION CRITERIA': [
            'Support owner: IntegrationTeam',
            'Service owner: RCMO Integration Service Owner',
            'Escalation group: RCMO-CPI-L2',
            'When to escalate: Escalate when the issue is reproducible, business impact expands, or the scenario cannot be stabilized within normal operational handling.',
            'Evidence required: MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.',
        ],
        'POST-FIX VALIDATION': [
            *scenario.validation,
            'Verify that MPL does not show the same signature repeatedly in the immediate post-fix monitoring window.',
            'Reprocessing possible: yes, after the failing condition is understood and stabilized.',
            'Method: Replay only one controlled test message first, then expand to backlog processing if validation succeeds.',
            'Retry pattern: Avoid blind mass replay; use sequenced replay with MPL observation.',
        ],
    }
    sections = self._refine_sections_with_policy(artifact_type='runbook', title=scenario.title, metadata=metadata, sections=sections)
    return self._render_runbook_from_sections(scenario.title, metadata, sections)


KnowledgeGenerationService._render_structured_markdown = _kgs_render_structured_markdown_v217
KnowledgeGenerationService._parse_markdown_sections = _kgs_parse_markdown_sections_v217
KnowledgeGenerationService._normalize_metadata = _kgs_normalize_metadata_v217
KnowledgeGenerationService._render_kedb_from_sections = _kgs_render_kedb_from_sections_v217
KnowledgeGenerationService._render_runbook_from_sections = _kgs_render_runbook_from_sections_v217
KnowledgeGenerationService._render_kedb = _kgs_render_kedb_v217
KnowledgeGenerationService._render_runbook = _kgs_render_runbook_v217

# -----------------------------------------------------------------------------
# v2.1.9 patch layer
# -----------------------------------------------------------------------------
_current_kgs_init_v219 = KnowledgeGenerationService.__init__
_current_kgs_derive_scenarios_v219 = KnowledgeGenerationService._derive_scenarios
_current_kgs_render_kedb_v219 = KnowledgeGenerationService._render_kedb
_current_kgs_render_runbook_v219 = KnowledgeGenerationService._render_runbook
_current_kgs_update_kedb_v219 = KnowledgeGenerationService.update_kedb_documents
_current_kgs_update_runbook_v219 = KnowledgeGenerationService.update_runbook_documents
_current_kgs_maybe_refine_with_openai_v219 = KnowledgeGenerationService._maybe_refine_with_openai


def _kgs_init_v219(self, *args, **kwargs):
    _current_kgs_init_v219(self, *args, **kwargs)
    self._v219_interface_catalog_index_cache = None
    self._v219_design_inventory_cache = None
    self._v219_mpl_records_cache = None
    self._v219_policy_bundle_cache = None
    self._v219_sample_bundle_cache = None


def _kgs_v219_reference_root(self) -> Path:
    return self.project_root / "resources" / "reference_materials"


def _kgs_v219_policies_root(self) -> Path:
    return self.project_root / "resources" / "policies"


def _kgs_v219_read_text(self, path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    text = text.replace("\x00", "").strip()
    return text[:limit] if limit and limit > 0 else text


def _kgs_v219_load_policy_bundle(self) -> dict[str, str]:
    if self._v219_policy_bundle_cache is not None:
        return self._v219_policy_bundle_cache
    policies = {
        "primary": self._v219_read_text(self._v219_policies_root() / "AI4BIZ_Knowledge_Ingestion_Guide.txt", 5000),
        "bm25": self._v219_read_text(self._v219_policies_root() / "BM25_Runbook_Authoring_Guideline.txt", 5000),
        "schema": self._v219_read_text(self._v219_policies_root() / "knowledge_schema_standard.md", 3000),
    }
    self._v219_policy_bundle_cache = policies
    return policies


def _kgs_v219_load_sample_bundle(self) -> dict[str, str]:
    if self._v219_sample_bundle_cache is not None:
        return self._v219_sample_bundle_cache
    root = self._v219_reference_root() / "additional_samples"
    bundle = {
        "kedb_model": self._v219_read_text(root / "NEW_MODEL_KB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md", 5000),
        "runbook_model": self._v219_read_text(root / "NEW_MODEL_RB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md", 7000),
        "remediation": self._v219_read_text(root / "AI4BIZ_Remediation_Package_Strict_Ingestion_V1.txt", 3000),
    }
    self._v219_sample_bundle_cache = bundle
    return bundle


def _kgs_v219_load_interface_catalog_index(self) -> dict[str, dict[str, Any]]:
    if self._v219_interface_catalog_index_cache is not None:
        return self._v219_interface_catalog_index_cache
    index: dict[str, dict[str, Any]] = {}
    roots = [
        self.project_root / "resources" / "examples" / "interface_catalog_docs",
        self.project_root / "exports" / "knowledge" / "interface_catalogs" / "v1",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("DOC_*.md")):
            try:
                parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            metadata = parsed.get("metadata", {})
            sections = parsed.get("sections", {})
            entry = {
                "path": str(path),
                "title": parsed.get("title") or "",
                "document_id": parsed.get("document_id") or "",
                "metadata": metadata,
                "sections": sections,
                "scope_excerpt": " | ".join(self._strip_bullet_prefix(x) for x in (sections.get("2. SCOPE") or [])[:4]),
                "core_excerpt": " | ".join(self._strip_bullet_prefix(x) for x in (sections.get("4. CORE EXPLANATION") or [])[:4]),
            }
            keys = {
                metadata.get("interface_id", ""),
                metadata.get("integration_flow_id", ""),
                metadata.get("integration_flow_name", ""),
                metadata.get("object_name", ""),
                parsed.get("title", ""),
            }
            for key in keys:
                if not key:
                    continue
                norm = self._normalize_object_name(str(key))
                if norm and norm not in index:
                    index[norm] = entry
    self._v219_interface_catalog_index_cache = index
    return index


def _kgs_v219_flatten_records(self, data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("d"), dict) and isinstance(data["d"].get("results"), list):
            return [x for x in data["d"]["results"] if isinstance(x, dict)]
        if isinstance(data.get("value"), list):
            return [x for x in data["value"] if isinstance(x, dict)]
        for key in ("records", "MessageErrors", "MessageProcessingLogs", "items", "packages"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
        return [data]
    return []


def _kgs_v219_load_design_inventory_index(self) -> dict[str, Any]:
    if self._v219_design_inventory_cache is not None:
        return self._v219_design_inventory_cache
    root = self._v219_reference_root() / "sap-ci-design-and-configuration-inventory"
    package_map: dict[str, dict[str, str]] = {}
    iflow_map: dict[str, dict[str, str]] = {}

    def add_package(pkg_id: str, name: str, short_text: str = "") -> None:
        if not pkg_id:
            return
        package_map[pkg_id] = {
            "package_id": pkg_id,
            "package_name": name or pkg_id,
            "short_text": short_text,
        }

    def add_iflow(record: dict[str, Any]) -> None:
        iflow_id = str(record.get("Id") or record.get("iflow_id") or record.get("interface_id") or "").strip()
        iflow_name = str(record.get("Name") or record.get("integration_flow_name") or record.get("name") or iflow_id).strip()
        package_id = str(record.get("PackageId") or record.get("package_id") or record.get("Package") or "").strip()
        package_name = str(record.get("PackageName") or record.get("package_name") or "").strip()
        if package_id and package_id in package_map and not package_name:
            package_name = package_map[package_id].get("package_name", package_id)
        item = {
            "iflow_id": iflow_id or iflow_name,
            "iflow_name": iflow_name or iflow_id,
            "integration_flow_id": iflow_id or iflow_name,
            "integration_flow_name": iflow_name or iflow_id,
            "package_id": package_id,
            "package_name": package_name or package_id or "Unknown Package",
        }
        for key in {iflow_id, iflow_name, self._normalize_object_name(iflow_id), self._normalize_object_name(iflow_name)}:
            if key:
                iflow_map[str(key)] = item

    for path in sorted(root.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        records = self._v219_flatten_records(payload)
        name = path.name.lower()
        if name == "available_packages_and_iflows.json":
            for rec in records:
                add_package(str(rec.get("package_id") or "").strip(), str(rec.get("name") or "").strip(), str(rec.get("short_text") or "").strip())
            continue
        if name == "packages.json":
            for rec in records:
                add_package(str(rec.get("Id") or rec.get("package_id") or "").strip(), str(rec.get("Name") or rec.get("name") or "").strip(), str(rec.get("ShortText") or rec.get("short_text") or "").strip())
            continue
        if name == "iflows.json":
            for rec in records:
                add_iflow(rec)

    cache = {"package_map": package_map, "iflow_map": iflow_map}
    self._v219_design_inventory_cache = cache
    return cache


def _kgs_v219_complete_metadata(self, metadata: dict[str, str], *, artifact_type: str) -> dict[str, str]:
    normalized = dict(metadata)
    if artifact_type in {"kedb", "runbook"}:
        normalized["object_name"] = self._canonical_object_name(normalized.get("object_name") or "UNKNOWN_OBJECT")
    normalized.setdefault("environment", self.settings.default_environment)
    normalized.setdefault("customer_id", self.settings.default_customer_id)
    normalized.setdefault("system_id", self.settings.default_system_id)
    normalized.setdefault("sap_sid", self.settings.default_sap_sid)
    normalized.setdefault("artifact_type", artifact_type)
    normalized.setdefault("priority", "P3")
    normalized.setdefault("review_cycle", self.settings.default_review_cycle)
    normalized.setdefault("version", self._normalize_version(normalized.get("version") or "v1"))

    interface_index = self._v219_load_interface_catalog_index()
    inventory = self._v219_load_design_inventory_index()
    candidates = [
        normalized.get("interface_id", ""),
        normalized.get("integration_flow_id", ""),
        normalized.get("integration_flow_name", ""),
        normalized.get("object_name", ""),
    ]
    resolved_interface: dict[str, Any] | None = None
    for candidate in candidates:
        norm = self._normalize_object_name(str(candidate or ""))
        if not norm:
            continue
        entry = interface_index.get(norm)
        if entry:
            resolved_interface = entry
            break
    if resolved_interface is None:
        for candidate in candidates:
            norm = self._normalize_object_name(str(candidate or ""))
            if not norm:
                continue
            entry = inventory["iflow_map"].get(candidate) or inventory["iflow_map"].get(norm)
            if entry:
                resolved_interface = {"metadata": {
                    "interface_id": entry.get("iflow_name") or entry.get("iflow_id"),
                    "integration_flow_id": entry.get("iflow_id") or entry.get("iflow_name"),
                    "integration_flow_name": entry.get("iflow_name") or entry.get("iflow_id"),
                    "package_name": entry.get("package_name") or entry.get("package_id") or "Unknown Package",
                }, "document_id": ""}
                break
    if resolved_interface:
        meta = resolved_interface.get("metadata", {})
        if normalized.get("interface_id") in {None, "", "UNKNOWN_INTERFACE", "MULTI_INTERFACE"}:
            normalized["interface_id"] = str(meta.get("interface_id") or meta.get("integration_flow_name") or meta.get("integration_flow_id") or normalized.get("interface_id") or "UNKNOWN_INTERFACE")
        if normalized.get("integration_flow_id") in {None, "", "UNKNOWN_INTERFACE", "MULTI_INTERFACE"}:
            normalized["integration_flow_id"] = str(meta.get("integration_flow_id") or meta.get("interface_id") or normalized.get("integration_flow_id") or "UNKNOWN_INTERFACE")
        if normalized.get("integration_flow_name") in {None, "", "UNKNOWN_INTERFACE", "MULTI_INTERFACE", "Multiple interfaces"}:
            normalized["integration_flow_name"] = str(meta.get("integration_flow_name") or meta.get("interface_id") or normalized.get("integration_flow_name") or "UNKNOWN_INTERFACE")
        if normalized.get("package_name") in {None, "", "Multiple packages", "Unknown Package"}:
            normalized["package_name"] = str(meta.get("package_name") or normalized.get("package_name") or "Unknown Package")
    if normalized.get("package_name") in {None, "", "Unknown Package"}:
        normalized["package_name"] = "Multiple packages"
    return normalized


def _kgs_v219_match_interface_context(self, *, metadata: dict[str, str] | None = None, scenario: ScenarioFamily | None = None) -> dict[str, Any]:
    interface_index = self._v219_load_interface_catalog_index()
    inventory = self._v219_load_design_inventory_index()
    candidates: list[str] = []
    if scenario is not None:
        candidates.extend(sorted(scenario.affected_interfaces))
        candidates.extend(sorted(scenario.flow_names))
        candidates.append(f"{self.settings.default_sap_sid}_{scenario.code}")
    if metadata:
        candidates.extend([
            str(metadata.get("interface_id") or ""),
            str(metadata.get("integration_flow_id") or ""),
            str(metadata.get("integration_flow_name") or ""),
            str(metadata.get("object_name") or ""),
        ])
    for candidate in candidates:
        norm = self._normalize_object_name(candidate)
        if not norm:
            continue
        if norm in interface_index:
            entry = interface_index[norm]
            sections = entry.get("sections", {})
            return {
                "document_id": entry.get("document_id") or "",
                "interface_id": str(entry.get("metadata", {}).get("interface_id") or entry.get("metadata", {}).get("integration_flow_name") or candidate),
                "integration_flow_id": str(entry.get("metadata", {}).get("integration_flow_id") or entry.get("metadata", {}).get("interface_id") or candidate),
                "integration_flow_name": str(entry.get("metadata", {}).get("integration_flow_name") or entry.get("metadata", {}).get("interface_id") or candidate),
                "package_name": str(entry.get("metadata", {}).get("package_name") or "Multiple packages"),
                "scope_excerpt": entry.get("scope_excerpt") or "",
                "core_excerpt": entry.get("core_excerpt") or "",
                "key_terms": [self._strip_bullet_prefix(x) for x in (sections.get("3. KEY TERMS") or [])[:8]],
            }
        inv = inventory["iflow_map"].get(candidate) or inventory["iflow_map"].get(norm)
        if inv:
            return {
                "document_id": "",
                "interface_id": str(inv.get("iflow_name") or inv.get("iflow_id") or candidate),
                "integration_flow_id": str(inv.get("iflow_id") or inv.get("iflow_name") or candidate),
                "integration_flow_name": str(inv.get("iflow_name") or inv.get("iflow_id") or candidate),
                "package_name": str(inv.get("package_name") or inv.get("package_id") or "Multiple packages"),
                "scope_excerpt": "",
                "core_excerpt": "",
                "key_terms": [],
            }
    return {
        "document_id": "",
        "interface_id": metadata.get("interface_id", "UNKNOWN_INTERFACE") if metadata else "UNKNOWN_INTERFACE",
        "integration_flow_id": metadata.get("integration_flow_id", "UNKNOWN_INTERFACE") if metadata else "UNKNOWN_INTERFACE",
        "integration_flow_name": metadata.get("integration_flow_name", "UNKNOWN_INTERFACE") if metadata else "UNKNOWN_INTERFACE",
        "package_name": metadata.get("package_name", "Multiple packages") if metadata else "Multiple packages",
        "scope_excerpt": "",
        "core_excerpt": "",
        "key_terms": [],
    }


def _kgs_v219_load_mpl_records(self) -> list[dict[str, str]]:
    if self._v219_mpl_records_cache is not None:
        return self._v219_mpl_records_cache
    paths: list[Path] = []
    mpl_root = self._v219_reference_root() / "mpl"
    if mpl_root.exists():
        paths.extend(sorted(mpl_root.rglob("*.json")))
    inv_mpl = self._v219_reference_root() / "sap-ci-design-and-configuration-inventory" / "Message_Processing_Logs.json"
    if inv_mpl.exists():
        paths.append(inv_mpl)
    records: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for rec in self._v219_flatten_records(payload):
            status = str(rec.get("Status") or rec.get("status") or "FAILED").upper()
            if status != "FAILED":
                continue
            error_text = self.mpl_semantic_service._clean_error_text(str(rec.get("ErrorMessage") or rec.get("localizedText") or rec.get("error_text") or rec.get("ErrorDetails") or ""))
            if not error_text:
                continue
            guid = str(rec.get("MessageGuid") or rec.get("messageID") or rec.get("message_guid") or "UNKNOWN_MESSAGE_GUID")
            dedupe_key = (guid, error_text)
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            records.append({
                "message_guid": guid,
                "iflow_name": str(rec.get("IntegrationFlowName") or rec.get("interface") or rec.get("iflow_id") or "UNKNOWN_IFLOW"),
                "timestamp": str(rec.get("LogStart") or rec.get("timeStamp") or rec.get("LogEnd") or ""),
                "sender": str(rec.get("Sender") or rec.get("sender") or ""),
                "receiver": str(rec.get("Receiver") or rec.get("receiver") or ""),
                "error_text": error_text,
                "normalized_code": self.mpl_semantic_service._normalized_code_from_error_text(error_text),
                "taxonomy": self.mpl_semantic_service._taxonomy_from_error_text(error_text),
            })
    records.sort(key=lambda x: (x.get("timestamp") or "", x.get("message_guid") or ""), reverse=True)
    self._v219_mpl_records_cache = records
    return records


def _kgs_v219_collect_mpl_evidence(self, *, metadata: dict[str, str] | None = None, scenario: ScenarioFamily | None = None, limit: int = 3) -> list[dict[str, str]]:
    records = self._v219_load_mpl_records()
    code = scenario.code if scenario is not None else ""
    taxonomy = scenario.taxonomy if scenario is not None else ""
    candidates = set()
    if metadata:
        candidates.update({str(metadata.get("interface_id") or ""), str(metadata.get("integration_flow_id") or ""), str(metadata.get("integration_flow_name") or "")})
    if scenario is not None:
        candidates.update(scenario.affected_interfaces)
        candidates.update(scenario.flow_names)
    norm_candidates = {self._normalize_object_name(x) for x in candidates if x}
    scored: list[tuple[int, dict[str, str]]] = []
    for rec in records:
        score = 0
        if code and rec.get("normalized_code") == code:
            score += 8
        if taxonomy and rec.get("taxonomy") == taxonomy:
            score += 4
        if self._normalize_object_name(rec.get("iflow_name", "")) in norm_candidates:
            score += 5
        if scenario and any(token in rec.get("error_text", "").upper() for token in scenario.code.split("_")[:3] if len(token) > 3):
            score += 2
        if score > 0:
            scored.append((score, rec))
    scored.sort(key=lambda item: (item[0], item[1].get("timestamp") or ""), reverse=True)
    results: list[dict[str, str]] = []
    seen_guids: set[str] = set()
    for _, rec in scored:
        guid = rec.get("message_guid") or ""
        if guid in seen_guids:
            continue
        seen_guids.add(guid)
        results.append(rec)
        if len(results) >= limit:
            break
    return results


def _kgs_v219_format_mpl_evidence_line(self, record: dict[str, str], *, prefix: str = "Sample") -> str:
    timestamp = record.get("timestamp") or "unknown time"
    guid = record.get("message_guid") or "unknown-guid"
    iflow = record.get("iflow_name") or "UNKNOWN_IFLOW"
    sender = record.get("sender") or "n/a"
    receiver = record.get("receiver") or "n/a"
    error_text = self._shorten(record.get("error_text") or "", 280)
    return f"{prefix}: {timestamp} | MessageGuid {guid} | Interface {iflow} | Sender {sender} | Receiver {receiver} | Error: {error_text}"


def _kgs_v219_analysis_from_interface_catalog(self, iflow_id: str, item: dict[str, Any]) -> dict[str, Any]:
    context = self._v219_match_interface_context(metadata={
        "interface_id": str(item.get("Name") or iflow_id),
        "integration_flow_id": str(item.get("Id") or iflow_id),
        "integration_flow_name": str(item.get("Name") or iflow_id),
        "package_name": str(item.get("PackageName") or self._resolve_package_name(item) or "Multiple packages"),
        "object_name": self._normalize_object_name(str(item.get("Name") or iflow_id)),
    })
    key_terms = [x.upper() for x in context.get("key_terms", [])]
    protocols = []
    for proto in ("HTTP", "HTTPS", "ODATA", "SOAP", "SFTP", "MAIL", "JDBC"):
        if any(proto in term for term in key_terms):
            protocols.append(proto)
    auth = []
    for token in ("BASIC", "OAUTH", "CLIENT", "CERTIFICATE", "PGP"):
        if any(token in term for term in key_terms):
            auth.append(token)
    return {
        "summary": context.get("core_excerpt") or context.get("scope_excerpt") or f"Local catalog-only analysis for {iflow_id}.",
        "sender_systems": [],
        "receiver_systems": [],
        "protocols": protocols,
        "authentication": auth,
        "dependencies": context.get("key_terms", []),
    }


def _kgs_derive_scenarios_v219(self, package_id: str | None = None, iflow_ids: list[str] | None = None, use_mpl: bool = True, mpl_hours: int | None = None, mpl_limit: int | None = None):
    async def inner():
        scenarios: dict[str, ScenarioFamily] = {}
        iflows = await self._collect_iflows(package_id=package_id, iflow_ids=iflow_ids)
        iflows_by_id: dict[str, dict[str, Any]] = {str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW"): item for item in iflows}
        for item in iflows:
            iflow_id = str(item.get("Id") or item.get("iflow_id") or "UNKNOWN_IFLOW")
            try:
                artifact = await self.sap_client.get_iflow_content(iflow_id=iflow_id)
                analysis = self.iflow_parser.parse(artifact)
            except Exception:
                analysis = self._v219_analysis_from_interface_catalog(iflow_id, item)
            flow_name = str(item.get("Name") or iflow_id)
            package_name = self._resolve_package_name(item)
            for scenario in self._candidate_scenarios(analysis):
                family = scenarios.setdefault(scenario.code, scenario)
                family.affected_interfaces.add(flow_name)
                family.flow_names.add(flow_name)
                family.package_names.add(package_name)
        self._merge_enterprise_catalog_into_scenarios(scenarios=scenarios, iflows_by_id=iflows_by_id, iflow_ids=iflow_ids)
        if use_mpl:
            local_mpl_dir = self._resolve_local_mpl_dir()
            signals = await self.mpl_semantic_service.collect_failure_signals(
                hours_back=mpl_hours or self.settings.mpl_default_lookback_hours,
                limit=mpl_limit or self.settings.mpl_default_limit,
                local_json_dir=str(local_mpl_dir) if local_mpl_dir else None,
            )
            summary = self.mpl_semantic_service.summarize_signals(signals)
            self._merge_mpl_summary_into_scenarios(scenarios=scenarios, mpl_summary=summary, iflows_by_id=iflows_by_id)
        # Final hardening from local inventory and MPL evidence
        for scenario in scenarios.values():
            context = self._v219_match_interface_context(scenario=scenario)
            if context.get("interface_id"):
                scenario.affected_interfaces.add(str(context.get("interface_id")))
            if context.get("integration_flow_name"):
                scenario.flow_names.add(str(context.get("integration_flow_name")))
            if context.get("package_name"):
                scenario.package_names.add(str(context.get("package_name")))
            mpl_matches = self._v219_collect_mpl_evidence(scenario=scenario, limit=3)
            for rec in mpl_matches:
                line = self._v219_format_mpl_evidence_line(rec, prefix="MPL sample")
                if line not in scenario.runtime_evidence:
                    scenario.runtime_evidence.append(line)
                err = rec.get("error_text") or ""
                if err and err not in scenario.example_error_messages:
                    scenario.example_error_messages.append(err)
            if mpl_matches:
                scenario.last_seen = mpl_matches[0].get("timestamp") or scenario.last_seen
                if scenario.occurrence_count < len(mpl_matches):
                    scenario.occurrence_count = len(mpl_matches)
        return scenarios
    return inner()


def _kgs_v219_professional_symptom(self, scenario: ScenarioFamily, evidence: list[dict[str, str]]) -> str:
    symptom = self._sentence_case((scenario.symptom or "").strip())
    if evidence:
        text = evidence[0].get("error_text") or ""
        if text and (not symptom or symptom.lower().startswith("runtime failure") or len(symptom) < 20):
            symptom = self._shorten(text, 170)
    return symptom or self._humanize_object_name(scenario.code)


def _kgs_render_kedb_v219(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    context = self._v219_match_interface_context(scenario=scenario)
    metadata = self._v219_complete_metadata({
        "environment": self.settings.default_environment,
        "customer_id": self.settings.default_customer_id,
        "system_id": self.settings.default_system_id,
        "sap_sid": self.settings.default_sap_sid,
        "artifact_type": "kedb",
        "object_name": object_name,
        "priority": scenario.priority,
        "interface_id": context.get("interface_id") or (sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "UNKNOWN_INTERFACE"),
        "integration_flow_id": context.get("integration_flow_id") or (sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "UNKNOWN_INTERFACE"),
        "integration_flow_name": context.get("integration_flow_name") or (sorted(scenario.flow_names)[0] if scenario.flow_names else "UNKNOWN_INTERFACE"),
        "package_name": context.get("package_name") or (", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages"),
        "review_cycle": self.settings.default_review_cycle,
        "version": self._normalize_version(version),
        "document_id": scenario.document_id or f"KEDB-{scenario.priority}-0000",
    }, artifact_type="kedb")
    evidence = self._v219_collect_mpl_evidence(metadata=metadata, scenario=scenario, limit=2)
    related = [
        f"Primary runbook: {self._artifact_filename('RB', object_name, scenario.priority, version)}",
    ]
    if context.get("document_id"):
        related.append(f"Catalog objects: {context['document_id']}")
    related.extend([
        f"Updated at: {scenario.last_seen or self._today_iso()}",
        "Owner: IntegrationTeam",
        f"Notes: Taxonomy normalized to 4-level pattern {scenario.taxonomy} for stricter RAG retrieval.",
    ])
    diagnosis_signals = list(scenario.diagnosis)
    for rec in evidence:
        diagnosis_signals.append(self._v219_format_mpl_evidence_line(rec, prefix="Evidence"))
    sections = {
        "SYMPTOM": [self._v219_professional_symptom(scenario, evidence)],
        "ERROR PATTERN": [scenario.taxonomy],
        "ROOT CAUSE": scenario.root_causes,
        "DIAGNOSIS SIGNALS": diagnosis_signals,
        "RESOLUTION": scenario.resolution,
        "VALIDATION": scenario.validation,
        "WORKAROUND": [scenario.workaround],
        "RELATED ARTIFACTS": related,
    }
    sections = self._refine_sections_with_policy(artifact_type="kedb", title=scenario.title, metadata=metadata, sections=sections)
    return self._render_kedb_from_sections(scenario.title, metadata, sections)


def _kgs_render_runbook_v219(self, scenario: ScenarioFamily, version: str) -> str:
    object_name = self._canonical_object_name(scenario.code)
    context = self._v219_match_interface_context(scenario=scenario)
    source_kedb_id = self._compact_kedb_reference(scenario.document_id)
    rb_numeric = re.search(r"(\d{4})$", scenario.document_id or "")
    metadata = self._v219_complete_metadata({
        "environment": self.settings.default_environment,
        "customer_id": self.settings.default_customer_id,
        "system_id": self.settings.default_system_id,
        "sap_sid": self.settings.default_sap_sid,
        "artifact_type": "runbook",
        "object_name": object_name,
        "priority": scenario.priority,
        "interface_id": context.get("interface_id") or (sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "UNKNOWN_INTERFACE"),
        "integration_flow_id": context.get("integration_flow_id") or (sorted(scenario.affected_interfaces)[0] if scenario.affected_interfaces else "UNKNOWN_INTERFACE"),
        "integration_flow_name": context.get("integration_flow_name") or (sorted(scenario.flow_names)[0] if scenario.flow_names else "UNKNOWN_INTERFACE"),
        "package_name": context.get("package_name") or (", ".join(sorted(x for x in scenario.package_names if x)) or "Multiple packages"),
        "review_cycle": self.settings.default_review_cycle,
        "version": self._normalize_version(version),
        "document_id": f"RB-{scenario.priority}-{rb_numeric.group(1) if rb_numeric else '0000'}",
    }, artifact_type="runbook")
    evidence = self._v219_collect_mpl_evidence(metadata=metadata, scenario=scenario, limit=3)
    monitoring_lines = []
    if evidence:
        monitoring_lines.append(f"Observed failed MPL messages for this family: {max(scenario.occurrence_count, len(evidence))}")
        for idx, rec in enumerate(evidence, start=1):
            monitoring_lines.append(self._v219_format_mpl_evidence_line(rec, prefix=f"Sample {idx}"))
    else:
        monitoring_lines.append("No directly matching MPL sample was found in the provided export. The runbook is grounded mainly in the KEDB taxonomy and should be enriched further when additional MPL samples become available.")
        monitoring_lines.append("Sample 1: No directly matching MPL example available in the provided export.")
    sections = {
        "PURPOSE": [f"This runbook supports incident triage, diagnosis, containment, recovery, and post-fix validation for the KEDB scenario **{object_name}**. It is intended for SAP CPI operations and RAG-based incident guidance."],
        "BUSINESS CONTEXT": [
            "Business process: Scenario-dependent CPI integration processing",
            f"Description: Primary reference interface is **{metadata['interface_id']}**. The same error family may also affect other interfaces listed in the affected-interface set.",
            "Message direction: scenario-dependent",
            f"Business criticality: {self._criticality_from_priority(scenario.priority)}",
            f"Impact: {self._v219_professional_symptom(scenario, evidence)}",
            f"Affected interfaces count: {len(scenario.affected_interfaces) or 1}",
            f"Representative affected interfaces: {', '.join(sorted(scenario.affected_interfaces)[:5]) or metadata['interface_id']}",
        ],
        "TECHNICAL LANDSCAPE": [
            f"Package: {metadata['package_name']}",
            f"Integration flow ID: {metadata['integration_flow_id']}",
            f"Integration flow name: {metadata['integration_flow_name']}",
            f"Processing component: {scenario.component}",
            f"Protocol family: {scenario.protocol_family}",
            f"Error pattern: {scenario.taxonomy}",
            "System type: cpi",
            f"Source KEDB ID(s): {source_kedb_id}",
        ],
        "MONITORING AND MPL EVIDENCE": monitoring_lines,
        "ERROR SIGNATURE": [
            f"Title: {scenario.title}",
            f"Short symptom: {self._v219_professional_symptom(scenario, evidence)}",
            f"Normalized object name: {object_name}",
        ],
        "KNOWN ROOT CAUSES": scenario.root_causes,
        "PREREQUISITES FOR INVESTIGATION": [
            "Access to SAP CPI Monitor / MPL and trace where applicable.",
            f"Access to the owning package **{metadata['package_name']}** and the interface **{metadata['interface_id']}**.",
            "Deployment/runtime version reference and recent transport/deployment history.",
            "Security material and endpoint configuration access when authentication, connectivity, or certificate topics are involved.",
            "Representative failing payload or reproducible test message where available.",
        ],
        "DIAGNOSIS STEPS": scenario.diagnosis,
        "RECOVERY STEPS": [
            "Contain the incident and preserve reproducible evidence before changing configuration.",
            f"Contain noise, document the pattern, and keep the scenario stable enough to capture trace and reproducible evidence. Apply the documented workaround where appropriate: {scenario.workaround}",
            *scenario.resolution,
            f"Create a {scenario.priority} incident when the issue is business-visible, recurrent, or affects productive test execution; otherwise log a tracked support ticket and notify the interface owner with the failing evidence.",
            "Apply permanent hardening after the incident is stabilized.",
            "Rollback options:",
            "Revert the latest change that amplified the condition if applicable.",
            "Pause replay if the receiver or downstream system continues to fail under the same signature.",
        ],
        "ESCALATION CRITERIA": [
            "Support owner: IntegrationTeam",
            "Service owner: RCMO Integration Service Owner",
            "Escalation group: RCMO-CPI-L2",
            "When to escalate: Escalate when the issue is reproducible, business impact expands, or the scenario cannot be stabilized within normal operational handling.",
            "Evidence required: MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.",
        ],
        "POST-FIX VALIDATION": [
            *scenario.validation,
            "Verify that MPL does not show the same signature repeatedly in the immediate post-fix monitoring window.",
            "Reprocessing possible: yes, after the failing condition is understood and stabilized.",
            "Method: Replay only one controlled test message first, then expand to backlog processing if validation succeeds.",
            "Retry pattern: Avoid blind mass replay; use sequenced replay with MPL observation.",
        ],
    }
    sections = self._refine_sections_with_policy(artifact_type="runbook", title=scenario.title, metadata=metadata, sections=sections)
    return self._render_runbook_from_sections(scenario.title, metadata, sections)


def _kgs_update_kedb_documents_v219(self, version: str, source_dir: str | None = None, source_zip_path: str | None = None, output_dir: str | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    source_path = self._resolve_markdown_source(artifact_type="kedb", source_dir=source_dir, source_zip_path=source_zip_path)
    target_dir = self._resolve_output_dir(output_dir, "kedb_updated", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for path in sorted(source_path.glob("*.md")):
        parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
        metadata = self._v219_complete_metadata(self._normalize_metadata(parsed["metadata"], artifact_type="kedb"), artifact_type="kedb")
        metadata["artifact_type"] = "kedb"
        metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
        metadata["object_name"] = self._canonical_object_name(metadata.get("object_name") or self._object_from_filename(path.name))
        metadata["version"] = version
        title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
        metadata["document_id"] = parsed.get("document_id") or f"KEDB-{metadata['priority']}-0000"
        sections = parsed["sections"]
        ordered = {
            "SYMPTOM": sections.get("1. SYMPTOM") or sections.get("SYMPTOM") or ["Symptom requires expert refinement."],
            "ERROR PATTERN": [self._normalize_taxonomy_line(x) for x in (sections.get("2. ERROR PATTERN") or sections.get("ERROR PATTERN") or [f"- {self._taxonomy_from_object_name(metadata['object_name'])}"])],
            "ROOT CAUSE": sections.get("3. ROOT CAUSE") or sections.get("ROOT CAUSE") or ["Root cause needs confirmation from runtime evidence."],
            "DIAGNOSIS SIGNALS": sections.get("4. DIAGNOSIS SIGNALS") or sections.get("DIAGNOSIS SIGNALS") or ["Check MPL and compare failing step against last successful message."],
            "RESOLUTION": sections.get("5. RESOLUTION") or sections.get("RESOLUTION") or ["Apply the least risky corrective change and redeploy."],
            "VALIDATION": sections.get("6. VALIDATION") or sections.get("VALIDATION") or ["Confirm the message completes successfully after the change."],
            "WORKAROUND": sections.get("7. WORKAROUND") or sections.get("WORKAROUND") or ["Escalate if no safe workaround is available."],
            "RELATED ARTIFACTS": sections.get("8. RELATED ARTIFACTS") or sections.get("RELATED ARTIFACTS") or [f"Primary runbook: {self._artifact_filename('RB', metadata['object_name'], metadata['priority'], version)}"],
        }
        for rec in self._v219_collect_mpl_evidence(metadata=metadata, limit=2):
            evidence_line = self._v219_format_mpl_evidence_line(rec, prefix="Evidence")
            if evidence_line not in ordered["DIAGNOSIS SIGNALS"]:
                ordered["DIAGNOSIS SIGNALS"].append(evidence_line)
        context = self._v219_match_interface_context(metadata=metadata)
        if context.get("document_id"):
            ordered["RELATED ARTIFACTS"].append(f"Catalog objects: {context['document_id']}")
        ordered = self._enrich_update_kedb_sections(metadata=metadata, sections=ordered, version=version)
        ordered = self._refine_sections_with_policy(artifact_type="kedb", title=title, metadata=metadata, sections=ordered)
        out_path = target_dir / self._artifact_filename("KB", metadata['object_name'], metadata['priority'], version)
        out_path.write_text(self._render_kedb_from_sections(title, metadata, ordered), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "kedb_update", "version": version, "source_dir": str(source_path), "count": len(files), "updated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


def _kgs_update_runbook_documents_v219(self, version: str, source_dir: str | None = None, source_zip_path: str | None = None, output_dir: str | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    source_path = self._resolve_markdown_source(artifact_type="runbooks", source_dir=source_dir, source_zip_path=source_zip_path)
    target_dir = self._resolve_output_dir(output_dir, "runbooks_updated", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for path in sorted(source_path.glob("*.md")):
        parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
        metadata = self._v219_complete_metadata(self._normalize_metadata(parsed["metadata"], artifact_type="runbook"), artifact_type="runbook")
        metadata["artifact_type"] = "runbook"
        metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
        metadata["object_name"] = self._canonical_object_name(metadata.get("object_name") or self._object_from_filename(path.name))
        metadata["version"] = version
        title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
        metadata["document_id"] = parsed.get("document_id") or f"RB-{metadata['priority']}-0000"
        sections = parsed["sections"]
        ordered = {
            "PURPOSE": sections.get("1. PURPOSE") or sections.get("PURPOSE") or [f"This runbook supports the canonical incident pattern {metadata['object_name']}."],
            "BUSINESS CONTEXT": sections.get("2. BUSINESS CONTEXT") or sections.get("BUSINESS CONTEXT") or ["Business impact requires confirmation from the owning interface team."],
            "TECHNICAL LANDSCAPE": sections.get("3. TECHNICAL LANDSCAPE") or sections.get("TECHNICAL LANDSCAPE") or [f"Package: {metadata['package_name']}"],
            "MONITORING AND MPL EVIDENCE": sections.get("4. MONITORING AND MPL EVIDENCE") or sections.get("MONITORING AND MPL EVIDENCE") or ["Review MPL entries in the affected time window and preserve MessageGuid evidence."],
            "ERROR SIGNATURE": sections.get("5. ERROR SIGNATURE") or sections.get("ERROR SIGNATURE") or [f"Normalized object name: {metadata['object_name']}"],
            "KNOWN ROOT CAUSES": sections.get("6. KNOWN ROOT CAUSES") or sections.get("KNOWN ROOT CAUSES") or ["Root cause requires technical verification."],
            "PREREQUISITES FOR INVESTIGATION": sections.get("7. PREREQUISITES FOR INVESTIGATION") or sections.get("PREREQUISITES FOR INVESTIGATION") or ["Access to CPI Monitor, Security Material, and deployment history."],
            "DIAGNOSIS STEPS": sections.get("8. DIAGNOSIS STEPS") or sections.get("DIAGNOSIS STEPS") or sections.get("DIAGNOSIS PROCEDURE") or ["Check MPL and compare the failure with the last successful message."],
            "RECOVERY STEPS": sections.get("9. RECOVERY STEPS") or sections.get("RECOVERY STEPS") or sections.get("RECOVERY / FIX ACTIONS") or ["Apply the least risky corrective change, redeploy, and replay one controlled message."],
            "ESCALATION CRITERIA": sections.get("10. ESCALATION CRITERIA") or sections.get("ESCALATION CRITERIA") or sections.get("ESCALATION") or ["Escalate when the issue is reproducible and cannot be stabilized with standard operational handling."],
            "POST-FIX VALIDATION": sections.get("11. POST-FIX VALIDATION") or sections.get("POST-FIX VALIDATION") or sections.get("VALIDATION AFTER FIX") or ["Confirm that the same error signature does not reappear after controlled replay."],
        }
        ordered = self._enrich_update_runbook_sections(metadata=metadata, sections=ordered)
        evidence = self._v219_collect_mpl_evidence(metadata=metadata, limit=3)
        if evidence:
            ordered["MONITORING AND MPL EVIDENCE"] = [self._v219_format_mpl_evidence_line(rec, prefix=f"Sample {idx}") for idx, rec in enumerate(evidence, start=1)]
            if not any("Short symptom:" in x for x in ordered["ERROR SIGNATURE"]):
                ordered["ERROR SIGNATURE"].append(f"Short symptom: {self._shorten(evidence[0].get('error_text') or '', 170)}")
        ordered = self._refine_sections_with_policy(artifact_type="runbook", title=title, metadata=metadata, sections=ordered)
        out_path = target_dir / self._artifact_filename("RB", metadata['object_name'], metadata['priority'], version)
        out_path.write_text(self._render_runbook_from_sections(title, metadata, ordered), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "runbook_update", "version": version, "source_dir": str(source_path), "count": len(files), "updated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


def _kgs_maybe_refine_with_openai_v219(self, artifact_type: str, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> dict[str, list[str]] | None:
    if not self.settings.openai_api_key:
        return None
    policies = self._v219_load_policy_bundle()
    samples = self._v219_load_sample_bundle()
    interface_context = self._v219_match_interface_context(metadata=metadata)
    mpl_evidence = self._v219_collect_mpl_evidence(metadata=metadata, limit=3)
    payload = {
        "model": self.settings.openai_model,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a senior SAP CPI knowledge engineer. Rewrite the provided KEDB or Runbook sections into an enterprise-ready artifact. "
                            "Keep the same section keys and order. Preserve facts, remove generic wording, normalize taxonomy to the pattern A | B | C | D, "
                            "use exact interface/package values when provided, integrate MPL evidence concretely, and make recovery/diagnosis bullets action-led. "
                            "Do not invent metadata or IDs. Return strict JSON only in the form {\"sections\": {section_name: [lines]}}.\n\n"
                            "Primary policy excerpt:\n" + policies.get("primary", "") + "\n\n"
                            "BM25 policy excerpt:\n" + policies.get("bm25", "") + "\n\n"
                            "Reference sample:\n" + (samples.get("runbook_model") if artifact_type == "runbook" else samples.get("kedb_model"))
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(
                            {
                                "artifact_type": artifact_type,
                                "title": title,
                                "metadata": metadata,
                                "interface_context": interface_context,
                                "mpl_evidence": mpl_evidence,
                                "sections": sections,
                            },
                            ensure_ascii=False,
                        ),
                    }
                ],
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }
    try:
        with httpx.Client(timeout=45.0) as client:
            response = client.post(
                f"{self.settings.openai_base_url.rstrip('/')}/responses",
                headers={
                    "Authorization": f"Bearer {self.settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
        output_text = data.get("output_text") or ""
        if not output_text:
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"} and content.get("text"):
                        output_text += content.get("text", "")
        parsed = json.loads(output_text) if output_text else {}
        result = parsed.get("sections") if isinstance(parsed, dict) else None
        if isinstance(result, dict):
            normalized: dict[str, list[str]] = {}
            for key, value in result.items():
                if isinstance(value, list):
                    normalized[key] = [self._strip_bullet_prefix(str(x)) for x in value if str(x).strip()]
            return normalized or None
    except Exception:
        return None
    return None


KnowledgeGenerationService.__init__ = _kgs_init_v219
KnowledgeGenerationService._v219_reference_root = _kgs_v219_reference_root
KnowledgeGenerationService._v219_policies_root = _kgs_v219_policies_root
KnowledgeGenerationService._v219_read_text = _kgs_v219_read_text
KnowledgeGenerationService._v219_load_policy_bundle = _kgs_v219_load_policy_bundle
KnowledgeGenerationService._v219_load_sample_bundle = _kgs_v219_load_sample_bundle
KnowledgeGenerationService._v219_load_interface_catalog_index = _kgs_v219_load_interface_catalog_index
KnowledgeGenerationService._v219_flatten_records = _kgs_v219_flatten_records
KnowledgeGenerationService._v219_load_design_inventory_index = _kgs_v219_load_design_inventory_index
KnowledgeGenerationService._v219_complete_metadata = _kgs_v219_complete_metadata
KnowledgeGenerationService._v219_match_interface_context = _kgs_v219_match_interface_context
KnowledgeGenerationService._v219_load_mpl_records = _kgs_v219_load_mpl_records
KnowledgeGenerationService._v219_collect_mpl_evidence = _kgs_v219_collect_mpl_evidence
KnowledgeGenerationService._v219_format_mpl_evidence_line = _kgs_v219_format_mpl_evidence_line
KnowledgeGenerationService._v219_analysis_from_interface_catalog = _kgs_v219_analysis_from_interface_catalog
KnowledgeGenerationService._derive_scenarios = _kgs_derive_scenarios_v219
KnowledgeGenerationService._v219_professional_symptom = _kgs_v219_professional_symptom
KnowledgeGenerationService._render_kedb = _kgs_render_kedb_v219
KnowledgeGenerationService._render_runbook = _kgs_render_runbook_v219
KnowledgeGenerationService.update_kedb_documents = _kgs_update_kedb_documents_v219
KnowledgeGenerationService.update_runbook_documents = _kgs_update_runbook_documents_v219
KnowledgeGenerationService._maybe_refine_with_openai = _kgs_maybe_refine_with_openai_v219

# -----------------------------------------------------------------------------
# v2.1.9b polish layer
# -----------------------------------------------------------------------------
_current_normalize_action_line_v219b = KnowledgeGenerationService._normalize_action_line


def _kgs_normalize_action_line_v219b(self, line: str, *, artifact_type: str, section_name: str) -> str:
    text = self._strip_bullet_prefix(line)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^Generated by .*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^Generated at:.*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^No directly matching MPL sample was found in the provided export\.?\s*", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"The MPL ID for the failed message is\s*:\s*[A-Za-z0-9_\-]+", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^[A-Za-z0-9_.:$]+(?:Exception|Error):\s*", "", text)
    if not text:
        return ""
    if section_name == "TECHNICAL LANDSCAPE" and text.lower().startswith("error pattern:"):
        head, _, tail = text.partition(":")
        text = f"{head}: {re.sub(r'\s*\|\s*', ' | ', tail).strip()}"
    if artifact_type == "runbook" and section_name in {"DIAGNOSIS STEPS", "RECOVERY STEPS", "POST-FIX VALIDATION", "ESCALATION CRITERIA"}:
        text = text[:1].upper() + text[1:]
        if not re.match(r"^(Check|Verify|Confirm|Review|Capture|Compare|Collect|Preserve|Reduce|Apply|Replay|Lower|Schedule|Escalate|Contain|Inspect|Coordinate|Use|Document|Re-run|Increase|Persist|Open|Validate|Identify)", text):
            text = f"Check {text[:1].lower() + text[1:]}" if section_name == "DIAGNOSIS STEPS" else text
    return text


def _kgs_update_runbook_documents_v219b(self, version: str, source_dir: str | None = None, source_zip_path: str | None = None, output_dir: str | None = None) -> dict[str, Any]:
    version = self._normalize_version(version)
    source_path = self._resolve_markdown_source(artifact_type="runbooks", source_dir=source_dir, source_zip_path=source_zip_path)
    target_dir = self._resolve_output_dir(output_dir, "runbooks_updated", version)
    target_dir.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for path in sorted(source_path.glob("*.md")):
        parsed = self._parse_markdown_sections(path.read_text(encoding="utf-8"))
        metadata = self._v219_complete_metadata(self._normalize_metadata(parsed["metadata"], artifact_type="runbook"), artifact_type="runbook")
        metadata["artifact_type"] = "runbook"
        metadata["priority"] = metadata.get("priority") or self._priority_from_filename(path.name)
        metadata["object_name"] = self._canonical_object_name(metadata.get("object_name") or self._object_from_filename(path.name))
        metadata["version"] = version
        title = parsed["title"] or self._humanize_object_name(metadata["object_name"])
        metadata["document_id"] = parsed.get("document_id") or f"RB-{metadata['priority']}-0000"
        sections = parsed["sections"]
        evidence = self._v219_collect_mpl_evidence(metadata=metadata, limit=3)
        ordered = {
            "PURPOSE": sections.get("1. PURPOSE") or sections.get("PURPOSE") or [f"This runbook supports the canonical incident pattern {metadata['object_name']}."],
            "BUSINESS CONTEXT": sections.get("2. BUSINESS CONTEXT") or sections.get("BUSINESS CONTEXT") or ["Business impact requires confirmation from the owning interface team."],
            "TECHNICAL LANDSCAPE": [
                f"Package: {metadata['package_name']}",
                f"Integration flow ID: {metadata['integration_flow_id']}",
                f"Integration flow name: {metadata['integration_flow_name']}",
                *[
                    x
                    for x in (sections.get("3. TECHNICAL LANDSCAPE") or sections.get("TECHNICAL LANDSCAPE") or [])
                    if not self._strip_bullet_prefix(str(x)).lower().startswith(("package:", "integration flow id:", "integration flow name:"))
                ],
            ],
            "MONITORING AND MPL EVIDENCE": [self._v219_format_mpl_evidence_line(rec, prefix=f"Sample {idx}") for idx, rec in enumerate(evidence, start=1)] or ["No directly matching MPL sample was found in the provided export. The runbook is grounded mainly in the KEDB taxonomy and should be enriched further when additional MPL samples become available.", "Sample 1: No directly matching MPL example available in the provided export."],
            "ERROR SIGNATURE": sections.get("5. ERROR SIGNATURE") or sections.get("ERROR SIGNATURE") or [f"Normalized object name: {metadata['object_name']}"],
            "KNOWN ROOT CAUSES": sections.get("6. KNOWN ROOT CAUSES") or sections.get("KNOWN ROOT CAUSES") or ["Root cause requires technical verification."],
            "PREREQUISITES FOR INVESTIGATION": [
                "Access to SAP CPI Monitor / MPL and trace where applicable.",
                f"Access to the owning package **{metadata['package_name']}** and the interface **{metadata['interface_id']}**.",
                "Deployment/runtime version reference and recent transport/deployment history.",
                "Security material and endpoint configuration access when authentication, connectivity, or certificate topics are involved.",
                "Representative failing payload or reproducible test message where available.",
            ],
            "DIAGNOSIS STEPS": sections.get("8. DIAGNOSIS STEPS") or sections.get("DIAGNOSIS STEPS") or sections.get("DIAGNOSIS PROCEDURE") or ["Check MPL and compare the failure with the last successful message."],
            "RECOVERY STEPS": sections.get("9. RECOVERY STEPS") or sections.get("RECOVERY STEPS") or sections.get("RECOVERY / FIX ACTIONS") or ["Apply the least risky corrective change, redeploy, and replay one controlled message."],
            "ESCALATION CRITERIA": sections.get("10. ESCALATION CRITERIA") or sections.get("ESCALATION CRITERIA") or sections.get("ESCALATION") or ["Escalate when the issue is reproducible and cannot be stabilized with standard operational handling."],
            "POST-FIX VALIDATION": sections.get("11. POST-FIX VALIDATION") or sections.get("POST-FIX VALIDATION") or sections.get("VALIDATION AFTER FIX") or ["Confirm that the same error signature does not reappear after controlled replay."],
        }
        if evidence and not any("Short symptom:" in x for x in ordered["ERROR SIGNATURE"]):
            ordered["ERROR SIGNATURE"].append(f"Short symptom: {self._shorten(evidence[0].get('error_text') or '', 170)}")
        ordered = self._enrich_update_runbook_sections(metadata=metadata, sections=ordered)
        ordered = self._refine_sections_with_policy(artifact_type="runbook", title=title, metadata=metadata, sections=ordered)
        out_path = target_dir / self._artifact_filename("RB", metadata['object_name'], metadata['priority'], version)
        out_path.write_text(self._render_runbook_from_sections(title, metadata, ordered), encoding="utf-8")
        files.append(str(out_path))
    archive_path = self._zip_directory(target_dir)
    return {"artifact_type": "runbook_update", "version": version, "source_dir": str(source_path), "count": len(files), "updated_count": len(files), "output_dir": str(target_dir), "archive_path": str(archive_path), "files": files}


KnowledgeGenerationService._normalize_action_line = _kgs_normalize_action_line_v219b
KnowledgeGenerationService.update_runbook_documents = _kgs_update_runbook_documents_v219b


# -----------------------------------------------------------------------------
# v2.1.12 metadata + formatting + scoped-discovery hardening layer
# -----------------------------------------------------------------------------

def _kgs_collect_iflows_v212(self, package_id: str | None = None, iflow_ids: list[str] | None = None) -> list[dict[str, Any]]:
    async def inner() -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        inventory_package_map = self._get_inventory_package_map()
        try:
            raw = await self.sap_client.list_iflows(package_id=package_id)
            items = raw.get('items', [])
        except Exception:
            items = self._get_inventory_iflows()
        if not items:
            items = self._get_inventory_iflows()
        if package_id:
            items = [x for x in items if str(x.get('PackageId') or x.get('Package') or '').strip() == package_id]
        if iflow_ids:
            allowed = {str(x) for x in iflow_ids}
            items = [x for x in items if str(x.get('Id') or x.get('iflow_id') or '').strip() in allowed]
        deduped: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for item in items:
            iflow_id = str(item.get('Id') or item.get('iflow_id') or '').strip()
            if not iflow_id or iflow_id in seen_ids:
                continue
            seen_ids.add(iflow_id)
            pkg_id = str(item.get('PackageId') or item.get('Package') or '').strip()
            current_name = str(item.get('PackageName') or item.get('PackageNameDisplay') or '').strip()
            if pkg_id and (not current_name or current_name == pkg_id):
                resolved_name = inventory_package_map.get(pkg_id) or current_name or pkg_id
                if resolved_name:
                    item['PackageName'] = resolved_name
                    item.setdefault('PackageNameDisplay', resolved_name)
            deduped.append(item)
        if not package_id:
            package_map = await self._get_package_name_map()
            for item in deduped:
                pkg_id = str(item.get('PackageId') or item.get('Package') or '').strip()
                current_name = str(item.get('PackageName') or item.get('PackageNameDisplay') or '').strip()
                resolved_name = package_map.get(pkg_id) or package_map.get(pkg_id.lower()) or package_map.get(pkg_id.upper())
                if pkg_id and resolved_name and (not current_name or current_name == pkg_id):
                    item['PackageName'] = resolved_name
                    item.setdefault('PackageNameDisplay', resolved_name)
        return deduped
    return inner()


def _kgs_v219_match_interface_context_v212(self, *, metadata: dict[str, str] | None = None, scenario: ScenarioFamily | None = None) -> dict[str, Any]:
    interface_index = self._v219_load_interface_catalog_index()
    inventory = self._v219_load_design_inventory_index()
    candidates: list[str] = []
    if scenario is not None:
        candidates.extend([x for x in sorted(scenario.affected_interfaces) if x])
        candidates.extend([x for x in sorted(scenario.flow_names) if x])
        candidates.extend([x for x in sorted(scenario.package_names) if x])
        candidates.append(f"{self.settings.default_sap_sid}_{scenario.code}")
    if metadata:
        candidates.extend([
            str(metadata.get('interface_id') or ''),
            str(metadata.get('integration_flow_id') or ''),
            str(metadata.get('integration_flow_name') or ''),
            str(metadata.get('object_name') or ''),
            str(metadata.get('package_name') or ''),
        ])
    for candidate in candidates:
        norm = self._normalize_object_name(candidate)
        if not norm:
            continue
        if norm in interface_index:
            entry = interface_index[norm]
            sections = entry.get('sections', {})
            return {
                'document_id': entry.get('document_id') or '',
                'interface_id': str(entry.get('metadata', {}).get('interface_id') or entry.get('metadata', {}).get('integration_flow_id') or entry.get('metadata', {}).get('integration_flow_name') or candidate),
                'integration_flow_id': str(entry.get('metadata', {}).get('integration_flow_id') or entry.get('metadata', {}).get('interface_id') or candidate),
                'integration_flow_name': str(entry.get('metadata', {}).get('integration_flow_name') or entry.get('metadata', {}).get('interface_id') or candidate),
                'package_name': str(entry.get('metadata', {}).get('package_name') or 'Multiple packages'),
                'scope_excerpt': entry.get('scope_excerpt') or '',
                'core_excerpt': entry.get('core_excerpt') or '',
                'key_terms': [self._strip_bullet_prefix(x) for x in (sections.get('3. KEY TERMS') or [])[:8]],
            }
        inv = inventory['iflow_map'].get(candidate) or inventory['iflow_map'].get(norm)
        if inv:
            return {
                'document_id': '',
                'interface_id': str(inv.get('iflow_id') or inv.get('interface_id') or inv.get('iflow_name') or candidate),
                'integration_flow_id': str(inv.get('iflow_id') or inv.get('interface_id') or inv.get('iflow_name') or candidate),
                'integration_flow_name': str(inv.get('iflow_name') or inv.get('integration_flow_id') or inv.get('iflow_id') or candidate),
                'package_name': str(inv.get('package_name') or inv.get('package_id') or 'Multiple packages'),
                'scope_excerpt': '',
                'core_excerpt': '',
                'key_terms': [],
            }
    scenario_interface_id = sorted([x for x in (scenario.affected_interfaces if scenario else set()) if x])[0] if scenario and scenario.affected_interfaces else ''
    scenario_flow_name = sorted([x for x in (scenario.flow_names if scenario else set()) if x])[0] if scenario and scenario.flow_names else ''
    scenario_package_name = sorted([x for x in (scenario.package_names if scenario else set()) if x])[0] if scenario and scenario.package_names else ''
    return {
        'document_id': '',
        'interface_id': str((metadata or {}).get('interface_id') or (metadata or {}).get('integration_flow_id') or scenario_interface_id or 'UNKNOWN_INTERFACE'),
        'integration_flow_id': str((metadata or {}).get('integration_flow_id') or (metadata or {}).get('interface_id') or scenario_interface_id or 'UNKNOWN_INTERFACE'),
        'integration_flow_name': str((metadata or {}).get('integration_flow_name') or scenario_flow_name or scenario_interface_id or 'UNKNOWN_INTERFACE'),
        'package_name': str((metadata or {}).get('package_name') or scenario_package_name or 'Multiple packages'),
        'scope_excerpt': '',
        'core_excerpt': '',
        'key_terms': [],
    }


def _kgs_render_kedb_from_sections_v212(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
    metadata = dict(metadata)
    metadata['version'] = self._normalize_version(metadata.get('version', 'v1'))
    return self._render_structured_markdown(
        title=title,
        metadata=metadata,
        id_label='KEDB ID',
        doc_id=metadata.get('document_id') or f"KEDB-{metadata['priority']}-{metadata['object_name']}",
        title_label='KEDB TITLE',
        title_value=title,
        section_order=[
            '1. SYMPTOM',
            '2. ERROR PATTERN',
            '3. ROOT CAUSE',
            '4. DIAGNOSIS SIGNALS',
            '5. RESOLUTION',
            '6. VALIDATION',
            '7. WORKAROUND',
            '8. RELATED ARTIFACTS',
        ],
        section_map={
            '1. SYMPTOM': sections.get('SYMPTOM', ['None']),
            '2. ERROR PATTERN': sections.get('ERROR PATTERN', [self._taxonomy_from_object_name(metadata['object_name'])]),
            '3. ROOT CAUSE': sections.get('ROOT CAUSE', ['None']),
            '4. DIAGNOSIS SIGNALS': sections.get('DIAGNOSIS SIGNALS', ['None']),
            '5. RESOLUTION': sections.get('RESOLUTION', ['None']),
            '6. VALIDATION': sections.get('VALIDATION', ['None']),
            '7. WORKAROUND': sections.get('WORKAROUND', ['None']),
            '8. RELATED ARTIFACTS': sections.get('RELATED ARTIFACTS', ['None']),
        },
        bullet='*',
        escape_underscores=False,
        plain_sections=set(),
    )


def _kgs_render_runbook_from_sections_v212(self, title: str, metadata: dict[str, str], sections: dict[str, list[str]]) -> str:
    metadata = dict(metadata)
    metadata['version'] = self._normalize_version(metadata.get('version', 'v1'))
    return self._render_structured_markdown(
        title=title,
        metadata=metadata,
        id_label='RUNBOOK ID',
        doc_id=metadata.get('document_id') or f"RB-{metadata['priority']}-{metadata['object_name']}",
        title_label='RUNBOOK TITLE',
        title_value=title,
        section_order=[
            '1. PURPOSE',
            '2. BUSINESS CONTEXT',
            '3. TECHNICAL LANDSCAPE',
            '4. MONITORING AND MPL EVIDENCE',
            '5. ERROR SIGNATURE',
            '6. KNOWN ROOT CAUSES',
            '7. PREREQUISITES FOR INVESTIGATION',
            '8. DIAGNOSIS STEPS',
            '9. RECOVERY STEPS',
            '10. ESCALATION CRITERIA',
            '11. POST-FIX VALIDATION',
        ],
        section_map={
            '1. PURPOSE': sections.get('PURPOSE', ['This runbook supports incident triage, diagnosis, recovery, and validation for the referenced scenario.']),
            '2. BUSINESS CONTEXT': sections.get('BUSINESS CONTEXT', ['None']),
            '3. TECHNICAL LANDSCAPE': sections.get('TECHNICAL LANDSCAPE', ['None']),
            '4. MONITORING AND MPL EVIDENCE': sections.get('MONITORING AND MPL EVIDENCE', ['No directly matching MPL evidence was attached during generation.']),
            '5. ERROR SIGNATURE': sections.get('ERROR SIGNATURE', ['None']),
            '6. KNOWN ROOT CAUSES': sections.get('KNOWN ROOT CAUSES', ['None']),
            '7. PREREQUISITES FOR INVESTIGATION': sections.get('PREREQUISITES FOR INVESTIGATION', ['Access to SAP CPI Monitor / MPL and the affected iFlow.']),
            '8. DIAGNOSIS STEPS': sections.get('DIAGNOSIS STEPS', ['Check MPL for the failing time window and compare with the last successful run.']),
            '9. RECOVERY STEPS': sections.get('RECOVERY STEPS', ['Stabilize the flow, apply the corrective change, and replay one controlled message.']),
            '10. ESCALATION CRITERIA': sections.get('ESCALATION CRITERIA', ['Escalate when the issue is reproducible or business impact expands.']),
            '11. POST-FIX VALIDATION': sections.get('POST-FIX VALIDATION', ['Confirm that the same signature no longer appears in the immediate post-fix window.']),
        },
        bullet='*',
        escape_underscores=False,
        plain_sections={'1. PURPOSE'},
    )


KnowledgeGenerationService._collect_iflows = _kgs_collect_iflows_v212
KnowledgeGenerationService._v219_match_interface_context = _kgs_v219_match_interface_context_v212
KnowledgeGenerationService._render_kedb_from_sections = _kgs_render_kedb_from_sections_v212
KnowledgeGenerationService._render_runbook_from_sections = _kgs_render_runbook_from_sections_v212
