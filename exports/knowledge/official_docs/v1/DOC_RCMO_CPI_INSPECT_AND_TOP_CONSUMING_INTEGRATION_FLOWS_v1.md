# Inspect and Top Consuming Integration Flows

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "INSPECT_AND_TOP_CONSUMING_INTEGRATION_FLOWS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-092

DOC TITLE
Inspect and Top Consuming Integration Flows

1. PURPOSE
- This guide condenses the SAP Help pages behind Inspect and Top Consuming Integration Flows into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

2. SCOPE
- Primary source scope: Inspect and Top Consuming Integration Flows and closely related SAP Help pages.
- Chunking hint: run; trace; inspect; persist.
- Preferred retrieval anchors: inspect and top consuming integration flows, run, trace, inspect, inspect and top consuming flows.

3. KEY TERMS
- Run
- Trace
- Inspect
- Persist
- Recover

4. CORE EXPLANATION
- Pair runtime views with message identifiers, status values, and persisted evidence so incident reconstruction stays deterministic.
- This guide condenses the SAP Help pages behind Inspect and Top Consuming Integration Flows into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

5. OPERATIONAL RELEVANCE
- Capturing too little evidence in MPL or tracing and losing reproducibility.
- Persisting or logging more data than needed and creating avoidable storage pressure.
- Representative question forms:
- What is the intended use of inspect and top consuming integration flows in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for inspect and top consuming integration flows?
- What evidence and search anchors should be stored for inspect and top consuming integration flows, run, trace?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-092
- Related runbooks: RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, RB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, RB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, KB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, KB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md
- Related catalog objects: IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete, IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1, IR16_IF00_Read_and_Write_Variable_IFlow_1, IR27_IF03_Dynamic_Process_Football_OData_Scores
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/inspect, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/inspect-top-consuming-integration-flows
