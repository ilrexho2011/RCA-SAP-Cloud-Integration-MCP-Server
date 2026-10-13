# Content Filter and XPath Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CONTENT_FILTER_AND_XPATH_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-130

DOC TITLE
Content Filter and XPath Patterns

1. PURPOSE
- This guide condenses the SAP Help pages behind Content Filter and XPath Patterns into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: content filter, xpath, filter.

2. SCOPE
- Primary source scope: Content Filter and XPath Patterns and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: content filter and xpath patterns, define, configure, validate, filter.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for content filter so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Content Filter and XPath Patterns into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating content filter as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of content filter and xpath patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for content filter and xpath patterns?
- What evidence and search anchors should be stored for content filter and xpath patterns, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-130
- Related runbooks: RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, KB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
