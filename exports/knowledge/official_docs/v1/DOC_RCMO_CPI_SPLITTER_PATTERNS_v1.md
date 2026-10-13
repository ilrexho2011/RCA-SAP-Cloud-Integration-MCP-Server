# Splitter Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SPLITTER_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-041

DOC TITLE
Splitter Patterns

1. PURPOSE
- Splitter steps decompose a composite message into smaller messages for downstream processing.
- The main design choice is whether enveloping context should be preserved or not, and how the split path is selected.

2. SCOPE
- Primary source scope: Splitter Patterns and closely related SAP Help pages.
- Chunking hint: identify composite structure; choose splitter type; define split path; validate each fragment shape.
- Preferred retrieval anchors: splitter patterns, identify composite structure, choose splitter type, define split path, patterns.

3. KEY TERMS
- Identify composite
- structure
- Choose splitter type
- Define split path
- Validate each fragment
- shape
- Continue processing or
- gather later Why this …

4. CORE EXPLANATION
- SAP Help describes several splitter variants and emphasizes the decomposition of composite messages. In operations, that becomes important whenever only some child records fail, an XPath returns no node, or a downstream step receives a fragment shape different from what the flow assumed.
- Splitter type matters: general and iterating splitters do not preserve context in the same way.
- Path resolution is critical: if the configured path returns no node, the error is usually structural, not transport-related.
- Fragment contract: downstream mappings and receivers must understand the post-split message shape.
- Bulk processing changes observability: one source message can become many operational outcomes.

5. OPERATIONAL RELEVANCE
- Choosing a splitter type without considering whether parent context must remain available later.
- Assuming a configured path is stable even when source structures vary.
- Treating fragment failures as isolated when the split design is globally wrong.
- Ignoring how observability changes once one message becomes many runtime units.
- Representative question forms:
- What is the intended use of splitter patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for splitter patterns?
- What evidence and search anchors should be stored for splitter patterns, identify composite structure, choose splitter type?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-041
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related KEDB: KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, KB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/define-splitter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/general-and-iterating-splitter-examples, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/splitter
