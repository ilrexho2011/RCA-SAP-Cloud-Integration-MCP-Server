# SAP CPI Data Store - Write conflict on existing key
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_DATASTORE_WRITE_CONFLICT"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0068
KEDB TITLE
SAP CPI Data Store - Write conflict on existing key
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Data Store write fails because concurrent messages or duplicate business keys target the same entry.
* Canonical retrieval phrase: SAP CPI Data Store - Write conflict on existing key.
* Normalized object_name: CPI_DATASTORE_WRITE_CONFLICT.
2. ERROR PATTERN
* DATASTORE | WRITE | CONFLICT | KEY_COLLISION
3. ROOT CAUSE
* Multiple messages write the same Data Store key in parallel.
* The key design is not unique for the business object.
* Overwrite handling is not aligned with the process idempotency rule.
4. DIAGNOSIS SIGNALS
* Check MPL for concurrent executions with the same Data Store key.
* Compare the key expression with the business object uniqueness rule.
* Confirm whether overwrite, update, or reject behavior is expected.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_DATASTORE_WRITE_CONFLICT and DATASTORE | WRITE | CONFLICT | KEY_COLLISION during search and triage.
5. RESOLUTION
* Use a unique composite key for each independent business object.
* Serialize processing for keys that must be updated sequentially.
* Apply controlled retry only after the conflicting execution is completed.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_DATASTORE_WRITE_CONFLICT and DATASTORE | WRITE | CONFLICT | KEY_COLLISION do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Pause parallel replay for the affected key range until serialization is active.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_DATASTORE_WRITE_CONFLICT_P2_v1.md
* Cross-reference object_name: CPI_DATASTORE_WRITE_CONFLICT
* Cross-reference taxonomy: DATASTORE | WRITE | CONFLICT | KEY_COLLISION
* Source KEDB ID: KEDB-P2-0068
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
