# SAP CPI Splitter - Payload split expression failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SPLITTER_FAILED"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0090
KEDB TITLE
SAP CPI Splitter - Payload split expression failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Splitter fails because the configured XPath or JSONPath does not match the current bulk payload structure.
* Canonical retrieval phrase: SAP CPI Splitter - Payload split expression failed.
* Normalized object_name: CPI_SPLITTER_FAILED.
2. ERROR PATTERN
* SPLITTER | PAYLOAD | SPLIT_EXPRESSION | NODE_NOT_FOUND
3. ROOT CAUSE
* XPath or JSONPath points to a missing node.
* Payload schema changed without updating the split expression.
* Bulk payload is empty or structurally invalid.
4. DIAGNOSIS SIGNALS
* Check MPL before the Splitter and inspect the actual payload structure.
* Validate XPath or JSONPath against the current payload sample.
* Confirm whether schema changes were introduced by the sender.
* Preserve runtime evidence: Check MPL API for the affected MessageGuid and interface context.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SPLITTER_FAILED and SPLITTER | PAYLOAD | SPLIT_EXPRESSION | NODE_NOT_FOUND during search and triage.
5. RESOLUTION
* Correct the split expression to match the current payload.
* Add validation for empty or invalid bulk payloads before split.
* Redeploy and replay one controlled bulk message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SPLITTER_FAILED and SPLITTER | PAYLOAD | SPLIT_EXPRESSION | NODE_NOT_FOUND do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Process the payload manually or sequentially only after sender confirms record boundaries.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SPLITTER_FAILED_P2_v1.md
* Cross-reference object_name: CPI_SPLITTER_FAILED
* Cross-reference taxonomy: SPLITTER | PAYLOAD | SPLIT_EXPRESSION | NODE_NOT_FOUND
* Source KEDB ID: KEDB-P2-0090
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
