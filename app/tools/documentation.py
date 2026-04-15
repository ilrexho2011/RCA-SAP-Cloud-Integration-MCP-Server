from __future__ import annotations

from app.models.tool_schemas import AnalyzeIFlowResponse, GenerateDocxResponse
from app.services.docx_service import DocxService
from app.services.iflow_parser import IFlowParser
from app.services.sap_client import SAPClient
from app.services.scoring_service import ScoringService


def register_documentation_tools(
    mcp,
    sap_client: SAPClient,
    iflow_parser: IFlowParser,
    docx_service: DocxService,
    scoring_service: ScoringService,
) -> None:
    @mcp.tool()
    async def generate_iflow_docx(
        iflow_id: str,
        package_id: str | None = None,
        template_name: str = "sap_enterprise_v1",
        include_cover_page: bool = True,
        include_findings: bool = True,
    ) -> dict:
        """
        Generate enterprise Word documentation (.docx) for an SAP CPI iFlow.
        """
        artifact = await sap_client.get_iflow_content(iflow_id=iflow_id)
        analysis = iflow_parser.parse(artifact)

        quality = None
        if include_findings:
            quality = scoring_service.score_iflow(
                iflow_id=iflow_id, analysis=analysis)

        result = docx_service.generate_iflow_docx(
            iflow_id=iflow_id,
            analysis=analysis,
            quality=quality,
        )

        response = GenerateDocxResponse(
            iflow_id=iflow_id,
            output_path=result["output_path"],
            filename=result["filename"],
            sections=result["sections"],
        )
        return response.model_dump()
