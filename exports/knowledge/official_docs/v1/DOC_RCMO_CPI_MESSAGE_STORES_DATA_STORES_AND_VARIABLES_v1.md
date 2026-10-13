# Message Stores, Data Stores, and Variables

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "MESSAGE_STORES_DATA_STORES_AND_VARIABLES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-090

DOC TITLE
Message Stores, Data Stores, and Variables

1. PURPOSE
- This guide condenses the SAP Help pages behind Message Stores, Data Stores, and Variables into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

2. SCOPE
- Primary source scope: Message Stores, Data Stores, and Variables and closely related SAP Help pages.
- Chunking hint: run; trace; inspect; persist.
- Preferred retrieval anchors: message stores, data stores, and variables, run, trace, inspect, stores.

3. KEY TERMS
- Run
- Trace
- Inspect
- Persist
- Recover

4. CORE EXPLANATION
- Pair runtime views with message identifiers, status values, and persisted evidence so incident reconstruction stays deterministic.
- This guide condenses the SAP Help pages behind Message Stores, Data Stores, and Variables into retrieval-friendly checkpoints for RAG ingestion.
- Focus on runtime observability: message processing, tracing, persistence, lock management, and consumption hotspots.

5. OPERATIONAL RELEVANCE
- Capturing too little evidence in MPL or tracing and losing reproducibility.
- Persisting or logging more data than needed and creating avoidable storage pressure.
- Representative question forms:
- What is the intended use of message stores, data stores, and variables in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for message stores, data stores, and variables?
- What evidence and search anchors should be stored for message stores, data stores, and variables, run, trace?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-090
- Related runbooks: RB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, RB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, RB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, RB_RCMO_CPI_DATASTORE_LOOKUP_KEY_NOT_FOUND_P2_v1.md
- Related KEDB: KB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, KB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, KB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, KB_RCMO_CPI_DATASTORE_LOOKUP_KEY_NOT_FOUND_P2_v1.md
- Related catalog objects: IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1, IR27_IF03_Dynamic_Process_Football_OData_Scores
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-stores, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/data-storages, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/data-store-variables-and-jms-queues-when-to-use-which-option
