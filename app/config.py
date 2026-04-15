from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mcp_server_name: str = Field(
        default="SAP CPI MCP Server", alias="MCP_SERVER_NAME")
    mcp_transport: str = Field(
        default="streamable-http", alias="MCP_TRANSPORT")
    mcp_host: str = Field(default="0.0.0.0", alias="MCP_HOST")
    mcp_port: int = Field(default=8000, alias="MCP_PORT")
    mcp_mount_path: str = Field(default="/mcp", alias="MCP_MOUNT_PATH")
    mcp_api_key: str | None = Field(default=None, alias="MCP_API_KEY")
    mcp_require_api_key: bool = Field(
        default=False, alias="MCP_REQUIRE_API_KEY")

    sap_cpi_base_url: str = Field(..., alias="SAP_CPI_BASE_URL")
    sap_token_url: str = Field(..., alias="SAP_TOKEN_URL")
    sap_client_id: str = Field(..., alias="SAP_CLIENT_ID")
    sap_client_secret: str = Field(..., alias="SAP_CLIENT_SECRET")
    sap_scope: str | None = Field(default=None, alias="SAP_SCOPE")
    sap_verify_ssl: bool = Field(default=True, alias="SAP_VERIFY_SSL")
    sap_timeout_seconds: int = Field(default=60, alias="SAP_TIMEOUT_SECONDS")

    sap_packages_path: str = Field(
        default="/api/v1/IntegrationPackages", alias="SAP_PACKAGES_PATH")
    sap_iflows_path: str = Field(
        default="/api/v1/IntegrationDesigntimeArtifacts", alias="SAP_IFLOWS_PATH")
    sap_artifact_content_path_template: str = Field(
        default="/api/v1/IntegrationDesigntimeArtifacts(Id='{artifact_id}',Version='active')/$value",
        alias="SAP_ARTIFACT_CONTENT_PATH_TEMPLATE",
    )

    docx_output_dir: str = Field(
        default="./exports/docx", alias="DOCX_OUTPUT_DIR")
    docx_company_name: str = Field(
        default="RealCore", alias="DOCX_COMPANY_NAME")
    docx_template_name: str = Field(
        default="sap_enterprise_v1", alias="DOCX_TEMPLATE_NAME")

    quality_max_score: int = Field(default=100, alias="QUALITY_MAX_SCORE")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")


settings = Settings()
