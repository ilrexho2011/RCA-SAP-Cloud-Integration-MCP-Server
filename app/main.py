from mcp.server.fastmcp import FastMCP

from app.config import settings
from app.dependencies import docx_service, iflow_parser, sap_client, scoring_service
from app.tools.analysis import register_analysis_tools
from app.tools.catalog import register_catalog_tools
from app.tools.documentation import register_documentation_tools
from app.tools.quality import register_quality_tools

mcp = FastMCP(settings.mcp_server_name, json_response=True)

register_catalog_tools(mcp, sap_client)
register_analysis_tools(mcp, sap_client, iflow_parser)
register_documentation_tools(
    mcp, sap_client, iflow_parser, docx_service, scoring_service)
register_quality_tools(mcp, sap_client, iflow_parser, scoring_service)

if __name__ == "__main__":
    mcp.run(transport=settings.mcp_transport)
