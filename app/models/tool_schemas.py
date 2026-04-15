from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class PackageSummary(BaseModel):
    package_id: str = Field(..., description="Technical package ID")
    name: str = Field(..., description="Package display name")
    short_text: str | None = Field(
        default=None, description="Short description")
    artifact_count: int | None = Field(
        default=None, description="Number of artifacts if known")


class CatalogPackagesResponse(BaseModel):
    total: int
    packages: list[PackageSummary]


class IFlowSummary(BaseModel):
    iflow_id: str
    name: str
    package_id: str | None = None
    version: str | None = None
    deployed: bool | None = None


class CatalogIFlowsResponse(BaseModel):
    total: int
    iflows: list[IFlowSummary]


class AnalyzeIFlowRequest(BaseModel):
    package_id: str | None = None
    iflow_id: str
    include_security: bool = True
    include_dependencies: bool = True


class AnalyzeIFlowResponse(BaseModel):
    iflow_id: str
    name: str | None = None
    summary: str
    sender_systems: list[str] = []
    receiver_systems: list[str] = []
    protocols: list[str] = []
    authentication: list[str] = []
    dependencies: list[str] = []
    raw_metadata: dict[str, Any] = {}


class GenerateDocxRequest(BaseModel):
    package_id: str | None = None
    iflow_id: str
    template_name: str = "sap_enterprise_v1"
    include_cover_page: bool = True
    include_findings: bool = True


class GenerateDocxResponse(BaseModel):
    iflow_id: str
    output_path: str
    filename: str
    sections: list[str]


class QualityIssue(BaseModel):
    category: str
    severity: Literal["critical", "high", "medium", "low"]
    points_deducted: int
    message: str
    recommendation: str


class QualityScoreResponse(BaseModel):
    iflow_id: str
    score: int
    max_score: int = 100
    issues: list[QualityIssue]
    summary: str
