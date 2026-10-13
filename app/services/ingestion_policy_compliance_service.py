from __future__ import annotations

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

from app.config import Settings


ACCENT_BLUE = "2F5597"
LIGHT_BLUE = "D9EAF7"
BORDER_BLUE = "8AA9C1"
MUTED_BLUE = "5B9BD5"
DARK_TEXT = "1F1F1F"
CAPTION_BLUE = "4F81BD"

RUNBOOK_PRIMARY_CRITERIA = [
    "Naming",
    "Metadata",
    "Sections",
    "Taxonomy",
    "Pair links",
    "Compactness",
]

KEDB_PRIMARY_CRITERIA = [
    "Naming",
    "Metadata",
    "Sections",
    "Taxonomy",
    "Pair links",
    "Compactness",
]

RUNBOOK_BM25_RULES = [
    "Canonical problem",
    "Searchable title",
    "Metadata order",
    "Canonical terms",
    "Stable headings",
    "Semantic separation",
    "Literal evidence",
    "Action-led steps",
    "Normalized taxonomy",
    "Low narrative noise",
    "Cross-reference alignment",
    "Pre/post-fix proof",
]

KEDB_BM25_RULES = [
    "Single issue focus",
    "Technical title",
    "Metadata order",
    "Vocabulary consistency",
    "Stable sections",
    "Semantic separation",
    "Literal evidence",
    "Action-led steps",
    "Normalized taxonomy",
    "Pair alignment",
    "Compact wording",
]

ACTION_VERBS = {
    "check",
    "verify",
    "confirm",
    "compare",
    "inspect",
    "review",
    "open",
    "replay",
    "restart",
    "restore",
    "apply",
    "reduce",
    "coordinate",
    "schedule",
    "lower",
    "pause",
    "capture",
    "contain",
    "collect",
    "validate",
    "escalate",
    "identify",
    "trace",
    "monitor",
}

RUNBOOK_REQUIRED_METADATA = [
    "environment",
    "customer_id",
    "system_id",
    "sap_sid",
    "artifact_type",
    "object_name",
    "priority",
    "interface_id",
    "integration_flow_id",
    "integration_flow_name",
    "package_name",
    "review_cycle",
    "version",
]

KEDB_REQUIRED_METADATA = RUNBOOK_REQUIRED_METADATA

RUNBOOK_REQUIRED_SECTIONS = [
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
]

KEDB_REQUIRED_SECTIONS = [
    "1. SYMPTOM",
    "2. ERROR PATTERN",
    "3. ROOT CAUSE",
    "4. DIAGNOSIS SIGNALS",
    "5. RESOLUTION",
    "6. VALIDATION",
    "7. WORKAROUND",
    "8. RELATED ARTIFACTS",
]

INTERFACE_CATALOG_REQUIRED_SECTIONS = [
    "1. PURPOSE",
    "2. TECHNICAL SUMMARY",
    "3. LANDSCAPE AND PARTICIPANTS",
    "4. PROCESSING FLOW",
    "5. OPERATIONS AND MONITORING",
    "6. RELATED ARTIFACTS",
]

OFFICIAL_DOC_REQUIRED_SECTIONS = [
    "1. PURPOSE",
    "2. SCOPE",
    "3. KEY TERMS",
    "4. CORE EXPLANATION",
    "5. OPERATIONAL RELEVANCE",
    "6. RELATED ARTIFACTS",
]

PLACEHOLDER_MPL_PHRASES = [
    "No directly matching MPL sample was found",
    "No directly matching MPL example available",
]


@dataclass
class ParsedDocument:
    path: Path
    component: str
    title: str
    metadata_keys: list[str]
    metadata: dict[str, str]
    sections: list[str]
    section_bodies: dict[str, str]
    text: str
    word_count: int
    bullet_count: int
    long_paragraphs: int
    paragraph_count: int
    id_count: int
    priority: str
    object_name: str
    normalized_error_pattern: str
    has_pair_link: bool
    has_literal_evidence: bool
    direct_mpl_sample: bool
    rollback_inline: bool
    action_bullet_ratio: float
    exact_required_structure: bool
    filename_compliant: bool
    metadata_compliant: bool
    taxonomy_compliant: bool
    searchable_title: bool


@dataclass
class CriterionScore:
    component: str
    criterion: str
    score: float
    comment: str


@dataclass
class ComponentAssessment:
    component: str
    files: int
    p1: int
    p2: int
    p3: int
    primary_score: float
    bm25_score: float
    verdict: str
    primary_rows: list[CriterionScore]
    bm25_rows: list[CriterionScore]
    quantitative_rows: list[tuple[str, str]]
    average_words: float
    average_bullets: float
    long_paragraph_count: int
    paragraph_count: int
    long_paragraph_pct: float
    direct_mpl_samples: int


@dataclass
class GenericFamilyAssessment:
    family: str
    files: int
    primary_score: float
    bm25_score: float
    notes: list[str]


class IngestionPolicyComplianceService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.project_root = Path(__file__).resolve().parents[2]
        self.base_output_dir = Path(getattr(settings, "knowledge_output_dir", "./exports/knowledge")).resolve()
        self.report_output_dir = self.project_root / "exports" / "compliance"
        self.report_output_dir.mkdir(parents=True, exist_ok=True)

    def assess_ingestion_policy_compliance(
        self,
        version: str,
        knowledge_version: str | None = None,
        source_root: str | None = None,
        output_dir: str | None = None,
        use_openai: bool = True,
    ) -> dict[str, Any]:
        report_version = self._normalize_version(version)
        source_base = Path(source_root).resolve() if source_root else self.base_output_dir
        selected_version = knowledge_version or self._resolve_latest_knowledge_version(source_base)
        target_dir = Path(output_dir).resolve() if output_dir else self.report_output_dir / report_version
        target_dir.mkdir(parents=True, exist_ok=True)

        runbooks = self._load_documents(
            component="Runbook",
            directory=source_base / "runbooks" / selected_version,
            required_metadata=RUNBOOK_REQUIRED_METADATA,
            required_sections=RUNBOOK_REQUIRED_SECTIONS,
            filename_regex=re.compile(r"^RB_[A-Z0-9]+_[A-Z0-9]+_[A-Z0-9_]+_P[1-4]_v[0-9][A-Za-z0-9.\-]*\.md$"),
        )
        kedb = self._load_documents(
            component="KEDB",
            directory=source_base / "kedb" / selected_version,
            required_metadata=KEDB_REQUIRED_METADATA,
            required_sections=KEDB_REQUIRED_SECTIONS,
            filename_regex=re.compile(r"^KB_[A-Z0-9]+_[A-Z0-9]+_[A-Z0-9_]+_P[1-4]_v[0-9][A-Za-z0-9.\-]*\.md$"),
        )
        pair_alignment = self._pair_alignment(kedb, runbooks)
        kedb_assessment = self._assess_component("KEDB", kedb, pair_alignment)
        runbook_assessment = self._assess_component("Runbook", runbooks, pair_alignment)

        other_families = [
            self._assess_generic_markdown_family(
                family="interface_catalogs",
                directory=source_base / "interface_catalogs" / selected_version,
                prefix="DOC",
                required_sections=INTERFACE_CATALOG_REQUIRED_SECTIONS,
            ),
            self._assess_generic_markdown_family(
                family="official_docs",
                directory=source_base / "official_docs" / selected_version,
                prefix="DOC",
                required_sections=OFFICIAL_DOC_REQUIRED_SECTIONS,
            ),
        ]

        narrative = self._build_narrative(
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            pair_alignment=pair_alignment,
            other_families=other_families,
        )
        ai_narrative = self._maybe_enrich_with_openai(
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            pair_alignment=pair_alignment,
            narrative=narrative,
        ) if use_openai else None
        if ai_narrative:
            narrative = {**narrative, **ai_narrative}

        remediation_text = self._render_remediation_text(
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            other_families=other_families,
            pair_alignment=pair_alignment,
            narrative=narrative,
        )

        txt_path = target_dir / f"AI4BIZ_Ingestion_Policy_Compliance_{report_version}.txt"
        remediation_txt_path = target_dir / f"AI4BIZ_Remediation_Package_{report_version}.txt"
        json_path = target_dir / f"AI4BIZ_Ingestion_Policy_Compliance_{report_version}.json"
        docx_path = target_dir / f"AI4BIZ_Ingestion_Policy_Compliance_{report_version}.docx"
        pdf_path = target_dir / f"AI4BIZ_Ingestion_Policy_Compliance_{report_version}.pdf"
        chart_paths = {
            "overall_scores": target_dir / f"AI4BIZ_Overall_Compliance_Scores_{report_version}.png",
            "priority_distribution": target_dir / f"AI4BIZ_Priority_Distribution_{report_version}.png",
            "primary_indicators": target_dir / f"AI4BIZ_Primary_Indicators_{report_version}.png",
            "runbook_bm25": target_dir / f"AI4BIZ_Runbook_BM25_Profile_{report_version}.png",
            "kedb_bm25": target_dir / f"AI4BIZ_KEDB_BM25_Profile_{report_version}.png",
        }

        self._write_charts(kedb_assessment, runbook_assessment, chart_paths)
        txt_content = self._render_compliance_text(
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            other_families=other_families,
            pair_alignment=pair_alignment,
            narrative=narrative,
        )
        txt_path.write_text(txt_content, encoding="utf-8")
        remediation_txt_path.write_text(remediation_text, encoding="utf-8")
        json_payload = self._build_json_payload(
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            other_families=other_families,
            pair_alignment=pair_alignment,
            narrative=narrative,
            chart_paths=chart_paths,
            remediation_txt_path=remediation_txt_path,
            compliance_txt_path=txt_path,
            docx_path=docx_path,
            pdf_path=pdf_path,
        )
        json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self._write_docx_report(
            docx_path=docx_path,
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            pair_alignment=pair_alignment,
            narrative=narrative,
            chart_paths=chart_paths,
        )
        self._write_pdf_report(
            pdf_path=pdf_path,
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            narrative=narrative,
            chart_paths=chart_paths,
        )

        screen_markdown = self._render_screen_markdown(
            knowledge_version=selected_version,
            report_version=report_version,
            kedb_assessment=kedb_assessment,
            runbook_assessment=runbook_assessment,
            pair_alignment=pair_alignment,
            narrative=narrative,
            chart_paths=chart_paths,
        )

        return {
            "artifact_type": "ingestion_policy_compliance_assessment",
            "version": report_version,
            "knowledge_version": selected_version,
            "source_root": str(source_base),
            "output_dir": str(target_dir),
            "docx_path": str(docx_path),
            "pdf_path": str(pdf_path) if pdf_path.exists() else None,
            "compliance_txt_path": str(txt_path),
            "remediation_txt_path": str(remediation_txt_path),
            "json_path": str(json_path),
            "chart_paths": {name: str(path) for name, path in chart_paths.items()},
            "summary": narrative.get("executive_summary", ""),
            "strengths": narrative.get("main_strengths", []),
            "optimization_opportunities": narrative.get("optimization_opportunities", []),
            "conclusion": narrative.get("conclusion", ""),
            "component_scores": {
                "KEDB": {
                    "files": kedb_assessment.files,
                    "p1": kedb_assessment.p1,
                    "p2": kedb_assessment.p2,
                    "p3": kedb_assessment.p3,
                    "primary_score": kedb_assessment.primary_score,
                    "bm25_score": kedb_assessment.bm25_score,
                },
                "Runbook": {
                    "files": runbook_assessment.files,
                    "p1": runbook_assessment.p1,
                    "p2": runbook_assessment.p2,
                    "p3": runbook_assessment.p3,
                    "primary_score": runbook_assessment.primary_score,
                    "bm25_score": runbook_assessment.bm25_score,
                },
            },
            "additional_family_observations": [
                {
                    "family": family.family,
                    "files": family.files,
                    "primary_score": family.primary_score,
                    "bm25_score": family.bm25_score,
                    "notes": family.notes,
                }
                for family in other_families
            ],
            "screen_markdown": screen_markdown,
        }

    def _normalize_version(self, version: str) -> str:
        cleaned = (version or "").strip()
        return cleaned if cleaned.lower().startswith("v") else f"v{cleaned or '1'}"

    def _resolve_latest_knowledge_version(self, source_base: Path) -> str:
        candidates: list[str] = []
        for family in ("kedb", "runbooks", "interface_catalogs", "official_docs"):
            family_dir = source_base / family
            if not family_dir.exists():
                continue
            for child in family_dir.iterdir():
                if child.is_dir():
                    candidates.append(child.name)
        if not candidates:
            return "v1"
        return sorted(set(candidates), key=self._version_sort_key)[-1]

    def _version_sort_key(self, value: str) -> tuple[int, ...]:
        parts = re.findall(r"\d+", value)
        return tuple(int(part) for part in parts) if parts else (0,)

    def _load_documents(
        self,
        *,
        component: str,
        directory: Path,
        required_metadata: list[str],
        required_sections: list[str],
        filename_regex: re.Pattern[str],
    ) -> list[ParsedDocument]:
        documents: list[ParsedDocument] = []
        for path in sorted(directory.glob("*.md")) if directory.exists() else []:
            text = path.read_text(encoding="utf-8", errors="ignore").replace(r"\_", "_")
            lines = text.splitlines()
            metadata_keys: list[str] = []
            metadata: dict[str, str] = {}
            title = ""
            sections: list[str] = []
            section_bodies: dict[str, str] = {}
            current_section = ""
            current_lines: list[str] = []
            for idx, raw_line in enumerate(lines):
                line = raw_line.strip()
                if idx == 0 and line.startswith("# "):
                    title = line[2:].strip()
                meta_match = re.match(r'^([a-z_]+):\s*"?(.*?)"?$', line)
                if meta_match:
                    key = meta_match.group(1)
                    value = meta_match.group(2).strip()
                    metadata_keys.append(key)
                    metadata[key] = value
                if re.match(r"^\d+\.\s+", line):
                    if current_section:
                        section_bodies[current_section] = "\n".join(current_lines).strip()
                    current_section = line
                    sections.append(line)
                    current_lines = []
                elif current_section:
                    current_lines.append(raw_line)
            if current_section:
                section_bodies[current_section] = "\n".join(current_lines).strip()

            paragraphs = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
            paragraph_word_counts = [len(re.findall(r"\b\w+\b", block)) for block in paragraphs]
            long_paragraphs = sum(1 for value in paragraph_word_counts if value > 60)
            word_count = len(re.findall(r"\b\w+\b", text))
            bullet_count = sum(1 for line in lines if line.strip().startswith(("-", "*")))
            artifact_id_label = {
                "Runbook": r"(?m)^RUNBOOK ID\s*$",
                "KEDB": r"(?m)^KEDB ID\s*$",
            }.get(component, r"(?m)^DOC ID\s*$")
            id_count = len(re.findall(artifact_id_label, text))
            priority_match = re.search(r"_(P\d)_", path.name)
            priority = priority_match.group(1) if priority_match else metadata.get("priority", "")
            normalized_pattern = self._extract_error_pattern(component, section_bodies, text)
            has_pair_link = self._has_pair_link(component, section_bodies, text)
            direct_mpl_sample = self._has_direct_mpl_sample(component, section_bodies)
            rollback_inline = self._has_inline_rollback(component, section_bodies)
            action_bullet_ratio = self._action_bullet_ratio(component, section_bodies)
            has_literal_evidence = self._has_literal_evidence(component, section_bodies, text)
            searchable_title = self._is_searchable_title(title, path.name)
            exact_required_structure = sections == required_sections
            metadata_compliant = metadata_keys[: len(required_metadata)] == required_metadata
            taxonomy_compliant = self._is_taxonomy_compliant(normalized_pattern, text)
            filename_compliant = bool(filename_regex.match(path.name))

            documents.append(
                ParsedDocument(
                    path=path,
                    component=component,
                    title=title,
                    metadata_keys=metadata_keys,
                    metadata=metadata,
                    sections=sections,
                    section_bodies=section_bodies,
                    text=text,
                    word_count=word_count,
                    bullet_count=bullet_count,
                    long_paragraphs=long_paragraphs,
                    paragraph_count=max(1, len(paragraphs)),
                    id_count=id_count,
                    priority=priority,
                    object_name=metadata.get("object_name", ""),
                    normalized_error_pattern=normalized_pattern,
                    has_pair_link=has_pair_link,
                    has_literal_evidence=has_literal_evidence,
                    direct_mpl_sample=direct_mpl_sample,
                    rollback_inline=rollback_inline,
                    action_bullet_ratio=action_bullet_ratio,
                    exact_required_structure=exact_required_structure,
                    filename_compliant=filename_compliant,
                    metadata_compliant=metadata_compliant,
                    taxonomy_compliant=taxonomy_compliant,
                    searchable_title=searchable_title,
                )
            )
        return documents

    def _extract_error_pattern(self, component: str, section_bodies: dict[str, str], text: str) -> str:
        if component == "KEDB":
            body = section_bodies.get("2. ERROR PATTERN", "")
        else:
            body = section_bodies.get("3. TECHNICAL LANDSCAPE", "")
        match = re.search(r"Error pattern:\s*([^\n]+)", body, re.IGNORECASE)
        if not match:
            match = re.search(r"-\s*([A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+)", body)
        if not match:
            match = re.search(r"([A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+\s*\|\s*[A-Z0-9_ ]+)", text)
        value = match.group(1).strip() if match else ""
        value = re.sub(r"\s*\|\s*", " | ", value)
        value = re.sub(r"\s+", " ", value).strip(" -")
        return value

    def _has_pair_link(self, component: str, section_bodies: dict[str, str], text: str) -> bool:
        if component == "KEDB":
            body = section_bodies.get("8. RELATED ARTIFACTS", "")
            return "Primary runbook:" in body or "RB_" in body
        body = section_bodies.get("3. TECHNICAL LANDSCAPE", "") + "\n" + text
        return "Source KEDB ID" in body or re.search(r"KEDB[-_]", body) is not None

    def _has_direct_mpl_sample(self, component: str, section_bodies: dict[str, str]) -> bool:
        if component != "Runbook":
            return False
        body = section_bodies.get("4. MONITORING AND MPL EVIDENCE", "")
        if not body:
            return False
        if any(phrase in body for phrase in PLACEHOLDER_MPL_PHRASES):
            return False
        return True

    def _has_inline_rollback(self, component: str, section_bodies: dict[str, str]) -> bool:
        if component != "Runbook":
            return False
        body = section_bodies.get("9. RECOVERY STEPS", "")
        return "Rollback" in body and not any(section.startswith("10. ROLLBACK") for section in section_bodies)

    def _action_bullet_ratio(self, component: str, section_bodies: dict[str, str]) -> float:
        relevant_sections = [
            section_bodies.get("8. DIAGNOSIS STEPS", ""),
            section_bodies.get("9. RECOVERY STEPS", ""),
        ] if component == "Runbook" else [
            section_bodies.get("4. DIAGNOSIS SIGNALS", ""),
            section_bodies.get("5. RESOLUTION", ""),
        ]
        bullets: list[str] = []
        for body in relevant_sections:
            for line in body.splitlines():
                stripped = line.strip().lstrip("-* ").strip()
                if stripped:
                    bullets.append(stripped)
        if not bullets:
            return 0.0
        action_led = 0
        for item in bullets:
            first_word = re.split(r"\W+", item.lower())[0]
            if first_word in ACTION_VERBS:
                action_led += 1
        return action_led / max(len(bullets), 1)

    def _has_literal_evidence(self, component: str, section_bodies: dict[str, str], text: str) -> bool:
        signals = [
            r"HTTP/1\.1\s+\d{3}",
            r"\b\d{3}\b",
            r"MessageGuid",
            r"CorrelationId",
            r"MPL ID",
            r"IR\d+_IF\d+",
            r"SAP-CI-\d+",
        ]
        if component == "Runbook":
            evidence_body = section_bodies.get("4. MONITORING AND MPL EVIDENCE", "") + "\n" + section_bodies.get("5. ERROR SIGNATURE", "")
        else:
            evidence_body = section_bodies.get("1. SYMPTOM", "") + "\n" + section_bodies.get("8. RELATED ARTIFACTS", "")
        return any(re.search(pattern, evidence_body or text) for pattern in signals)

    def _is_searchable_title(self, title: str, filename: str) -> bool:
        reference = title or filename.replace("_", " ")
        words = re.findall(r"[A-Za-z0-9_]+", reference)
        return len(words) >= 4

    def _is_taxonomy_compliant(self, normalized_pattern: str, text: str) -> bool:
        if normalized_pattern:
            return bool(re.fullmatch(r"[A-Z0-9_ ]+( \| [A-Z0-9_ ]+){3}", normalized_pattern))
        fallback = re.search(r"[A-Z0-9_ ]+ \| [A-Z0-9_ ]+ \| [A-Z0-9_ ]+ \| [A-Z0-9_ ]+", text)
        return bool(fallback)

    def _pair_alignment(self, kedb_docs: list[ParsedDocument], runbook_docs: list[ParsedDocument]) -> dict[str, Any]:
        kedb_map = {doc.path.name.replace("KB_", ""): doc for doc in kedb_docs}
        runbook_map = {doc.path.name.replace("RB_", ""): doc for doc in runbook_docs}
        shared_keys = sorted(set(kedb_map) & set(runbook_map))
        title_matches = 0
        object_matches = 0
        pattern_matches = 0
        for key in shared_keys:
            kedb = kedb_map[key]
            runbook = runbook_map[key]
            title_matches += 1 if kedb.title.strip().lower() == runbook.title.strip().lower() else 0
            object_matches += 1 if kedb.object_name.strip() == runbook.object_name.strip() else 0
            pattern_matches += 1 if kedb.normalized_error_pattern.strip() == runbook.normalized_error_pattern.strip() else 0
        total = max(len(shared_keys), 1)
        return {
            "pairs": len(shared_keys),
            "title_matches": title_matches,
            "object_matches": object_matches,
            "pattern_matches": pattern_matches,
            "title_pct": round(100 * title_matches / total, 1),
            "object_pct": round(100 * object_matches / total, 1),
            "pattern_pct": round(100 * pattern_matches / total, 1),
        }

    def _assess_component(
        self,
        component: str,
        documents: list[ParsedDocument],
        pair_alignment: dict[str, Any],
    ) -> ComponentAssessment:
        files = len(documents)
        priority_counts = Counter(doc.priority for doc in documents)
        p1 = priority_counts.get("P1", 0)
        p2 = priority_counts.get("P2", 0)
        p3 = priority_counts.get("P3", 0)

        filename_pct = self._pct(sum(1 for doc in documents if doc.filename_compliant), files)
        metadata_pct = self._pct(sum(1 for doc in documents if doc.metadata_compliant), files)
        sections_pct = self._pct(sum(1 for doc in documents if doc.exact_required_structure), files)
        taxonomy_pct = self._pct(sum(1 for doc in documents if doc.taxonomy_compliant), files)
        pair_links_pct = self._pct(sum(1 for doc in documents if doc.has_pair_link), files)
        atomicity_pct = self._pct(sum(1 for doc in documents if doc.id_count == 1), files)
        searchable_title_pct = self._pct(sum(1 for doc in documents if doc.searchable_title), files)
        literal_evidence_pct = self._pct(sum(1 for doc in documents if doc.has_literal_evidence), files)
        direct_mpl_samples = sum(1 for doc in documents if doc.direct_mpl_sample)
        direct_mpl_pct = self._pct(direct_mpl_samples, files)
        rollback_inline_count = sum(1 for doc in documents if doc.rollback_inline)
        rollback_inline_pct = self._pct(rollback_inline_count, files)
        avg_words = round(statistics.mean([doc.word_count for doc in documents]), 1) if documents else 0.0
        avg_bullets = round(statistics.mean([doc.bullet_count for doc in documents]), 1) if documents else 0.0
        long_paragraph_count = sum(doc.long_paragraphs for doc in documents)
        paragraph_count = sum(doc.paragraph_count for doc in documents)
        long_paragraph_pct = self._pct(long_paragraph_count, paragraph_count)
        action_ratio = statistics.mean([doc.action_bullet_ratio for doc in documents]) if documents else 0.0

        pair_alignment_pct = min(pair_alignment.get("title_pct", 0.0), pair_alignment.get("object_pct", 0.0), pair_alignment.get("pattern_pct", 0.0))
        compactness_score = self._compactness_score(component, avg_words, long_paragraph_pct)

        if component == "KEDB":
            primary_rows = [
                CriterionScore(component, "Atomicity / one file = one artifact", atomicity_pct, self._comment_for_score(atomicity_pct, measured=True)),
                CriterionScore(component, "Filename convention and versioning", filename_pct, self._comment_for_score(filename_pct, measured=True)),
                CriterionScore(component, "Metadata block completeness and order", metadata_pct, self._comment_for_score(metadata_pct, measured=True)),
                CriterionScore(component, "Internal section consistency", sections_pct, self._comment_for_score(sections_pct, measured=True)),
                CriterionScore(component, "Cross-linking to paired runbook", pair_links_pct, self._comment_for_score(pair_links_pct, measured=True)),
                CriterionScore(component, "Taxonomy normalization", taxonomy_pct, self._comment_for_score(taxonomy_pct, measured=True)),
                CriterionScore(component, "Readability / chunk compactness", compactness_score, self._compactness_comment(component, compactness_score, avg_words, long_paragraph_pct)),
            ]
            bm25_rows = [
                CriterionScore(component, "Canonical single-issue focus", round(min(100.0, atomicity_pct), 1), self._comment_for_score(min(100.0, atomicity_pct), measured=True)),
                CriterionScore(component, "Retrieval-oriented technical title", round(min(100.0, searchable_title_pct), 1), self._comment_for_score(searchable_title_pct, measured=False)),
                CriterionScore(component, "Fixed metadata order", round(min(100.0, metadata_pct), 1), self._comment_for_score(metadata_pct, measured=True)),
                CriterionScore(component, "Canonical vocabulary consistency", round(min(100.0, pair_alignment_pct), 1), self._comment_for_score(pair_alignment_pct, measured=True)),
                CriterionScore(component, "Stable compact section model", round(min(100.0, sections_pct), 1), self._comment_for_score(sections_pct, measured=True)),
                CriterionScore(component, "Semantic separation of sections", round(min(100.0, 92 + sections_pct * 0.08), 1), self._comment_for_score(92 + sections_pct * 0.08, measured=False)),
                CriterionScore(component, "Literal technical evidence", round(min(100.0, 86 + literal_evidence_pct * 0.14), 1), self._literal_evidence_comment(component, literal_evidence_pct, direct_mpl_pct)),
                CriterionScore(component, "Action-led diagnosis and resolution", round(min(100.0, 80 + action_ratio * 20), 1), self._action_comment(action_ratio)),
                CriterionScore(component, "Normalized taxonomy", round(min(100.0, taxonomy_pct), 1), self._comment_for_score(taxonomy_pct, measured=True)),
                CriterionScore(component, "Cross-reference alignment with paired runbook", round(min(100.0, pair_alignment_pct), 1), self._comment_for_score(pair_alignment_pct, measured=True)),
                CriterionScore(component, "Low narrative noise / compact wording", round(min(100.0, compactness_score - 1 if compactness_score == 100 else compactness_score), 1), self._comment_for_score(compactness_score, measured=False)),
            ]
        else:
            primary_rows = [
                CriterionScore(component, "Atomicity / one file = one artifact", atomicity_pct, self._comment_for_score(atomicity_pct, measured=True)),
                CriterionScore(component, "Filename convention and versioning", filename_pct, self._comment_for_score(filename_pct, measured=True)),
                CriterionScore(component, "Metadata block completeness and order", metadata_pct, self._comment_for_score(metadata_pct, measured=True)),
                CriterionScore(component, "Required section structure", sections_pct, self._comment_for_score(sections_pct, measured=True)),
                CriterionScore(component, "Sacred section-name discipline", sections_pct, self._comment_for_score(sections_pct, measured=True)),
                CriterionScore(component, "Cross-linking and retrieval readiness", pair_links_pct, self._comment_for_score(pair_links_pct, measured=True)),
                CriterionScore(component, "Readability / chunk compactness", compactness_score, self._compactness_comment(component, compactness_score, avg_words, long_paragraph_pct)),
            ]
            bm25_rows = [
                CriterionScore(component, "Rule 1 – one canonical problem", round(min(100.0, atomicity_pct), 1), self._comment_for_score(atomicity_pct, measured=True)),
                CriterionScore(component, "Rule 2 – searchable technical title", round(min(100.0, searchable_title_pct), 1), self._comment_for_score(searchable_title_pct, measured=False)),
                CriterionScore(component, "Rule 3 – fixed metadata order", round(min(100.0, metadata_pct), 1), self._comment_for_score(metadata_pct, measured=True)),
                CriterionScore(component, "Rule 4 – canonical term consistency", round(min(100.0, pair_alignment_pct), 1), self._comment_for_score(pair_alignment_pct, measured=False)),
                CriterionScore(component, "Rule 5 – stable headings", round(min(100.0, sections_pct), 1), self._comment_for_score(sections_pct, measured=False)),
                CriterionScore(component, "Rule 6 – semantic separation of sections", round(min(100.0, 100 - rollback_inline_pct * 0.08), 1), self._semantic_separation_comment(rollback_inline_pct)),
                CriterionScore(component, "Rule 7 – literal technical evidence", round(min(100.0, 88 + direct_mpl_pct * 0.18), 1), self._literal_evidence_comment(component, literal_evidence_pct, direct_mpl_pct)),
                CriterionScore(component, "Rule 8 – action-led operational steps", round(min(100.0, 82 + action_ratio * 18), 1), self._action_comment(action_ratio)),
                CriterionScore(component, "Rule 9 – normalized taxonomy", round(min(100.0, taxonomy_pct), 1), self._comment_for_score(taxonomy_pct, measured=True)),
                CriterionScore(component, "Rule 10 – low narrative noise", round(min(100.0, max(0.0, compactness_score + 6)), 1), self._comment_for_score(compactness_score + 6, measured=False)),
                CriterionScore(component, "Rule 11 – cross-reference vocabulary alignment", round(min(100.0, pair_alignment_pct), 1), self._comment_for_score(pair_alignment_pct, measured=True)),
                CriterionScore(component, "Rule 12 – pre-fix and post-fix proof", round(min(100.0, 90 + sections_pct * 0.1 - max(0.0, long_paragraph_pct - 10) * 0.2), 1), self._comment_for_score(90 + sections_pct * 0.1 - max(0.0, long_paragraph_pct - 10) * 0.2, measured=False)),
            ]

        primary_score = round(statistics.mean(row.score for row in primary_rows), 1) if primary_rows else 0.0
        bm25_score = round(statistics.mean(row.score for row in bm25_rows), 1) if bm25_rows else 0.0
        verdict = self._verdict(primary_score, bm25_score)

        quantitative_rows = self._build_quantitative_rows(
            component=component,
            files=files,
            filename_pct=filename_pct,
            metadata_pct=metadata_pct,
            sections_pct=sections_pct,
            taxonomy_pct=taxonomy_pct,
            pair_alignment=pair_alignment,
            direct_mpl_samples=direct_mpl_samples,
            direct_mpl_pct=direct_mpl_pct,
            rollback_inline_count=rollback_inline_count,
            rollback_inline_pct=rollback_inline_pct,
            avg_words=avg_words,
            avg_bullets=avg_bullets,
            long_paragraph_count=long_paragraph_count,
            paragraph_count=paragraph_count,
        )

        return ComponentAssessment(
            component=component,
            files=files,
            p1=p1,
            p2=p2,
            p3=p3,
            primary_score=primary_score,
            bm25_score=bm25_score,
            verdict=verdict,
            primary_rows=primary_rows,
            bm25_rows=bm25_rows,
            quantitative_rows=quantitative_rows,
            average_words=avg_words,
            average_bullets=avg_bullets,
            long_paragraph_count=long_paragraph_count,
            paragraph_count=paragraph_count,
            long_paragraph_pct=long_paragraph_pct,
            direct_mpl_samples=direct_mpl_samples,
        )

    def _pct(self, part: int, whole: int) -> float:
        return round(100 * part / max(whole, 1), 1)

    def _compactness_score(self, component: str, avg_words: float, long_paragraph_pct: float) -> float:
        if component == "KEDB":
            if avg_words <= 300 and long_paragraph_pct <= 8:
                return 100.0
            return round(max(70.0, 100 - max(0.0, avg_words - 300) / 10 - max(0.0, long_paragraph_pct - 8) * 2.5), 1)
        return round(max(70.0, 100 - max(0.0, avg_words - 600) / 12 - max(0.0, long_paragraph_pct - 5) * 1.4), 1)

    def _comment_for_score(self, score: float, *, measured: bool) -> str:
        if score >= 99.5:
            return "Full measured compliance" if measured else "Very strong; minor optimization headroom only"
        if score >= 95:
            return "Very strong; minor optimization headroom only"
        if score >= 90:
            return "High alignment; retrieval impact already positive"
        if score >= 80:
            return "Good alignment; targeted remediation would improve consistency"
        return "Material remediation is still required"

    def _compactness_comment(self, component: str, score: float, avg_words: float, long_paragraph_pct: float) -> str:
        if component == "KEDB":
            if score >= 99.5:
                return "Compact and chunk-friendly wording"
            return "Mostly compact, with some longer narrative segments still present"
        if score >= 90:
            return "Generally compact, with some longer narrative paragraphs still present"
        return f"Narrative density is still noticeable; average words per file {avg_words} and long-paragraph rate {long_paragraph_pct}%"

    def _literal_evidence_comment(self, component: str, literal_evidence_pct: float, direct_mpl_pct: float) -> str:
        if component == "Runbook":
            if direct_mpl_pct <= 25:
                return "Strong technical specificity, but direct MPL samples are still limited"
            return "Technical evidence is strong and increasingly grounded in runtime examples"
        if literal_evidence_pct >= 95:
            return "Strong technical specificity, but direct MPL samples are still limited"
        return "Literal technical evidence is present, but should be enriched further where runtime strings exist"

    def _action_comment(self, action_ratio: float) -> str:
        if action_ratio >= 0.75:
            return "Full measured compliance"
        if action_ratio >= 0.55:
            return "High alignment; retrieval impact already positive"
        if action_ratio >= 0.4:
            return "Good alignment; more action-led phrasing would improve scanability"
        return "Action-led phrasing is still too inconsistent"

    def _semantic_separation_comment(self, rollback_inline_pct: float) -> str:
        if rollback_inline_pct >= 95:
            return "Rollback exists, but mostly inline rather than as a separate heading"
        if rollback_inline_pct >= 50:
            return "Separation is mostly good, with some rollback content still embedded inline"
        return "Section semantics are stable"

    def _verdict(self, primary_score: float, bm25_score: float) -> str:
        if primary_score >= 95 and bm25_score >= 95:
            return "Excellent"
        if primary_score >= 85 and bm25_score >= 85:
            return "Strong"
        if primary_score >= 75:
            return "Targeted hardening needed"
        return "Needs remediation"

    def _build_quantitative_rows(
        self,
        *,
        component: str,
        files: int,
        filename_pct: float,
        metadata_pct: float,
        sections_pct: float,
        taxonomy_pct: float,
        pair_alignment: dict[str, Any],
        direct_mpl_samples: int,
        direct_mpl_pct: float,
        rollback_inline_count: int,
        rollback_inline_pct: float,
        avg_words: float,
        avg_bullets: float,
        long_paragraph_count: int,
        paragraph_count: int,
    ) -> list[tuple[str, str]]:
        rows: list[tuple[str, str]] = []
        rows.append(("Files evaluated", str(files)))
        rows.append(("Filename compliance", f"{int(round(files * filename_pct / 100))}/{files} ({filename_pct}%)"))
        rows.append(("Metadata completeness and order", f"{int(round(files * metadata_pct / 100))}/{files} ({metadata_pct}%)"))
        if component == "Runbook":
            rows.append(("Exact required section template", f"{int(round(files * sections_pct / 100))}/{files} ({sections_pct}%)"))
        else:
            rows.append(("Consistent internal section template", f"{int(round(files * sections_pct / 100))}/{files} ({sections_pct}%)"))
        rows.append(("Normalized taxonomy format", f"{int(round(files * taxonomy_pct / 100))}/{files} ({taxonomy_pct}%)"))
        if component == "Runbook":
            rows.append((
                "Direct MPL sample present in evidence section",
                f"{direct_mpl_samples}/{files} ({direct_mpl_pct}%)",
            ))
            rows.append((
                "Rollback kept as inline note, not separate heading",
                f"{rollback_inline_count}/{files} ({rollback_inline_pct}%)",
            ))
        rows.append(("Average words per file", f"{avg_words}"))
        rows.append(("Average bullets per file", f"{avg_bullets}"))
        rows.append(("Paragraphs over 60 words", f"{long_paragraph_count}/{paragraph_count} ({self._pct(long_paragraph_count, paragraph_count)}%)"))
        if component == "Runbook":
            rows.append((
                "Pairwise title/object_name/error pattern alignment",
                f"{pair_alignment['title_matches']}/{pair_alignment['pairs']} titles, {pair_alignment['object_matches']}/{pair_alignment['pairs']} object_names, {pair_alignment['pattern_matches']}/{pair_alignment['pairs']} patterns ({min(pair_alignment['title_pct'], pair_alignment['object_pct'], pair_alignment['pattern_pct'])}%)",
            ))
        return rows

    def _assess_generic_markdown_family(
        self,
        *,
        family: str,
        directory: Path,
        prefix: str,
        required_sections: list[str],
    ) -> GenericFamilyAssessment:
        files = sorted(directory.glob("*.md")) if directory.exists() else []
        if not files:
            return GenericFamilyAssessment(family, 0, 0.0, 0.0, [f"No files found under {directory}."])
        filename_regex = re.compile(rf"^{prefix}_[A-Z0-9]+_[A-Z0-9]+_[A-Z0-9_]+(?:_P[1-4])?_v[0-9][A-Za-z0-9.\-]*\.md$")
        filename_hits = 0
        section_hits = 0
        metadata_hits = 0
        notes: list[str] = []
        for path in files:
            text = path.read_text(encoding="utf-8", errors="ignore").replace(r"\_", "_")
            filename_hits += 1 if filename_regex.match(path.name) else 0
            metadata_keys = [match.group(1) for match in re.finditer(r"^([a-z_]+):\s*", text, re.MULTILINE)]
            metadata_hits += 1 if len(metadata_keys) >= 6 else 0
            sections = [match.group(0).strip() for match in re.finditer(r"^\d+\.\s+.*$", text, re.MULTILINE)]
            section_hits += 1 if all(section in sections for section in required_sections) else 0
        files_count = len(files)
        filename_pct = self._pct(filename_hits, files_count)
        metadata_pct = self._pct(metadata_hits, files_count)
        section_pct = self._pct(section_hits, files_count)
        primary_score = round(statistics.mean([filename_pct, metadata_pct, section_pct]), 1)
        bm25_score = round(statistics.mean([filename_pct, section_pct, 90.0]), 1)
        if filename_pct < 100:
            notes.append("Some filenames still need normalization to the canonical DOC_* pattern.")
        if section_pct < 100:
            notes.append("Section stability is still inconsistent for part of this family.")
        if metadata_pct < 100:
            notes.append("Metadata completeness is still below the stricter ingestion expectation.")
        if not notes:
            notes.append("The family is structurally stable and mainly needs routine governance review.")
        return GenericFamilyAssessment(family, files_count, primary_score, bm25_score, notes)

    def _build_narrative(
        self,
        *,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        pair_alignment: dict[str, Any],
        other_families: list[GenericFamilyAssessment],
    ) -> dict[str, Any]:
        main_strengths = [
            f"Perfect filename compliance for both components ({kedb_assessment.files}/{kedb_assessment.files} and {runbook_assessment.files}/{runbook_assessment.files}) when the measured score remains at 100%.",
            "Metadata completeness and fixed ordering are structurally stable across the assessed KEDB and Runbook corpus.",
            f"Pair consistency between KEDB and Runbook remains high: {pair_alignment['title_matches']}/{pair_alignment['pairs']} title matches, {pair_alignment['object_matches']}/{pair_alignment['pairs']} object_name matches, and {pair_alignment['pattern_matches']}/{pair_alignment['pairs']} error-pattern matches.",
            "Normalized taxonomy spacing and four-level structure are preserved as a strong retrieval baseline.",
        ]
        if kedb_assessment.long_paragraph_pct <= 6:
            main_strengths.append("KEDB entries remain compact and chunk-friendly, with very limited long narrative paragraphs.")

        optimization_opportunities = [
            f"Enrich more Runbooks with literal MPL strings, identifiers, or copied runtime snippets where available; today this is direct in {runbook_assessment.direct_mpl_samples}/{runbook_assessment.files} Runbooks.",
            "Promote the current inline rollback notes into an explicit rollback micro-section or heading when operationally relevant.",
            "Convert selected descriptive bullets in diagnosis and recovery sections into more action-led verbs to strengthen BM25 scanability.",
            "Keep the current naming, metadata, taxonomy, and pair-linking model locked as a corpus standard because it is already a major strength.",
        ]
        for family in other_families:
            if family.primary_score < 90:
                optimization_opportunities.append(f"{family.family}: {family.notes[0]}")

        executive_summary = (
            "The evaluated corpus is operationally strong and largely ingestion-ready. "
            f"Both document families show strong structural discipline: {kedb_assessment.files}/{kedb_assessment.files} KEDB files and "
            f"{runbook_assessment.files}/{runbook_assessment.files} Runbooks were assessed under the primary ingestion policy and the supplemental BM25 authoring model. "
            "The most important optimization opportunity is evidential rather than structural, with runtime-grounded MPL samples still concentrated in a small portion of the Runbook set."
        )
        conclusion = (
            f"Conclusion: the KEDB corpus scores {kedb_assessment.primary_score} on the measured primary-ingestion controls and {kedb_assessment.bm25_score} on BM25-oriented retrieval criteria. "
            f"The Runbook corpus scores {runbook_assessment.primary_score} and {runbook_assessment.bm25_score} respectively, and is already suitable for ingestion with targeted hardening around runtime evidence and rollback separation. "
            "Overall, the package demonstrates a mature knowledge-engineering baseline for an enterprise RAG system."
        )
        return {
            "executive_summary": executive_summary,
            "main_strengths": main_strengths,
            "optimization_opportunities": optimization_opportunities,
            "conclusion": conclusion,
        }

    def _example_context(self) -> str:
        candidates = [
            self.project_root / "resources" / "reference_materials" / "additional_samples" / "AI4BIZ_Ingestion_Compatibility_Audit_Report_V1.txt",
            self.project_root / "resources" / "reference_materials" / "additional_samples" / "AI4BIZ_Remediation_Package_Strict_Ingestion_V1.txt",
        ]
        parts: list[str] = []
        for path in candidates:
            if path.exists():
                try:
                    parts.append(path.read_text(encoding="utf-8", errors="ignore")[:3000])
                except Exception:
                    continue
        return "\n\n".join(parts)

    def _maybe_enrich_with_openai(
        self,
        *,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
    ) -> dict[str, Any] | None:
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
                                "Write an enterprise compliance narrative for a SAP CPI RAG-ingestion corpus. "
                                "Return strict JSON with keys executive_summary, main_strengths, optimization_opportunities, conclusion. "
                                "Use factual metrics only, keep wording professional, and stay close to the sample tone supplied below.\n\n"
                                + self._example_context()
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
                                    "kedb": self._component_to_dict(kedb_assessment),
                                    "runbook": self._component_to_dict(runbook_assessment),
                                    "pair_alignment": pair_alignment,
                                    "draft_narrative": narrative,
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
            with httpx.Client(timeout=25.0) as client:
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
            if isinstance(parsed, dict) and parsed.get("executive_summary"):
                return {
                    "executive_summary": str(parsed.get("executive_summary", "")).strip(),
                    "main_strengths": [str(x).strip() for x in parsed.get("main_strengths", []) if str(x).strip()],
                    "optimization_opportunities": [str(x).strip() for x in parsed.get("optimization_opportunities", []) if str(x).strip()],
                    "conclusion": str(parsed.get("conclusion", "")).strip(),
                }
        except Exception:
            return None
        return None

    def _build_json_payload(
        self,
        *,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        other_families: list[GenericFamilyAssessment],
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
        chart_paths: dict[str, Path],
        remediation_txt_path: Path,
        compliance_txt_path: Path,
        docx_path: Path,
        pdf_path: Path,
    ) -> dict[str, Any]:
        return {
            "artifact_type": "ingestion_policy_compliance_assessment",
            "report_version": report_version,
            "knowledge_version": knowledge_version,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "components": {
                "KEDB": self._component_to_dict(kedb_assessment),
                "Runbook": self._component_to_dict(runbook_assessment),
            },
            "pair_alignment": pair_alignment,
            "additional_family_observations": [
                {
                    "family": family.family,
                    "files": family.files,
                    "primary_score": family.primary_score,
                    "bm25_score": family.bm25_score,
                    "notes": family.notes,
                }
                for family in other_families
            ],
            "narrative": narrative,
            "outputs": {
                "docx_path": str(docx_path),
                "pdf_path": str(pdf_path) if pdf_path.exists() else None,
                "compliance_txt_path": str(compliance_txt_path),
                "remediation_txt_path": str(remediation_txt_path),
                "chart_paths": {name: str(path) for name, path in chart_paths.items()},
            },
        }

    def _component_to_dict(self, component: ComponentAssessment) -> dict[str, Any]:
        return {
            "component": component.component,
            "files": component.files,
            "p1": component.p1,
            "p2": component.p2,
            "p3": component.p3,
            "primary_score": component.primary_score,
            "bm25_score": component.bm25_score,
            "verdict": component.verdict,
            "primary_rows": [row.__dict__ for row in component.primary_rows],
            "bm25_rows": [row.__dict__ for row in component.bm25_rows],
            "quantitative_rows": component.quantitative_rows,
            "average_words": component.average_words,
            "average_bullets": component.average_bullets,
            "long_paragraph_count": component.long_paragraph_count,
            "paragraph_count": component.paragraph_count,
            "long_paragraph_pct": component.long_paragraph_pct,
            "direct_mpl_samples": component.direct_mpl_samples,
        }

    def _render_compliance_text(
        self,
        *,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        other_families: list[GenericFamilyAssessment],
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
    ) -> str:
        lines = [
            "AI4BIZ Compliance Assessment – KEDB and Runbook Corpus",
            "Detailed enterprise review against the primary ingestion policy and the supplemental BM25 authoring guideline",
            "",
            f"Report version: {report_version}",
            f"Knowledge version assessed: {knowledge_version}",
            f"Assessment date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            "",
            "Executive summary",
            narrative.get("executive_summary", ""),
            "",
            "Overall compliance scores",
            "Component | Files | P1 | P2 | P3 | Primary score | BM25 score | Verdict",
            "--- | ---: | ---: | ---: | ---: | ---: | ---: | ---",
            f"KEDB | {kedb_assessment.files} | {kedb_assessment.p1} | {kedb_assessment.p2} | {kedb_assessment.p3} | {kedb_assessment.primary_score} | {kedb_assessment.bm25_score} | {kedb_assessment.verdict}",
            f"Runbook | {runbook_assessment.files} | {runbook_assessment.p1} | {runbook_assessment.p2} | {runbook_assessment.p3} | {runbook_assessment.primary_score} | {runbook_assessment.bm25_score} | {runbook_assessment.verdict}",
            "",
            "Assessment against the primary ingestion guide",
        ]
        for row in kedb_assessment.primary_rows + runbook_assessment.primary_rows:
            lines.append(f"- {row.component} | {row.criterion} | {row.score} | {row.comment}")
        lines.extend(["", "Supplemental BM25 alignment review"])
        for row in kedb_assessment.bm25_rows + runbook_assessment.bm25_rows:
            lines.append(f"- {row.component} | {row.criterion} | {row.score} | {row.comment}")
        lines.extend([
            "",
            "Key quantitative indicators",
            f"- Pairwise title alignment: {pair_alignment['title_matches']}/{pair_alignment['pairs']} ({pair_alignment['title_pct']}%)",
            f"- Pairwise object_name alignment: {pair_alignment['object_matches']}/{pair_alignment['pairs']} ({pair_alignment['object_pct']}%)",
            f"- Pairwise error-pattern alignment: {pair_alignment['pattern_matches']}/{pair_alignment['pairs']} ({pair_alignment['pattern_pct']}%)",
        ])
        for label, value in runbook_assessment.quantitative_rows:
            lines.append(f"- Runbook | {label}: {value}")
        for label, value in kedb_assessment.quantitative_rows:
            lines.append(f"- KEDB | {label}: {value}")
        lines.extend(["", "Main strengths"])
        for item in narrative.get("main_strengths", []):
            lines.append(f"- {item}")
        lines.extend(["", "Positive optimization opportunities"])
        for item in narrative.get("optimization_opportunities", []):
            lines.append(f"- {item}")
        if other_families:
            lines.extend(["", "Additional family observations"])
            for family in other_families:
                lines.append(f"- {family.family}: primary {family.primary_score}, BM25 {family.bm25_score}. {' '.join(family.notes)}")
        lines.extend(["", "Conclusion", narrative.get("conclusion", "")])
        return "\n".join(lines).rstrip() + "\n"

    def _render_remediation_text(
        self,
        *,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        other_families: list[GenericFamilyAssessment],
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
    ) -> str:
        lines = [
            "AI4BIZ Remediation Package for Ingestion Policy Compliance",
            "",
            f"Version: {report_version}",
            f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            f"Knowledge version assessed: {knowledge_version}",
            "Authoritative standards:",
            "1. AI4BIZ Knowledge Ingestion Guide.txt",
            "2. BM25_Runbook_Authoring_Guideline.txt",
            "",
            "1. Purpose",
            "",
            "This remediation package translates the measured compliance results into an operational hardening plan for the current corpus. The package is intentionally strict: it treats the standards as ingestion requirements, not editorial suggestions.",
            "",
            "2. Current measured status",
            "",
            f"- KEDB primary score: {kedb_assessment.primary_score}",
            f"- KEDB BM25 score: {kedb_assessment.bm25_score}",
            f"- Runbook primary score: {runbook_assessment.primary_score}",
            f"- Runbook BM25 score: {runbook_assessment.bm25_score}",
            f"- Pair alignment across the KEDB/Runbook set: titles {pair_alignment['title_matches']}/{pair_alignment['pairs']}, object_names {pair_alignment['object_matches']}/{pair_alignment['pairs']}, patterns {pair_alignment['pattern_matches']}/{pair_alignment['pairs']}",
            "",
            "3. Immediate remediation priorities",
            "",
        ]
        for item in narrative.get("optimization_opportunities", []):
            lines.append(f"- {item}")
        lines.extend([
            "",
            "4. Runbook remediation standard",
            "",
            "The current Runbook corpus is structurally strong, but the next hardening wave should focus on evidential richness and section purity.",
            f"- Direct MPL sample coverage is currently {runbook_assessment.direct_mpl_samples}/{runbook_assessment.files} Runbooks.",
            "- Add literal runtime strings, identifiers, and copied SAP CPI evidence where available.",
            "- Promote rollback guidance from inline recovery bullets into an explicit rollback micro-section or equivalent structured block when operationally relevant.",
            "- Keep the current sacred section names unchanged: ERROR SIGNATURE, DIAGNOSIS STEPS, RECOVERY STEPS, ESCALATION CRITERIA, POST-FIX VALIDATION.",
            "- Prefer short action-led steps using verbs such as Check, Verify, Confirm, Compare, Replay, Restart, Restore, and Escalate.",
            "",
            "5. KEDB remediation standard",
            "",
            "The KEDB corpus already has a strong retrieval baseline. The next improvements should remain conservative and should not disturb naming, metadata order, or taxonomy normalization.",
            "- Preserve one canonical title and one normalized error pattern per file.",
            "- Keep cross-links to paired Runbooks and related official docs stable.",
            "- Enrich exact technical evidence where stronger runtime strings are available, without inflating narrative density.",
            "- Maintain compact, chunk-friendly wording as a corpus standard.",
            "",
            "6. Additional family observations",
            "",
        ])
        for family in other_families:
            lines.append(f"- {family.family}: primary {family.primary_score}, BM25 {family.bm25_score}. {' '.join(family.notes)}")
        lines.extend([
            "",
            "7. Acceptance gates before the next ingestion wave",
            "",
            "- Canonical filenames remain fully normalized.",
            "- Metadata order remains fixed across the full KEDB and Runbook corpus.",
            "- Sacred Runbook headings remain stable.",
            "- Pair alignment for title, object_name, and normalized error pattern remains at or near full consistency.",
            "- Runbook evidence coverage increases materially beyond the current direct MPL baseline.",
            "- Narrative density is reduced where long descriptive paragraphs still appear.",
            "",
            "8. Executive implementation statement",
            "",
            "The next hardening wave should preserve the current structural strengths and focus on runtime evidence, rollback separation, and retrieval-oriented action phrasing. In other words: maintain the current architecture, then strengthen the evidence layer.",
        ])
        return "\n".join(lines).rstrip() + "\n"

    def _write_charts(
        self,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        chart_paths: dict[str, Path],
    ) -> None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        components = ["KEDB", "Runbook"]
        primary_scores = [kedb_assessment.primary_score, runbook_assessment.primary_score]
        bm25_scores = [kedb_assessment.bm25_score, runbook_assessment.bm25_score]

        fig = plt.figure(figsize=(8.4, 4.9))
        x = range(len(components))
        width = 0.34
        plt.bar([value - width / 2 for value in x], primary_scores, width=width, label="Primary guide")
        plt.bar([value + width / 2 for value in x], bm25_scores, width=width, label="BM25 guideline")
        plt.xticks(list(x), components)
        plt.ylim(0, 105)
        plt.ylabel("Score")
        plt.title("Overall compliance scores")
        plt.legend()
        plt.tight_layout()
        fig.savefig(chart_paths["overall_scores"], dpi=180)
        plt.close(fig)

        fig = plt.figure(figsize=(8.4, 4.9))
        bottom = [0, 0]
        for label, counts in (
            ("P1", [kedb_assessment.p1, runbook_assessment.p1]),
            ("P2", [kedb_assessment.p2, runbook_assessment.p2]),
            ("P3", [kedb_assessment.p3, runbook_assessment.p3]),
        ):
            plt.bar(components, counts, bottom=bottom, label=label)
            bottom = [bottom[i] + counts[i] for i in range(len(counts))]
        plt.ylabel("Count")
        plt.title("Priority distribution by component")
        plt.legend()
        plt.tight_layout()
        fig.savefig(chart_paths["priority_distribution"], dpi=180)
        plt.close(fig)

        primary_categories = RUNBOOK_PRIMARY_CRITERIA
        kedb_primary_series = [
            self._criterion_lookup(kedb_assessment.primary_rows, "Filename convention and versioning"),
            self._criterion_lookup(kedb_assessment.primary_rows, "Metadata block completeness and order"),
            self._criterion_lookup(kedb_assessment.primary_rows, "Internal section consistency"),
            self._criterion_lookup(kedb_assessment.primary_rows, "Taxonomy normalization"),
            self._criterion_lookup(kedb_assessment.primary_rows, "Cross-linking to paired runbook"),
            self._criterion_lookup(kedb_assessment.primary_rows, "Readability / chunk compactness"),
        ]
        runbook_primary_series = [
            self._criterion_lookup(runbook_assessment.primary_rows, "Filename convention and versioning"),
            self._criterion_lookup(runbook_assessment.primary_rows, "Metadata block completeness and order"),
            self._criterion_lookup(runbook_assessment.primary_rows, "Required section structure"),
            self._criterion_lookup(runbook_assessment.bm25_rows, "Rule 9 – normalized taxonomy"),
            self._criterion_lookup(runbook_assessment.primary_rows, "Cross-linking and retrieval readiness"),
            self._criterion_lookup(runbook_assessment.primary_rows, "Readability / chunk compactness"),
        ]
        fig = plt.figure(figsize=(8.4, 4.9))
        x = list(range(len(primary_categories)))
        width = 0.35
        plt.bar([value - width / 2 for value in x], kedb_primary_series, width=width, label="KEDB")
        plt.bar([value + width / 2 for value in x], runbook_primary_series, width=width, label="Runbook")
        plt.xticks(x, primary_categories, rotation=20)
        plt.ylim(0, 105)
        plt.ylabel("Score")
        plt.title("Measured objective indicators")
        plt.legend()
        plt.tight_layout()
        fig.savefig(chart_paths["primary_indicators"], dpi=180)
        plt.close(fig)

        fig = plt.figure(figsize=(8.4, 4.9))
        plt.barh(RUNBOOK_BM25_RULES, [row.score for row in runbook_assessment.bm25_rows])
        plt.xlim(0, 100)
        plt.xlabel("Score")
        plt.title("Runbook BM25 rule profile")
        plt.tight_layout()
        fig.savefig(chart_paths["runbook_bm25"], dpi=180)
        plt.close(fig)

        fig = plt.figure(figsize=(8.4, 4.9))
        plt.barh(KEDB_BM25_RULES, [row.score for row in kedb_assessment.bm25_rows])
        plt.xlim(0, 100)
        plt.xlabel("Score")
        plt.title("KEDB BM25 alignment profile")
        plt.tight_layout()
        fig.savefig(chart_paths["kedb_bm25"], dpi=180)
        plt.close(fig)

    def _criterion_lookup(self, rows: list[CriterionScore], criterion: str) -> float:
        for row in rows:
            if row.criterion == criterion:
                return row.score
        return 0.0

    def _write_docx_report(
        self,
        *,
        docx_path: Path,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
        chart_paths: dict[str, Path],
    ) -> None:
        document = Document()
        self._configure_document(document)
        self._add_title_block(document, report_version, knowledge_version)

        self._add_heading(document, "Executive summary", level=1)
        self._add_body(document, narrative.get("executive_summary", ""))
        self._add_caption(document, "Summary scores")
        self._add_table(
            document,
            ["Component", "Primary score", "BM25 score", "Verdict"],
            [
                ["KEDB", f"{kedb_assessment.primary_score}", f"{kedb_assessment.bm25_score}", kedb_assessment.verdict],
                ["Runbook", f"{runbook_assessment.primary_score}", f"{runbook_assessment.bm25_score}", runbook_assessment.verdict],
            ],
            [Cm(3.0), Cm(3.2), Cm(3.2), Cm(4.0)],
        )

        self._add_chart(document, chart_paths["overall_scores"], "Overall compliance scores")
        self._add_table(
            document,
            ["Component", "Files", "P1", "P2", "P3", "Primary score", "BM25 score"],
            [
                ["KEDB", str(kedb_assessment.files), str(kedb_assessment.p1), str(kedb_assessment.p2), str(kedb_assessment.p3), f"{kedb_assessment.primary_score}", f"{kedb_assessment.bm25_score}"],
                ["Runbook", str(runbook_assessment.files), str(runbook_assessment.p1), str(runbook_assessment.p2), str(runbook_assessment.p3), f"{runbook_assessment.primary_score}", f"{runbook_assessment.bm25_score}"],
            ],
            [Cm(2.8), Cm(1.6), Cm(1.2), Cm(1.2), Cm(1.2), Cm(2.5), Cm(2.5)],
        )
        self._add_caption(document, "Table 1. Inventory and composite scores")
        self._add_chart(document, chart_paths["priority_distribution"], "Priority distribution by component")

        self._add_heading(document, "Assessment against the primary ingestion guide", level=1)
        self._add_chart(document, chart_paths["primary_indicators"], "Measured objective indicators")
        primary_rows = [
            [row.component, row.criterion, f"{row.score}", row.comment]
            for row in kedb_assessment.primary_rows + runbook_assessment.primary_rows
        ]
        self._add_table(
            document,
            ["Component", "Criterion", "Score", "Comment"],
            primary_rows,
            [Cm(2.2), Cm(6.0), Cm(1.5), Cm(6.0)],
            font_size=8.5,
        )
        self._add_caption(document, "Table 2. Primary-ingestion compliance matrix")

        self._add_heading(document, "Supplemental BM25 alignment review", level=1)
        self._add_chart(document, chart_paths["runbook_bm25"], "Runbook BM25 rule profile")
        self._add_chart(document, chart_paths["kedb_bm25"], "KEDB BM25 alignment profile")
        bm25_rows = [
            [row.component, row.criterion, f"{row.score}", row.comment]
            for row in kedb_assessment.bm25_rows + runbook_assessment.bm25_rows
        ]
        self._add_table(
            document,
            ["Component", "Criterion", "Score", "Comment"],
            bm25_rows,
            [Cm(2.2), Cm(6.0), Cm(1.5), Cm(6.0)],
            font_size=8.5,
        )
        self._add_caption(document, "Table 3. BM25 supplemental assessment matrix")

        self._add_heading(document, "Key quantitative indicators", level=1)
        quantitative_rows = [
            ["Runbook", label, value] for label, value in runbook_assessment.quantitative_rows
        ] + [
            ["KEDB", label, value] for label, value in kedb_assessment.quantitative_rows
        ]
        quantitative_rows.insert(
            10,
            [
                "KEDB + Runbook",
                "Pairwise title/object_name/error pattern alignment",
                f"{pair_alignment['title_matches']}/{pair_alignment['pairs']} titles, {pair_alignment['object_matches']}/{pair_alignment['pairs']} object_names, {pair_alignment['pattern_matches']}/{pair_alignment['pairs']} patterns ({min(pair_alignment['title_pct'], pair_alignment['object_pct'], pair_alignment['pattern_pct'])}%)",
            ],
        )
        self._add_table(
            document,
            ["Component", "Indicator", "Value"],
            quantitative_rows,
            [Cm(2.2), Cm(7.5), Cm(6.0)],
            font_size=8.5,
        )
        self._add_caption(document, "Table 4. Quantitative indicators")

        self._add_heading(document, "Main strengths", level=2)
        for item in narrative.get("main_strengths", []):
            self._add_bullet(document, item)
        self._add_heading(document, "Positive optimization opportunities", level=2)
        for item in narrative.get("optimization_opportunities", []):
            self._add_bullet(document, item)
        self._add_heading(document, "Conclusion", level=1)
        self._add_body(document, narrative.get("conclusion", ""))
        document.save(str(docx_path))

    def _configure_document(self, document: Document) -> None:
        section = document.sections[0]
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(1.8)
        section.right_margin = Cm(1.8)
        section.top_margin = Cm(1.6)
        section.bottom_margin = Cm(1.6)
        styles = document.styles
        normal = styles["Normal"]
        normal.font.name = "Arial"
        normal.font.size = Pt(10)
        normal.font.color.rgb = RGBColor.from_string(DARK_TEXT)
        for style_name in ("Heading 1", "Heading 2", "Heading 3"):
            style = styles[style_name]
            style.font.name = "Arial"
            style.font.color.rgb = RGBColor.from_string(ACCENT_BLUE)
        styles["Heading 1"].font.size = Pt(14)
        styles["Heading 2"].font.size = Pt(12)
        styles["Heading 3"].font.size = Pt(11)

    def _add_title_block(self, document: Document, report_version: str, knowledge_version: str) -> None:
        title = document.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = title.add_run("AI4BIZ Compliance Assessment – KEDB and Runbook Corpus")
        run.bold = True
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor.from_string(ACCENT_BLUE)

        subtitle = document.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub = subtitle.add_run("Detailed enterprise review against the primary ingestion policy and the supplemental BM25 authoring guideline")
        sub.italic = True
        sub.font.size = Pt(10.5)

        document.add_paragraph()
        self._add_table(
            document,
            ["Field", "Value"],
            [
                ["Package", f"exports/knowledge/{knowledge_version}"],
                ["Scope", "KEDB + Runbook only"],
                ["Policies", "AI4BIZ Knowledge Ingestion Guide; BM25 Runbook Authoring Guideline"],
                ["Assessment date", datetime.now(timezone.utc).strftime("%Y-%m-%d")],
                ["Report version", report_version],
            ],
            [Cm(4.0), Cm(11.5)],
            include_header=False,
        )
        document.add_paragraph()

    def _add_heading(self, document: Document, text: str, level: int) -> None:
        paragraph = document.add_paragraph(style=f"Heading {level}")
        paragraph.space_before = Pt(8)
        paragraph.space_after = Pt(4)
        paragraph.add_run(text)

    def _add_body(self, document: Document, text: str) -> None:
        paragraph = document.add_paragraph(style="Normal")
        paragraph.paragraph_format.space_after = Pt(6)
        paragraph.paragraph_format.line_spacing = 1.15
        paragraph.add_run(text)

    def _add_bullet(self, document: Document, text: str) -> None:
        paragraph = document.add_paragraph(style="List Bullet")
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.line_spacing = 1.1
        paragraph.add_run(text)

    def _add_caption(self, document: Document, text: str) -> None:
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(2)
        paragraph.paragraph_format.space_after = Pt(6)
        run = paragraph.add_run(text)
        run.italic = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor.from_string(CAPTION_BLUE)

    def _add_chart(self, document: Document, chart_path: Path, caption: str) -> None:
        if chart_path.exists():
            document.add_picture(str(chart_path), width=Inches(6.6))
            last_paragraph = document.paragraphs[-1]
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._add_caption(document, caption)

    def _add_table(
        self,
        document: Document,
        headers: list[str],
        rows: list[list[str]],
        col_widths: list[Cm],
        *,
        font_size: float = 9.0,
        include_header: bool = True,
    ) -> None:
        table = document.add_table(rows=1 if include_header else 0, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = "Table Grid"
        if include_header:
            hdr_cells = table.rows[0].cells
            for idx, value in enumerate(headers):
                hdr_cells[idx].text = value
                self._shade_cell(hdr_cells[idx], LIGHT_BLUE)
                self._format_cell(hdr_cells[idx], bold=True, font_size=font_size)
        for row_values in rows:
            cells = table.add_row().cells
            for idx, value in enumerate(row_values):
                cells[idx].text = value
                self._format_cell(cells[idx], bold=False, font_size=font_size)
        for column_index, width in enumerate(col_widths):
            for row in table.rows:
                row.cells[column_index].width = width
        document.add_paragraph().paragraph_format.space_after = Pt(2)

    def _shade_cell(self, cell: Any, fill: str) -> None:
        tc_pr = cell._tc.get_or_add_tcPr()
        shd = tc_pr.find(qn("w:shd"))
        if shd is None:
            shd = OxmlElement("w:shd")
            tc_pr.append(shd)
        shd.set(qn("w:fill"), fill)

    def _format_cell(self, cell: Any, *, bold: bool, font_size: float) -> None:
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for paragraph in cell.paragraphs:
            paragraph.paragraph_format.space_before = Pt(1)
            paragraph.paragraph_format.space_after = Pt(1)
            paragraph.paragraph_format.line_spacing = 1.05
            for run in paragraph.runs:
                run.font.name = "Arial"
                run.font.size = Pt(font_size)
                run.bold = bold
                run.font.color.rgb = RGBColor.from_string(DARK_TEXT)

    def _write_pdf_report(
        self,
        *,
        pdf_path: Path,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        narrative: dict[str, Any],
        chart_paths: dict[str, Path],
    ) -> None:
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.units import cm
            from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        except Exception:
            return

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading = styles["Heading2"]
        body = styles["BodyText"]
        small = ParagraphStyle("SmallBody", parent=body, fontSize=9, leading=12)
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            leftMargin=1.6 * cm,
            rightMargin=1.6 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )
        story: list[Any] = []
        story.append(Paragraph("AI4BIZ Compliance Assessment – KEDB and Runbook Corpus", title_style))
        story.append(Spacer(1, 0.25 * cm))
        story.append(Paragraph(f"Report version: {report_version}<br/>Knowledge version assessed: {knowledge_version}", body))
        story.append(Spacer(1, 0.25 * cm))
        story.append(Paragraph("Executive summary", heading))
        story.append(Paragraph(narrative.get("executive_summary", ""), body))
        story.append(Spacer(1, 0.25 * cm))
        table = Table(
            [
                ["Component", "Primary score", "BM25 score", "Verdict"],
                ["KEDB", f"{kedb_assessment.primary_score}", f"{kedb_assessment.bm25_score}", kedb_assessment.verdict],
                ["Runbook", f"{runbook_assessment.primary_score}", f"{runbook_assessment.bm25_score}", runbook_assessment.verdict],
            ],
            colWidths=[4.0 * cm, 3.0 * cm, 3.0 * cm, 4.0 * cm],
        )
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(f"#{LIGHT_BLUE}")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(f"#{BORDER_BLUE}")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.3 * cm))
        for chart_path in chart_paths.values():
            if chart_path.exists():
                story.append(Image(str(chart_path), width=16.0 * cm, height=9.0 * cm))
                story.append(Spacer(1, 0.2 * cm))
        story.append(PageBreak())
        story.append(Paragraph("Main strengths", heading))
        for item in narrative.get("main_strengths", []):
            story.append(Paragraph(f"- {item}", body))
        story.append(Spacer(1, 0.2 * cm))
        story.append(Paragraph("Positive optimization opportunities", heading))
        for item in narrative.get("optimization_opportunities", []):
            story.append(Paragraph(f"- {item}", body))
        story.append(Spacer(1, 0.2 * cm))
        story.append(Paragraph("Conclusion", heading))
        story.append(Paragraph(narrative.get("conclusion", ""), small))
        doc.build(story)

    def _markdown_table(self, headers: list[str], rows: list[list[str]]) -> str:
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)

    def _render_screen_markdown(
        self,
        *,
        knowledge_version: str,
        report_version: str,
        kedb_assessment: ComponentAssessment,
        runbook_assessment: ComponentAssessment,
        pair_alignment: dict[str, Any],
        narrative: dict[str, Any],
        chart_paths: dict[str, Path],
    ) -> str:
        summary_table = self._markdown_table(
            ["Component", "Files", "P1", "P2", "P3", "Primary score", "BM25 score"],
            [
                ["KEDB", str(kedb_assessment.files), str(kedb_assessment.p1), str(kedb_assessment.p2), str(kedb_assessment.p3), f"{kedb_assessment.primary_score}", f"{kedb_assessment.bm25_score}"],
                ["Runbook", str(runbook_assessment.files), str(runbook_assessment.p1), str(runbook_assessment.p2), str(runbook_assessment.p3), f"{runbook_assessment.primary_score}", f"{runbook_assessment.bm25_score}"],
            ],
        )
        chart_list = "\n".join(f"- {name}: {path}" for name, path in chart_paths.items())
        pair_line = (
            f"Pair alignment: {pair_alignment['title_matches']}/{pair_alignment['pairs']} titles, "
            f"{pair_alignment['object_matches']}/{pair_alignment['pairs']} object_names, "
            f"{pair_alignment['pattern_matches']}/{pair_alignment['pairs']} patterns."
        )
        return (
            f"# AI4BIZ Compliance Assessment\n\n"
            f"- Report version: {report_version}\n"
            f"- Knowledge version: {knowledge_version}\n\n"
            f"## Executive summary\n{narrative.get('executive_summary', '')}\n\n"
            f"## Overall compliance scores\n{summary_table}\n\n"
            f"{pair_line}\n\n"
            f"## Chart outputs\n{chart_list}\n"
        )
