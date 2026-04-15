from __future__ import annotations

from app.models.tool_schemas import QualityScoreResponse
from app.services.iflow_parser import IFlowParser
from app.services.sap_client import SAPClient
from app.services.scoring_service import ScoringService


def register_quality_tools(
    mcp,
    sap_client: SAPClient,
    iflow_parser: IFlowParser,
    scoring_service: ScoringService,
) -> None:
    @mcp.tool()
    async def score_iflow_quality(
        iflow_id: str,
        package_id: str | None = None,
        rule_set: str = "enterprise15",
    ) -> dict:
        """
        Detect anti-patterns and calculate a quality score from 0 to 100 for an SAP CPI iFlow.
        """
        artifact = await sap_client.get_iflow_content(iflow_id=iflow_id)
        analysis = iflow_parser.parse(artifact)
        scored = scoring_service.score_iflow(
            iflow_id=iflow_id, analysis=analysis)

        return QualityScoreResponse(**scored).model_dump()
