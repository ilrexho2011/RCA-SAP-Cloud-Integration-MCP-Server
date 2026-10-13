# Using Message Processing Log Attachments

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "USING_MESSAGE_PROCESSING_LOG_ATTACHMENTS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-093

DOC TITLE
Using Message Processing Log Attachments

1. PURPOSE
- This guide condenses the SAP Help pages behind Using Message Processing Log Attachments into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

2. SCOPE
- Primary source scope: Using Message Processing Log Attachments and closely related SAP Help pages.
- Chunking hint: run; trace; inspect; persist.
- Preferred retrieval anchors: using message processing log attachments, run, trace, inspect, using.

3. KEY TERMS
- Run
- Trace
- Inspect
- Persist
- Recover

4. CORE EXPLANATION
- Pair runtime views with message identifiers, status values, and persisted evidence so incident reconstruction stays deterministic.
- This guide condenses the SAP Help pages behind Using Message Processing Log Attachments into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

5. OPERATIONAL RELEVANCE
- Capturing too little evidence in MPL or tracing and losing reproducibility.
- Persisting or logging more data than needed and creating avoidable storage pressure.
- Representative question forms:
- What is the intended use of using message processing log attachments in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for using message processing log attachments?
- What evidence and search anchors should be stored for using message processing log attachments, run, trace?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-093
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md
- Related catalog objects: IR01_IF06_Test_SMS_Message, IR12_IF04_MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/using-message-processing-log-attachments?locale=en-US, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-processing-log-text-view
