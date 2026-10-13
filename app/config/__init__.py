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

    sap_cpi_base_url: str = Field(default="", alias="SAP_CPI_BASE_URL")
    sap_token_url: str = Field(default="", alias="SAP_TOKEN_URL")
    sap_client_id: str = Field(default="", alias="SAP_CLIENT_ID")
    sap_client_secret: str = Field(default="", alias="SAP_CLIENT_SECRET")
    sap_scope: str | None = Field(default=None, alias="SAP_SCOPE")
    sap_verify_ssl: bool = Field(default=True, alias="SAP_VERIFY_SSL")
    sap_timeout_seconds: int = Field(default=60, alias="SAP_TIMEOUT_SECONDS")
    sap_connect_timeout_seconds: float | None = Field(default=None, alias="SAP_CONNECT_TIMEOUT_SECONDS")
    sap_read_timeout_seconds: float | None = Field(default=None, alias="SAP_READ_TIMEOUT_SECONDS")
    sap_write_timeout_seconds: float | None = Field(default=None, alias="SAP_WRITE_TIMEOUT_SECONDS")
    sap_pool_timeout_seconds: float | None = Field(default=None, alias="SAP_POOL_TIMEOUT_SECONDS")

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

    mpl_default_lookback_hours: int = Field(default=168, alias="MPL_DEFAULT_LOOKBACK_HOURS")
    mpl_default_limit: int = Field(default=250, alias="MPL_DEFAULT_LIMIT")
    mpl_local_json_dir: str | None = Field(default=None, alias="MPL_LOCAL_JSON_DIR")
    knowledge_staging_dir: str = Field(default="./exports/knowledge/staging", alias="KNOWLEDGE_STAGING_DIR")

    knowledge_output_dir: str = Field(
        default="./exports/knowledge", alias="KNOWLEDGE_OUTPUT_DIR")
    knowledge_examples_dir: str = Field(
        default="./resources/examples", alias="KNOWLEDGE_EXAMPLES_DIR")
    default_environment: str = Field(default="demo", alias="DEFAULT_ENVIRONMENT")
    default_customer_id: str = Field(default="RCMO", alias="DEFAULT_CUSTOMER_ID")
    default_system_id: str = Field(default="CPI-RCMO", alias="DEFAULT_SYSTEM_ID")
    default_sap_sid: str = Field(default="CPI", alias="DEFAULT_SAP_SID")
    default_review_cycle: str = Field(default="monthly", alias="DEFAULT_REVIEW_CYCLE")

    knowledge_inventory_path: str | None = Field(default=None, alias="KNOWLEDGE_INVENTORY_PATH")
    knowledge_enterprise_error_catalog_path: str | None = Field(default=None, alias="KNOWLEDGE_ENTERPRISE_ERROR_CATALOG_PATH")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    openai_base_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_BASE_URL")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")


settings = Settings()
