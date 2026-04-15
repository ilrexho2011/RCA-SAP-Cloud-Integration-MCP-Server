from app.config import settings
from app.services.docx_service import DocxService
from app.services.iflow_parser import IFlowParser
from app.services.sap_client import SAPClient
from app.services.scoring_service import ScoringService

sap_client = SAPClient(settings=settings)
iflow_parser = IFlowParser()
docx_service = DocxService(settings=settings)
scoring_service = ScoringService(max_score=settings.quality_max_score)
