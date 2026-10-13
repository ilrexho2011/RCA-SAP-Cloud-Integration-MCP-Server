# Define Gather and Join

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "DEFINE_GATHER_AND_JOIN"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-140

DOC TITLE
Define Gather and Join

1. PURPOSE
- This guide condenses the SAP Help pages behind Define Gather and Join into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: gather, join, aggregation.

2. SCOPE
- Primary source scope: Define Gather and Join and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: define gather and join, define, configure, validate.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for gather so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Define Gather and Join into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating gather as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of define gather and join in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for define gather and join?
- What evidence and search anchors should be stored for define gather and join, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-140
- Related runbooks: RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md
- Related catalog objects: IR27_IF03_Dynamic_Process_Football_OData_Scores
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
