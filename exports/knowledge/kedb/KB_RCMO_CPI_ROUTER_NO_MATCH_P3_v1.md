# SAP CPI Router - No condition matched
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_ROUTER_NO_MATCH"
priority: "P3"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P3-0083
KEDB TITLE
SAP CPI Router - No condition matched
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P3
VERSION
v1
1. SYMPTOM
* Router does not select any branch because predicates do not cover the message variant or no default route exists.
* Canonical retrieval phrase: SAP CPI Router - No condition matched.
* Normalized object_name: CPI_ROUTER_NO_MATCH.
2. ERROR PATTERN
* ROUTER | CONDITION | NO_MATCH | DEFAULT_MISSING
3. ROOT CAUSE
* Message variant is not covered by router predicates.
* Default branch is missing.
* Predicate logic is not null-safe for optional fields.
4. DIAGNOSIS SIGNALS
* Check MPL before the Router step and inspect fields used by predicates.
* Evaluate each router condition against the failing payload.
* Confirm whether a default branch exists for unmatched messages.
* Preserve runtime evidence: Evidence: 2026-03-27T18:54:27.780 | MessageGuid AGnG0mNnmIUL5nAp0d4ysw8CDqZA | Interface IR01_IF09_Access_Message_Processing_ErrorLogs_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: Could not match segment: 'MessageProcessingLogs('AGmt6OsRi31wm_R6tJgjIJkgS3s0')/ErrorInformation/$value'.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_ROUTER_NO_MATCH and ROUTER | CONDITION | NO_MATCH | DEFAULT_MISSING during search and triage.
5. RESOLUTION
* Add a default branch for unmatched messages.
* Update router predicates to cover current message variants.
* Add null-safe checks to predicate expressions and replay one controlled message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_ROUTER_NO_MATCH and ROUTER | CONDITION | NO_MATCH | DEFAULT_MISSING do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Route unmatched messages to a controlled exception path until predicate coverage is corrected.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_ROUTER_NO_MATCH_P3_v1.md
* Cross-reference object_name: CPI_ROUTER_NO_MATCH
* Cross-reference taxonomy: ROUTER | CONDITION | NO_MATCH | DEFAULT_MISSING
* Source KEDB ID: KEDB-P3-0083
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
