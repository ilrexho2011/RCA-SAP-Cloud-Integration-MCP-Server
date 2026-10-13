# SAP CPI Data Store - Entry not found during read
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_DATASTORE_NOT_FOUND"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0067
KEDB TITLE
SAP CPI Data Store - Entry not found during read
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Data Store read step cannot find the expected entry for the resolved key.
* Canonical retrieval phrase: SAP CPI Data Store - Entry not found during read.
* Normalized object_name: CPI_DATASTORE_NOT_FOUND.
2. ERROR PATTERN
* DATASTORE | READ | NOT_FOUND | KEY_MISSING
3. ROOT CAUSE
* Read key pattern differs from the write key pattern.
* The write branch was skipped or failed before the read step.
* Retention, cleanup, or wrong store name removed the expected entry.
4. DIAGNOSIS SIGNALS
* Check the resolved Data Store name and key in MPL properties and headers.
* Verify that the write step completed before the read step for the same key.
* Compare retention settings and cleanup jobs for the target Data Store.
* Preserve runtime evidence: Evidence: 2026-04-10T12:46:07.444 | MessageGuid AGnY8Q-_BPrbVBCyJpSOg5xiFWd_ | Interface Football_Service | Sender n/a | Receiver n/a | Error: An internal server error occured: (404) Not Found [HTTP/1.1 404 Not Found]
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_DATASTORE_NOT_FOUND and DATASTORE | READ | NOT_FOUND | KEY_MISSING during search and triage.
5. RESOLUTION
* Standardize the Data Store key pattern across write and read steps.
* Add an existence check before the read step.
* Replay one controlled message after confirming the key was written.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_DATASTORE_NOT_FOUND and DATASTORE | READ | NOT_FOUND | KEY_MISSING do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Create the missing entry manually only when the business owner approves the reconstructed value.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_DATASTORE_NOT_FOUND_P2_v1.md
* Cross-reference object_name: CPI_DATASTORE_NOT_FOUND
* Cross-reference taxonomy: DATASTORE | READ | NOT_FOUND | KEY_MISSING
* Source KEDB ID: KEDB-P2-0067
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
