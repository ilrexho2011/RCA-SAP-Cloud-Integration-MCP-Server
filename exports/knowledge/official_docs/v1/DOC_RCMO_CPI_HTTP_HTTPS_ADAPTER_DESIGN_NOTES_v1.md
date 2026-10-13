# HTTP and HTTPS Adapter Design Notes

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "HTTP_HTTPS_ADAPTER_DESIGN_NOTES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-074

DOC TITLE
HTTP and HTTPS Adapter Design Notes

1. PURPOSE
- This guide condenses the SAP Help pages behind HTTP and HTTPS Adapter Design Notes into retrieval-friendly checkpoints for RAG ingestion.
- Focus on protocol-facing and extensibility topics: custom adapters, tracing, endpoint visibility, and adapter-specific behavior.

2. SCOPE
- Primary source scope: HTTP and HTTPS Adapter Design Notes and closely related SAP Help pages.
- Chunking hint: select; configure; secure; trace.
- Preferred retrieval anchors: http and https adapter design notes, select, configure, secure, http.

3. KEY TERMS
- Select
- Configure
- Secure
- Trace
- Operate

4. CORE EXPLANATION
- Anchor retrieval on the concrete artifact type and on the lifecycle verb: create, configure, deploy, invoke, import, or transport.
- Keep protocol, direction, authentication mode, and runtime supportability close together in the same chunk.
- Index certificate, keystore, OAuth, IdP, and role terms explicitly to improve retrieval for auth and trust failures.

5. OPERATIONAL RELEVANCE
- Choosing an adapter from familiarity instead of protocol fit and runtime support.
- Ignoring trace, connection-status, or cluster-behavior aspects until after go-live.
- Representative question forms:
- What is the intended use of http and https adapter design notes in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for http and https adapter design notes?
- What evidence and search anchors should be stored for http and https adapter design notes, select, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-074
- Related runbooks: RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503_P1_v1.md, RB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503_P1_v1.md, KB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md
- Related catalog objects: IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete, IR16_IF00_Read_and_Write_Variable_IFlow_1
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/http-receiver-adapter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/https-sender-adapter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/setting-up-outbound-http-connections-with-client-certificate-authentication
