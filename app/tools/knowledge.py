from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field

from app.services.ingestion_policy_compliance_service import IngestionPolicyComplianceService
from app.services.knowledge_generation_service import KnowledgeGenerationService


class VersionSelectionForm(BaseModel):
    version: str = Field(
        default="v1",
        description="Choose the target documentation version, for example v1, v2, or v2.1.",
    )


async def _resolve_version(version: str | None, ctx: Context | None, purpose: str) -> str:
    cleaned = (version or "").strip()
    if cleaned:
        return cleaned
    if ctx is None:
        raise ValueError(
            f"Version is required for {purpose}. Provide values such as v1, v2, or v2.1."
        )
    try:
        result = await ctx.elicit(
            message=(
                f"Choose the generation version for {purpose}. "
                "Use a value such as v1, v2, or v2.1."
            ),
            schema=VersionSelectionForm,
        )
    except Exception as exc:  # pragma: no cover - depends on client support
        raise ValueError(
            f"Interactive version selection is not available in this MCP client. "
            f"Please pass 'version' explicitly for {purpose}. Technical note: {exc}"
        ) from exc
    if result.action == "accept" and result.data:
        return str(result.data.version)
    raise ValueError(f"Version selection was cancelled for {purpose}.")



def register_knowledge_tools(
    mcp: Any,
    knowledge_service: KnowledgeGenerationService,
    compliance_service: IngestionPolicyComplianceService,
) -> None:
    @mcp.tool()
    async def generate_interface_catalogs(
        version: str | None = None,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Generate enterprise Interface Catalog markdown files for the selected CPI tenant scope.

        Output is post-processed through the interface-catalog formatter layer so the final markdown matches the approved reference style.

        If version is omitted and the client supports MCP elicitation, the server asks the user
        to choose the version interactively.
        """
        resolved_version = await _resolve_version(version, ctx, "interface catalog generation")
        return await knowledge_service.generate_interface_catalogs(
            version=resolved_version,
            package_id=package_id,
            iflow_ids=iflow_ids,
            output_dir=output_dir,
        )

    @mcp.tool()
    async def generate_kedb_documents(
        version: str | None = None,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
        use_mpl: bool = False,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Generate new enterprise KEDB markdown documents for the selected CPI tenant scope.

        The generation can be enriched with MPL runtime evidence for stronger semantic coverage.
        """
        resolved_version = await _resolve_version(version, ctx, "KEDB generation")
        return await knowledge_service.generate_kedb_documents(
            version=resolved_version,
            package_id=package_id,
            iflow_ids=iflow_ids,
            output_dir=output_dir,
            use_mpl=use_mpl,
            mpl_hours=mpl_hours,
            mpl_limit=mpl_limit,
        )

    @mcp.tool()
    async def generate_runbook_documents(
        version: str | None = None,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        output_dir: str | None = None,
        use_mpl: bool = False,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Generate new enterprise Runbook markdown documents for the selected CPI tenant scope.

        The generation can be enriched with MPL runtime evidence for stronger semantic coverage.
        """
        resolved_version = await _resolve_version(version, ctx, "Runbook generation")
        return await knowledge_service.generate_runbook_documents(
            version=resolved_version,
            package_id=package_id,
            iflow_ids=iflow_ids,
            output_dir=output_dir,
            use_mpl=use_mpl,
            mpl_hours=mpl_hours,
            mpl_limit=mpl_limit,
        )

    @mcp.tool()
    async def update_kedb_documents(
        version: str | None = None,
        source_dir: str | None = None,
        source_zip_path: str | None = None,
        output_dir: str | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Update existing enterprise KEDB markdown documents and normalize them to the same
        structure, naming, and taxonomy rules used by the reference corpus.

        You can pass either a source directory or a ZIP path directly.
        """
        resolved_version = await _resolve_version(version, ctx, "KEDB update")
        return knowledge_service.update_kedb_documents(
            version=resolved_version,
            source_dir=source_dir,
            source_zip_path=source_zip_path,
            output_dir=output_dir,
        )

    @mcp.tool()
    async def update_runbook_documents(
        version: str | None = None,
        source_dir: str | None = None,
        source_zip_path: str | None = None,
        output_dir: str | None = None,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Update existing enterprise Runbook markdown documents and normalize them to the
        approved ingestion-policy and BM25 authoring structure.

        You can pass either a source directory or a ZIP path directly.
        """
        resolved_version = await _resolve_version(version, ctx, "Runbook update")
        return knowledge_service.update_runbook_documents(
            version=resolved_version,
            source_dir=source_dir,
            source_zip_path=source_zip_path,
            output_dir=output_dir,
        )

    @mcp.tool()
    async def generate_knowledge_output_bundle(
        version: str | None = None,
        package_id: str | None = None,
        iflow_ids: list[str] | None = None,
        kedb_zip_path: str | None = None,
        runbook_zip_path: str | None = None,
        output_dir: str | None = None,
        use_mpl: bool = False,
        mpl_hours: int | None = None,
        mpl_limit: int | None = None,
        include_interface_catalogs: bool = True,
        include_new_kedb: bool = True,
        include_new_runbooks: bool = True,
        include_updated_kedb: bool = True,
        include_updated_runbooks: bool = True,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Build one combined knowledge-output package from the selected tenant scope.

        The bundle can include interface catalogs, newly generated KEDB and Runbooks,
        plus updated corpora loaded directly from kedb.zip and runbooks.zip.
        """
        resolved_version = await _resolve_version(version, ctx, "combined knowledge-output bundle")
        return await knowledge_service.generate_knowledge_output_bundle(
            version=resolved_version,
            package_id=package_id,
            iflow_ids=iflow_ids,
            kedb_zip_path=kedb_zip_path,
            runbook_zip_path=runbook_zip_path,
            output_dir=output_dir,
            use_mpl=use_mpl,
            mpl_hours=mpl_hours,
            mpl_limit=mpl_limit,
            include_interface_catalogs=include_interface_catalogs,
            include_new_kedb=include_new_kedb,
            include_new_runbooks=include_new_runbooks,
            include_updated_kedb=include_updated_kedb,
            include_updated_runbooks=include_updated_runbooks,
        )

    @mcp.tool()
    async def assess_ingestion_policy_compliance(
        version: str | None = None,
        knowledge_version: str | None = None,
        source_root: str | None = None,
        output_dir: str | None = None,
        use_openai: bool = True,
        ctx: Context | None = None,
    ) -> dict[str, Any]:
        """
        Assess the generated KEDB, Runbooks, Interface Catalogs, and Official Docs against
        the packaged AI4BIZ ingestion policy and BM25-oriented retrieval expectations.

        The tool returns a structured on-screen summary and exports DOCX, TXT, remediation TXT,
        JSON, optional PDF, and PNG chart assets.
        """
        resolved_version = await _resolve_version(version, ctx, "ingestion-policy compliance assessment")
        return compliance_service.assess_ingestion_policy_compliance(
            version=resolved_version,
            knowledge_version=knowledge_version,
            source_root=source_root,
            output_dir=output_dir,
            use_openai=use_openai,
        )
