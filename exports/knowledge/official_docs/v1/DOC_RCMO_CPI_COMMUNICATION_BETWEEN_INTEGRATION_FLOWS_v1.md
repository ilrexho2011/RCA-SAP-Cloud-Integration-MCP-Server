# Communication Between Integration Flows

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "COMMUNICATION_BETWEEN_INTEGRATION_FLOWS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-145

DOC TITLE
Communication Between Integration Flows

1. PURPOSE
- This guide condenses the SAP Help pages behind Communication Between Integration Flows into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: processdirect, communication between flows.

2. SCOPE
- Primary source scope: Communication Between Integration Flows and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: communication between integration flows, define, configure, validate, communication between flows.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for processdirect so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Communication Between Integration Flows into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating processdirect as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of communication between integration flows in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for communication between integration flows?
- What evidence and search anchors should be stored for communication between integration flows, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-145
- Related runbooks: RB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, RB_RCMO_CPI_JMS_OPERATIONS_DLQ_THRESHOLD_REACHED_P3_v1.md, RB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, RB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, KB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, KB_RCMO_CPI_API_THROTTLING_RATE_LIMIT_EXCEEDED_P2_v1.md, KB_RCMO_CPI_JMS_OPERATIONS_DLQ_THRESHOLD_REACHED_P3_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
