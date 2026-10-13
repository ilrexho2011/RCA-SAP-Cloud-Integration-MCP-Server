# SAP CPI JMS Adapter - JMS queue unavailable
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_JMS_UNAVAILABLE"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0077
KEDB TITLE
SAP CPI JMS Adapter - JMS queue unavailable
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* JMS publish or consume fails because the queue is disabled, quota is reached, or the JMS service is unavailable.
* Canonical retrieval phrase: SAP CPI JMS Adapter - JMS queue unavailable.
* Normalized object_name: CPI_JMS_UNAVAILABLE.
2. ERROR PATTERN
* JMS | QUEUE | UNAVAILABLE | SERVICE_OR_QUOTA
3. ROOT CAUSE
* JMS queue is disabled or deleted.
* Tenant JMS quota is reached.
* Temporary JMS service outage affects publish or consume operations.
4. DIAGNOSIS SIGNALS
* Check JMS queue state, quota, and current backlog in CPI monitor.
* Check MPL for queue name, operation, MessageGuid, and error text.
* Confirm whether the issue affects one queue or the whole JMS service.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_JMS_UNAVAILABLE and JMS | QUEUE | UNAVAILABLE | SERVICE_OR_QUOTA during search and triage.
5. RESOLUTION
* Enable or recreate the approved JMS queue configuration.
* Reduce load or clear backlog when quota is reached.
* Restart affected processing only after queue health is confirmed.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_JMS_UNAVAILABLE and JMS | QUEUE | UNAVAILABLE | SERVICE_OR_QUOTA do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Pause inbound processing until JMS queue state and quota are stable.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_JMS_UNAVAILABLE_P1_v1.md
* Cross-reference object_name: CPI_JMS_UNAVAILABLE
* Cross-reference taxonomy: JMS | QUEUE | UNAVAILABLE | SERVICE_OR_QUOTA
* Source KEDB ID: KEDB-P1-0077
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
