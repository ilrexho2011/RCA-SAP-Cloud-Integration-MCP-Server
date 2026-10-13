# Tracing for Custom Adapters

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "TRACING_FOR_CUSTOM_ADAPTERS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-069

DOC TITLE
Tracing for Custom Adapters

1. PURPOSE
- This guide condenses the SAP Help pages behind Tracing for Custom Adapters into retrieval-friendly checkpoints for RAG ingestion.
- Focus on protocol-facing and extensibility topics: custom adapters, tracing, endpoint visibility, and adapter-specific behavior.

2. SCOPE
- Primary source scope: Tracing for Custom Adapters and closely related SAP Help pages.
- Chunking hint: select; configure; secure; trace.
- Preferred retrieval anchors: tracing for custom adapters, select, configure, secure, tracing.

3. KEY TERMS
- Select
- Configure
- Secure
- Trace
- Operate

4. CORE EXPLANATION
- Anchor retrieval on the concrete artifact type and on the lifecycle verb: create, configure, deploy, invoke, import, or transport.
- Keep protocol, direction, authentication mode, and runtime supportability close together in the same chunk.
- This guide condenses the SAP Help pages behind Tracing for Custom Adapters into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Choosing an adapter from familiarity instead of protocol fit and runtime support.
- Ignoring trace, connection-status, or cluster-behavior aspects until after go-live.
- Representative question forms:
- What is the intended use of tracing for custom adapters in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for tracing for custom adapters?
- What evidence and search anchors should be stored for tracing for custom adapters, select, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-069
- Related runbooks: RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, RB_RCMO_CPI_OBSERVABILITY_TRACE_DIAGNOSTICS_INSUFFICIENT_P3_v1.md
- Related KEDB: KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, KB_RCMO_CPI_OBSERVABILITY_TRACE_DIAGNOSTICS_INSUFFICIENT_P3_v1.md
- Related catalog objects: IR12_IF04_MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/enabling-tracing-for-custom-adapter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-processing-log-adapter-tracing
