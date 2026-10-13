# AS2, Kafka, and Event-Driven Connectivity

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "AS2_KAFKA_EVENT_DRIVEN_CONNECTIVITY"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-076

DOC TITLE
AS2, Kafka, and Event-Driven Connectivity

1. PURPOSE
- This guide condenses the SAP Help pages behind AS2, Kafka, and Event-Driven Connectivity into retrieval-friendly checkpoints for RAG ingestion.
- Focus on protocol-facing and extensibility topics: custom adapters, tracing, endpoint visibility, and adapter-specific behavior.

2. SCOPE
- Primary source scope: AS2, Kafka, and Event-Driven Connectivity and closely related SAP Help pages.
- Chunking hint: select; configure; secure; trace.
- Preferred retrieval anchors: as2, kafka, and event-driven connectivity, select, configure, secure, as2.

3. KEY TERMS
- Select
- Configure
- Secure
- Trace
- Operate

4. CORE EXPLANATION
- Anchor retrieval on the concrete artifact type and on the lifecycle verb: create, configure, deploy, invoke, import, or transport.
- Keep protocol, direction, authentication mode, and runtime supportability close together in the same chunk.
- This guide condenses the SAP Help pages behind AS2, Kafka, and Event-Driven Connectivity into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Choosing an adapter from familiarity instead of protocol fit and runtime support.
- Ignoring trace, connection-status, or cluster-behavior aspects until after go-live.
- Representative question forms:
- What is the intended use of as2, kafka, and event-driven connectivity in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for as2, kafka, and event-driven connectivity?
- What evidence and search anchors should be stored for as2, kafka, and event-driven connectivity, select, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-076
- Related runbooks: RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, RB_RCMO_CPI_B2B_AS2_MDN_VALIDATION_FAILED_P1_v1.md, RB_RCMO_CPI_MAIL_SMTP_CONFIG_OR_AUTH_FAILURE_P3_v1.md, RB_RCMO_CPI_SECURITY_CERTIFICATE_EXPIRY_WARNING_P3_v1.md
- Related KEDB: KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_B2B_AS2_MDN_VALIDATION_FAILED_P1_v1.md, KB_RCMO_CPI_MAIL_SMTP_CONFIG_OR_AUTH_FAILURE_P3_v1.md, KB_RCMO_CPI_SECURITY_CERTIFICATE_EXPIRY_WARNING_P3_v1.md
- Related catalog objects: IR01_IF07_Test_Email_with_OAuth2_Code
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/configure-as2-receiver-adapter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/kafka-adapter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/decoupling-using-sap-integration-suite-advanced-event-mesh
