# Sharing Data Within the Same Integration Flow

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SHARING_DATA_WITHIN_THE_SAME_INTEGRATION_FLOW"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-141

DOC TITLE
Sharing Data Within the Same Integration Flow

1. PURPOSE
- This guide condenses the SAP Help pages behind Sharing Data Within the Same Integration Flow into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: share data, headers, properties, flow.

2. SCOPE
- Primary source scope: Sharing Data Within the Same Integration Flow and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: sharing data within the same integration flow, define, configure, validate, sharing data within the same flow.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for share data so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Sharing Data Within the Same Integration Flow into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating share data as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of sharing data within the same integration flow in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for sharing data within the same integration flow?
- What evidence and search anchors should be stored for sharing data within the same integration flow, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-141
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md, RB_RCMO_CPI_OBSERVABILITY_TRACE_DIAGNOSTICS_INSUFFICIENT_P3_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md, KB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/getting-started-with-integration-flow-development
