# Enterprise Scoring Integration Patch Guide

This package connects `scoring_service_enterprise.py` to two downstream targets:

1. `documentation_service.py` for `.docx` generation
2. MCP tool JSON output for audit/documentation-aware responses

## Files

- `scoring_documentation_integration.py`
- `mcp_iflow_audit_output_schema.json`

## 1) Patch `documentation_service.py`

```python
from scoring_service_enterprise import ScoringService
from scoring_documentation_integration import EnterpriseScoringDocumentationAdapter

class DocumentationService:
    def __init__(self) -> None:
        self.scoring_service = ScoringService()
        self.scoring_adapter = EnterpriseScoringDocumentationAdapter(self.scoring_service)

    def build_iflow_docx(self, document, iflow_id: str, analysis: dict) -> None:
        # existing technical content here
        scoring_result = self.scoring_service.score_iflow(iflow_id, analysis)
        self.scoring_adapter.append_to_docx(document, iflow_id, analysis, scoring_result)
```

## 2) Alternative templated `.docx` rendering path

If your `documentation_service.py` already uses an internal table renderer, do this instead:

```python
scoring_result = self.scoring_service.score_iflow(iflow_id, analysis)
payload = self.scoring_adapter.build_documentation_payload(iflow_id, analysis, scoring_result)

# Use payload["executive_scorecard"], payload["narratives"], payload["tables"],
# or payload["section_blocks"] in your own renderer.
```

## 3) Patch MCP output schema

```python
from scoring_service_enterprise import ScoringService
from scoring_documentation_integration import EnterpriseScoringDocumentationAdapter

class AnalyzeIFlowTool:
    def __init__(self, parser) -> None:
        self.parser = parser
        self.scoring_service = ScoringService()
        self.scoring_adapter = EnterpriseScoringDocumentationAdapter(self.scoring_service)

    def run(self, iflow_id: str, iflow_content: bytes) -> dict:
        analysis = self.parser.parse(iflow_content)
        scoring_result = self.scoring_service.score_iflow(iflow_id, analysis)
        return self.scoring_adapter.build_mcp_output(iflow_id, analysis, scoring_result)
```

Validate the final payload against `mcp_iflow_audit_output_schema.json`.

## 4) What goes into the generated `.docx`

The adapter emits these sections:

- Executive Scorecard
- Audit Narrative
- Visibility Note
- Weighted Scoring Matrix
- Detected Issues
- Anti-Pattern Categories
- Evidence Coverage Signals
- Technical Appendix Snapshot

## 5) Why this integration is useful

- `zip_based` and `metadata_only` remain clearly separated in documentation
- visibility limitations are not incorrectly presented as hard design defects
- MCP output becomes machine-readable and audit-ready
- the same scoring result can feed both `.docx` and JSON without duplication
