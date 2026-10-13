# Tracing the Execution of an Integration Flow

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "TRACING_EXECUTION_OF_INTEGRATION_FLOW"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-088

DOC TITLE
Tracing the Execution of an Integration Flow

1. PURPOSE
- This guide condenses the SAP Help pages behind Tracing the Execution of an Integration Flow into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

2. SCOPE
- Primary source scope: Tracing the Execution of an Integration Flow and closely related SAP Help pages.
- Chunking hint: run; trace; inspect; persist.
- Preferred retrieval anchors: tracing the execution of an integration flow, run, trace, inspect, tracing the execution of an flow.

3. KEY TERMS
- Run
- Trace
- Inspect
- Persist
- Recover

4. CORE EXPLANATION
- Pair runtime views with message identifiers, status values, and persisted evidence so incident reconstruction stays deterministic.
- This guide condenses the SAP Help pages behind Tracing the Execution of an Integration Flow into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

5. OPERATIONAL RELEVANCE
- Capturing too little evidence in MPL or tracing and losing reproducibility.
- Persisting or logging more data than needed and creating avoidable storage pressure.
- Representative question forms:
- What is the intended use of tracing the execution of an integration flow in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for tracing the execution of an integration flow?
- What evidence and search anchors should be stored for tracing the execution of an integration flow, run, trace?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-088
- Related runbooks: RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503_P1_v1.md
- Related catalog objects: IR01_IF06_Test_SMS_Message, IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete, IR12_IF04_MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode, IR16_IF00_Read_and_Write_Variable_IFlow_1
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/tracing-execution-of-integration-flow, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-processing-log-adapter-tracing, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-processing-log-text-view
