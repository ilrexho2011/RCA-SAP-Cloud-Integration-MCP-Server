from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

try:
    from scoring_service_enterprise import ScoringService
except Exception:
    ScoringService = None  # type: ignore[assignment]


@dataclass
class SectionBlock:
    """Structured block that a documentation service can render to DOCX/HTML/Markdown."""

    kind: str
    title: str
    content: Any


class EnterpriseScoringDocumentationAdapter:
    """Bridge between ScoringService output and documentation/MCP output.

    This adapter provides three integration paths:
    1. build_documentation_payload(...) -> structured blocks for documentation_service.py
    2. append_to_docx(...)            -> direct python-docx rendering helper
    3. build_mcp_output(...)          -> normalized JSON payload for MCP tool output

    The adapter preserves the distinction between zip_based and metadata_only
    so documentation can include the correct audit posture and visibility note.
    """

    def __init__(self, scoring_service: Any | None = None) -> None:
        if scoring_service is not None:
            self.scoring_service = scoring_service
        elif ScoringService is not None:
            self.scoring_service = ScoringService()
        else:
            self.scoring_service = None

    def ensure_scored(self, iflow_id: str, analysis: dict[str, Any], scoring_result: dict[str, Any] | None = None) -> dict[str, Any]:
        if scoring_result is not None:
            return scoring_result
        if self.scoring_service is None:
            raise RuntimeError(
                "No scoring service instance is available. Pass scoring_result explicitly or make scoring_service_enterprise.py importable."
            )
        return self.scoring_service.score_iflow(iflow_id, analysis)

    def build_documentation_payload(
        self,
        iflow_id: str,
        analysis: dict[str, Any],
        scoring_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        score = self.ensure_scored(iflow_id, analysis, scoring_result)
        analysis_mode = score.get("analysis_mode") or analysis.get("analysis_mode") or "unknown"
        audit_output = score.get("audit_output", {})
        evidence = score.get("evidence_coverage", {})

        payload = {
            "iflow_id": iflow_id,
            "generated_at_utc": self._utc_now(),
            "analysis_mode": analysis_mode,
            "documentation_title": f"Technical Assessment - {iflow_id}",
            "executive_scorecard": {
                "score": score.get("score"),
                "max_score": score.get("max_score"),
                "confidence_level": score.get("confidence_level"),
                "confidence_score": score.get("confidence_score"),
                "evidence_coverage_percentage": evidence.get("percentage"),
                "evidence_coverage_status": evidence.get("status"),
                "quality_gate": audit_output.get("quality_gate"),
                "documentation_ready": audit_output.get("documentation_ready"),
                "recommended_next_step": audit_output.get("recommended_next_step"),
            },
            "narratives": {
                "analysis_summary": score.get("summary") or analysis.get("summary") or "",
                "audit_narrative": audit_output.get("audit_narrative", ""),
                "visibility_note": self._visibility_note(analysis_mode),
            },
            "tables": {
                "weighted_scoring_matrix": self._matrix_rows(score),
                "issues": self._issue_rows(score),
                "anti_pattern_categories": self._anti_pattern_rows(score),
                "evidence_coverage_signals": self._coverage_rows(score),
            },
            "appendix": {
                "package_name": self._safe_get(score, "audit_output", "mcp_documentation", "package_name")
                or analysis.get("package_name")
                or analysis.get("package"),
                "resolved_version": self._safe_get(score, "audit_output", "mcp_documentation", "resolved_version")
                or analysis.get("resolved_version")
                or analysis.get("version"),
                "protocols": self._normalized_join(analysis.get("protocols")),
                "authentication": self._normalized_join(analysis.get("authentication")),
                "sender_systems": self._normalized_join(analysis.get("sender_systems")),
                "receiver_systems": self._normalized_join(analysis.get("receiver_systems")),
            },
        }

        payload["section_blocks"] = self._build_section_blocks(payload)
        return payload

    def build_mcp_output(
        self,
        iflow_id: str,
        analysis: dict[str, Any],
        scoring_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        score = self.ensure_scored(iflow_id, analysis, scoring_result)
        payload = self.build_documentation_payload(iflow_id, analysis, score)

        return {
            "tool": "analyze_iflow",
            "version": "1.0.0",
            "generated_at_utc": payload["generated_at_utc"],
            "iflow": {
                "id": iflow_id,
                "analysis_mode": payload["analysis_mode"],
                "package_name": payload["appendix"]["package_name"],
                "resolved_version": payload["appendix"]["resolved_version"],
                "summary": payload["narratives"]["analysis_summary"],
            },
            "scoring": {
                "profile": score.get("scoring_profile"),
                "score": score.get("score"),
                "max_score": score.get("max_score"),
                "raw_score_100": score.get("raw_score_100"),
                "confidence_level": score.get("confidence_level"),
                "confidence_score": score.get("confidence_score"),
                "evidence_coverage": score.get("evidence_coverage", {}),
                "anti_pattern_categories": score.get("anti_pattern_categories", []),
                "weighted_scoring_matrix": score.get("weighted_scoring_matrix", []),
                "issues": score.get("issues", []),
            },
            "audit": score.get("audit_output", {}),
            "documentation": {
                "visibility_note": payload["narratives"]["visibility_note"],
                "section_blocks": [
                    {"kind": block.kind, "title": block.title, "content": block.content}
                    for block in payload["section_blocks"]
                ],
            },
        }

    def append_to_docx(
        self,
        document: Any,
        iflow_id: str,
        analysis: dict[str, Any],
        scoring_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Append enterprise scoring content directly to a python-docx Document.

        Returns the same documentation payload used to render the section.
        """
        payload = self.build_documentation_payload(iflow_id, analysis, scoring_result)
        blocks = payload["section_blocks"]

        document.add_heading("Enterprise Scoring and Audit Assessment", level=1)
        for block in blocks:
            document.add_heading(block.title, level=2)
            if block.kind == "paragraph":
                document.add_paragraph(str(block.content))
            elif block.kind == "bullets":
                for item in block.content:
                    document.add_paragraph(str(item), style="List Bullet")
            elif block.kind == "key_value":
                table = document.add_table(rows=1, cols=2)
                table.style = "Table Grid"
                hdr = table.rows[0].cells
                hdr[0].text = "Metric"
                hdr[1].text = "Value"
                for item in block.content:
                    row = table.rows[-1] if False else table.add_row().cells
                    row[0].text = str(item["key"])
                    row[1].text = str(item["value"])
            elif block.kind == "table":
                rows = block.content.get("rows", [])
                columns = block.content.get("columns", [])
                table = document.add_table(rows=1, cols=len(columns))
                table.style = "Table Grid"
                for idx, col in enumerate(columns):
                    table.rows[0].cells[idx].text = str(col)
                for item in rows:
                    row = table.add_row().cells
                    for idx, col in enumerate(columns):
                        row[idx].text = str(item.get(col, ""))
        return payload

    def to_json(self, payload: dict[str, Any]) -> str:
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def _build_section_blocks(self, payload: dict[str, Any]) -> list[SectionBlock]:
        scorecard = payload["executive_scorecard"]
        tables = payload["tables"]
        appendix = payload["appendix"]
        narratives = payload["narratives"]

        return [
            SectionBlock(
                kind="key_value",
                title="Executive Scorecard",
                content=[
                    {"key": "Score", "value": f"{scorecard['score']}/{scorecard['max_score']}"},
                    {"key": "Confidence Level", "value": scorecard["confidence_level"]},
                    {"key": "Confidence Score", "value": scorecard["confidence_score"]},
                    {"key": "Evidence Coverage", "value": f"{scorecard['evidence_coverage_percentage']}% ({scorecard['evidence_coverage_status']})"},
                    {"key": "Quality Gate", "value": scorecard["quality_gate"]},
                    {"key": "Documentation Ready", "value": scorecard["documentation_ready"]},
                ],
            ),
            SectionBlock(kind="paragraph", title="Audit Narrative", content=narratives["audit_narrative"]),
            SectionBlock(kind="paragraph", title="Visibility Note", content=narratives["visibility_note"]),
            SectionBlock(
                kind="table",
                title="Weighted Scoring Matrix",
                content={
                    "columns": [
                        "dimension",
                        "label",
                        "weight",
                        "points_awarded",
                        "points_deducted",
                        "status",
                        "evidence_field",
                        "rationale",
                    ],
                    "rows": tables["weighted_scoring_matrix"],
                },
            ),
            SectionBlock(
                kind="table",
                title="Detected Issues",
                content={
                    "columns": [
                        "anti_pattern_code",
                        "category",
                        "severity",
                        "issue_type",
                        "points_deducted",
                        "message",
                        "recommendation",
                    ],
                    "rows": tables["issues"],
                },
            ),
            SectionBlock(
                kind="table",
                title="Anti-Pattern Categories",
                content={
                    "columns": [
                        "anti_pattern_code",
                        "category",
                        "severity",
                        "issue_type",
                        "count",
                        "points_deducted",
                    ],
                    "rows": tables["anti_pattern_categories"],
                },
            ),
            SectionBlock(
                kind="table",
                title="Evidence Coverage Signals",
                content={
                    "columns": ["field", "status", "coverage_value"],
                    "rows": tables["evidence_coverage_signals"],
                },
            ),
            SectionBlock(
                kind="bullets",
                title="Technical Appendix Snapshot",
                content=[
                    f"Package Name: {appendix.get('package_name') or 'not resolved'}",
                    f"Resolved Version: {appendix.get('resolved_version') or 'not resolved'}",
                    f"Protocols: {appendix.get('protocols') or 'not resolved'}",
                    f"Authentication: {appendix.get('authentication') or 'not resolved'}",
                    f"Sender Systems: {appendix.get('sender_systems') or 'not resolved'}",
                    f"Receiver Systems: {appendix.get('receiver_systems') or 'not resolved'}",
                    f"Recommended Next Step: {scorecard.get('recommended_next_step')}",
                ],
            ),
        ]

    def _matrix_rows(self, score: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "dimension": row.get("dimension"),
                "label": row.get("label"),
                "weight": row.get("weight"),
                "points_awarded": row.get("points_awarded"),
                "points_deducted": row.get("points_deducted"),
                "status": row.get("status"),
                "evidence_field": row.get("evidence_field"),
                "rationale": row.get("rationale"),
            }
            for row in score.get("weighted_scoring_matrix", [])
        ]

    def _issue_rows(self, score: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "anti_pattern_code": row.get("anti_pattern_code"),
                "category": row.get("category"),
                "severity": row.get("severity"),
                "issue_type": row.get("issue_type"),
                "points_deducted": row.get("points_deducted"),
                "message": row.get("message"),
                "recommendation": row.get("recommendation"),
            }
            for row in score.get("issues", [])
        ]

    def _anti_pattern_rows(self, score: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            {
                "anti_pattern_code": row.get("anti_pattern_code"),
                "category": row.get("category"),
                "severity": row.get("severity"),
                "issue_type": row.get("issue_type"),
                "count": row.get("count"),
                "points_deducted": row.get("points_deducted"),
            }
            for row in score.get("anti_pattern_categories", [])
        ]

    def _coverage_rows(self, score: dict[str, Any]) -> list[dict[str, Any]]:
        evidence = score.get("evidence_coverage", {})
        return [
            {
                "field": row.get("field"),
                "status": row.get("status"),
                "coverage_value": row.get("coverage_value"),
            }
            for row in evidence.get("signals", [])
        ]

    def _visibility_note(self, analysis_mode: str) -> str:
        if analysis_mode == "metadata_only":
            return (
                "This assessment was generated in metadata_only mode. Some missing technical signals may reflect tenant visibility limits rather than confirmed design defects. "
                "For configuration-level certainty, re-run the assessment in zip_based mode."
            )
        if analysis_mode == "zip_based":
            return (
                "This assessment was generated in zip_based mode. The resulting score is based on configuration-level evidence and is suitable for stronger technical audit narratives."
            )
        return (
            "The analysis mode could not be established with certainty. Interpret the score with caution and prefer an explicit parser-emitted analysis_mode in future runs."
        )

    def _normalized_join(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, tuple, set)):
            values = [str(item).strip() for item in value if str(item).strip()]
            return ", ".join(values)
        return str(value).strip()

    def _safe_get(self, data: dict[str, Any], *keys: str) -> Any:
        current: Any = data
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


DOCUMENTATION_SERVICE_PATCH_EXAMPLE = '''
from scoring_documentation_integration import EnterpriseScoringDocumentationAdapter

# Inside documentation_service.py
adapter = EnterpriseScoringDocumentationAdapter(scoring_service=scoring_service)
scoring_result = scoring_service.score_iflow(iflow_id, analysis)

# A) For direct DOCX rendering
adapter.append_to_docx(document, iflow_id, analysis, scoring_result)

# B) For templated rendering
payload = adapter.build_documentation_payload(iflow_id, analysis, scoring_result)
# payload["section_blocks"] or payload["tables"] can now be passed into your own docx builder
'''


MCP_HANDLER_PATCH_EXAMPLE = '''
from scoring_documentation_integration import EnterpriseScoringDocumentationAdapter

adapter = EnterpriseScoringDocumentationAdapter(scoring_service=scoring_service)
analysis = parser.parse(iflow_content)
scoring_result = scoring_service.score_iflow(iflow_id, analysis)
result = adapter.build_mcp_output(iflow_id, analysis, scoring_result)
return result
'''
