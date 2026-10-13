# SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SF_THROTTLE"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0088
KEDB TITLE
SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* SuccessFactors or receiver API rejects calls because the allowed request rate or quota is exceeded.
* Canonical retrieval phrase: SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded.
* Normalized object_name: CPI_SF_THROTTLE.
2. ERROR PATTERN
* SUCCESSFACTORS | API | THROTTLING | RATE_LIMIT_EXCEEDED
3. ROOT CAUSE
* Polling interval or batch size creates too many calls.
* Parallel requests exceed receiver quota.
* Retry logic lacks backoff and amplifies throttling.
4. DIAGNOSIS SIGNALS
* Check MPL for 429, throttling, rate limit, or quota messages.
* Count calls per time window for the affected interface.
* Confirm receiver quota, paging, and retry policy with the API owner.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SF_THROTTLE and SUCCESSFACTORS | API | THROTTLING | RATE_LIMIT_EXCEEDED during search and triage.
5. RESOLUTION
* Apply paging and reduce payload volume per call.
* Add exponential backoff before retries.
* Reduce parallelism and align polling interval with receiver quota.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SF_THROTTLE and SUCCESSFACTORS | API | THROTTLING | RATE_LIMIT_EXCEEDED do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Pause non-critical polling until receiver quota recovers.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SF_THROTTLE_P2_v1.md
* Cross-reference object_name: CPI_SF_THROTTLE
* Cross-reference taxonomy: SUCCESSFACTORS | API | THROTTLING | RATE_LIMIT_EXCEEDED
* Source KEDB ID: KEDB-P2-0088
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
