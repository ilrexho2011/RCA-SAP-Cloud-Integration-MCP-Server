from __future__ import annotations

from app.models.tool_schemas import AnalyzeIFlowResponse
from app.services.iflow_parser import IFlowParser
from app.services.sap_client import SAPClient


def register_analysis_tools(mcp, sap_client: SAPClient, iflow_parser: IFlowParser) -> None:
    @mcp.tool()
    async def analyze_iflow(
        iflow_id: str,
        package_id: str | None = None,
        include_security: bool = True,
        include_dependencies: bool = True,
    ) -> dict:
        """
        Analyze an SAP CPI iFlow and explain what it does, which systems it connects,
        and how it authenticates.
        """
        artifact = await sap_client.get_iflow_content(iflow_id=iflow_id)
        parsed = iflow_parser.parse(artifact)

        if not include_security:
            parsed["authentication"] = []

        if not include_dependencies:
            parsed["dependencies"] = []

        response = AnalyzeIFlowResponse(
            iflow_id=iflow_id,
            name=artifact.get("name"),
            summary=parsed["summary"],
            sender_systems=parsed["sender_systems"],
            receiver_systems=parsed["receiver_systems"],
            protocols=parsed["protocols"],
            authentication=parsed["authentication"],
            dependencies=parsed["dependencies"],
            raw_metadata=parsed["raw_metadata"],
        )
        return response.model_dump()
