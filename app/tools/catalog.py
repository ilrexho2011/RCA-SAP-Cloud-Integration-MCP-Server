from __future__ import annotations

from app.models.tool_schemas import CatalogIFlowsResponse, CatalogPackagesResponse, IFlowSummary, PackageSummary
from app.services.sap_client import SAPClient


def register_catalog_tools(mcp, sap_client: SAPClient) -> None:
    @mcp.tool()
    async def catalog_packages(
        name_contains: str | None = None,
        package_id: str | None = None,
    ) -> dict:
        """
        List SAP Cloud Integration packages, optionally filtered by name or ID.
        """
        raw = await sap_client.list_packages(name_contains=name_contains, package_id=package_id)

        packages = [
            PackageSummary(
                package_id=item["Id"],
                name=item["Name"],
                short_text=item.get("ShortText"),
                artifact_count=item.get("ArtifactCount"),
            ).model_dump()
            for item in raw["items"]
        ]

        return CatalogPackagesResponse(total=raw["count"], packages=packages).model_dump()

    @mcp.tool()
    async def catalog_iflows(
        package_id: str | None = None,
        iflow_name_contains: str | None = None,
        iflow_id: str | None = None,
    ) -> dict:
        """
        List integration flows (iFlows), optionally filtered by package, name, or ID.
        """
        raw = await sap_client.list_iflows(
            package_id=package_id,
            iflow_name_contains=iflow_name_contains,
            iflow_id=iflow_id,
        )

        iflows = [
            IFlowSummary(
                iflow_id=item["Id"],
                name=item["Name"],
                package_id=item.get("PackageId"),
                version=item.get("Version"),
                deployed=item.get("Deployed"),
            ).model_dump()
            for item in raw["items"]
        ]

        return CatalogIFlowsResponse(total=raw["count"], iflows=iflows).model_dump()
