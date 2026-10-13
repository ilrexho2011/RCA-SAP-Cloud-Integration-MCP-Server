# Define Local Integration Process

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "DEFINE_LOCAL_INTEGRATION_PROCESS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-142

DOC TITLE
Define Local Integration Process

1. PURPOSE
- This guide condenses the SAP Help pages behind Define Local Integration Process into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: local integration process, process call.

2. SCOPE
- Primary source scope: Define Local Integration Process and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: define local integration process, define, configure, validate, define local process.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for local integration process so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Define Local Integration Process into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating local integration process as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of define local integration process in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for define local integration process?
- What evidence and search anchors should be stored for define local integration process, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-142
- Related runbooks: RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, RB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
