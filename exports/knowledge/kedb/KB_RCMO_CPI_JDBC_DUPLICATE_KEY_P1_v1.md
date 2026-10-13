# SAP CPI JDBC Adapter - SQL duplicate key violation
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_JDBC_DUPLICATE_KEY"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0076
KEDB TITLE
SAP CPI JDBC Adapter - SQL duplicate key violation
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* JDBC insert or update fails because the target table unique constraint already contains the business key.
* Canonical retrieval phrase: SAP CPI JDBC Adapter - SQL duplicate key violation.
* Normalized object_name: CPI_JDBC_DUPLICATE_KEY.
2. ERROR PATTERN
* JDBC | SQL | DUPLICATE_KEY | UNIQUE_CONSTRAINT
3. ROOT CAUSE
* Payload contains an already processed business key.
* The interface uses insert logic where upsert or idempotency is required.
* Replay sends duplicate records without duplicate control.
4. DIAGNOSIS SIGNALS
* Check MPL and database error for duplicate key or unique constraint text.
* Identify the business key and confirm whether the target row already exists.
* Compare replay history and idempotency repository for the same key.
* Preserve runtime evidence: Inspect the Exception Subprocess for the JDBC duplicate key error.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_JDBC_DUPLICATE_KEY and JDBC | SQL | DUPLICATE_KEY | UNIQUE_CONSTRAINT during search and triage.
5. RESOLUTION
* Implement deduplication before the JDBC write.
* Use upsert logic only when the target design allows update on existing keys.
* Record processed business keys in an idempotency repository.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_JDBC_DUPLICATE_KEY and JDBC | SQL | DUPLICATE_KEY | UNIQUE_CONSTRAINT do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Skip the duplicate record only after business validation confirms it was already processed.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_JDBC_DUPLICATE_KEY_P1_v1.md
* Cross-reference object_name: CPI_JDBC_DUPLICATE_KEY
* Cross-reference taxonomy: JDBC | SQL | DUPLICATE_KEY | UNIQUE_CONSTRAINT
* Source KEDB ID: KEDB-P1-0076
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
