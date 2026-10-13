# Data Stores and Persisted Processing

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "DATA_STORES_AND_PERSISTED_PROCESSING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-052

DOC TITLE
Data Stores and Persisted Processing

1. PURPOSE
- Data stores and message stores introduce persisted state into message processing and therefore change both reliability and troubleshooting.
- They are essential when a flow must decouple processing, remember prior state, or recover later with evidence.

2. SCOPE
- Primary source scope: Data Stores and Persisted Processing and closely related SAP Help pages.
- Chunking hint: need persisted state?; choose store purpose; define write/read/delete discipline; monitor key usage.
- Preferred retrieval anchors: data stores and persisted processing, need persisted state?, choose store purpose, define write/read/delete discipline, data.

3. KEY TERMS
- Need persisted state?
- Choose store purpose
- Define write/read/delete
- discipline
- Monitor key usage
- Validate retention and
- recovery behavior W…

4. CORE EXPLANATION
- SAP Help documents data storages, data store operations, and related storage-management areas. Operationally, persisted state is powerful because it supports decoupling and delayed processing, but it also creates new failure modes: stale keys, missing entries, storage pressure, and disagreements about what the system should remember.
- Persisted state should exist for a clear purpose: decoupling, deduplication, lookup, buffering, or evidence retention.
- Key design is central; a weak key strategy leads directly to not-found and conflict scenarios.
- State lifecycle matters: write, read, delete, and retention should be planned together.
- A persistence-heavy design changes incident analysis because historical state can outlive the current message.

5. OPERATIONAL RELEVANCE
- Introducing persisted state without a clear lifecycle and ownership model.
- Using keys that are not stable enough for reliable lookup or deduplication.
- Treating a datastore miss as a random runtime event instead of a state-management defect.
- Keeping evidence or temporary data without considering storage growth and governance.
- Representative question forms:
- What is the intended use of data stores and persisted processing in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for data stores and persisted processing?
- What evidence and search anchors should be stored for data stores and persisted processing, need persisted state?, choose store purpose?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-052
- Related runbooks: RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, RB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, RB_RCMO_CPI_DATASTORE_LOOKUP_KEY_NOT_FOUND_P2_v1.md
- Related KEDB: KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, KB_RCMO_CPI_MESSAGING_JMS_QUEUE_UNAVAILABLE_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, KB_RCMO_CPI_DATASTORE_LOOKUP_KEY_NOT_FOUND_P2_v1.md
- Related catalog objects: IR01_IF06_Test_SMS_Message
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/data-storages, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/define-data-store-operations, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/managing-data-stores, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-stores
