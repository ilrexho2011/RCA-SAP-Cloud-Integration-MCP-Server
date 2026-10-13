# Import Custom Integration Adapters

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "IMPORT_CUSTOM_INTEGRATION_ADAPTERS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-068

DOC TITLE
Import Custom Integration Adapters

1. PURPOSE
- This guide condenses the SAP Help pages behind Import Custom Integration Adapters into retrieval-friendly checkpoints for RAG ingestion.
- Focus on protocol-facing and extensibility topics: custom adapters, tracing, endpoint visibility, and adapter-specific behavior.

2. SCOPE
- Primary source scope: Import Custom Integration Adapters and closely related SAP Help pages.
- Chunking hint: select; configure; secure; trace.
- Preferred retrieval anchors: import custom integration adapters, select, configure, secure, import custom adapters.

3. KEY TERMS
- Select
- Configure
- Secure
- Trace
- Operate

4. CORE EXPLANATION
- Anchor retrieval on the concrete artifact type and on the lifecycle verb: create, configure, deploy, invoke, import, or transport.
- Keep protocol, direction, authentication mode, and runtime supportability close together in the same chunk.
- This guide condenses the SAP Help pages behind Import Custom Integration Adapters into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Choosing an adapter from familiarity instead of protocol fit and runtime support.
- Ignoring trace, connection-status, or cluster-behavior aspects until after go-live.
- Representative question forms:
- What is the intended use of import custom integration adapters in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for import custom integration adapters?
- What evidence and search anchors should be stored for import custom integration adapters, select, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-068
- Related runbooks: RB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P3_v1.md
- Related KEDB: KB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P3_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/importing-custom-integration-adapter-in-cloud-foundry-environment, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/adapter-development
