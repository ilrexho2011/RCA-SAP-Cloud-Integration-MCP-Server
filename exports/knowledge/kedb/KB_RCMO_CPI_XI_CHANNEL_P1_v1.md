# SAP CPI XI Adapter - Receiver channel handoff failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_XI_CHANNEL"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0092
KEDB TITLE
SAP CPI XI Adapter - Receiver channel handoff failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* XI protocol handoff fails because the target XI endpoint, receiver channel, QoS, or agreement is unavailable or misconfigured.
* Canonical retrieval phrase: SAP CPI XI Adapter - Receiver channel handoff failed.
* Normalized object_name: CPI_XI_CHANNEL.
2. ERROR PATTERN
* XI | CHANNEL | HANDOFF | ERROR
3. ROOT CAUSE
* Target XI endpoint or receiver channel is unavailable.
* QoS settings are incorrect for the receiver scenario.
* Receiver agreement or channel configuration does not match the flow.
4. DIAGNOSIS SIGNALS
* Check MPL for XI channel error and capture receiver channel, QoS, and MessageGuid.
* Verify target XI endpoint, receiver agreement, and channel state.
* Compare QoS settings with the interface contract.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_XI_CHANNEL and XI | CHANNEL | HANDOFF | ERROR during search and triage.
5. RESOLUTION
* Correct XI endpoint, receiver agreement, and QoS settings.
* Restore or restart the XI receiver channel after owner confirmation.
* Replay one controlled XI message after channel validation succeeds.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_XI_CHANNEL and XI | CHANNEL | HANDOFF | ERROR do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Queue affected messages and avoid blind replay while the XI channel remains unstable.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_XI_CHANNEL_P1_v1.md
* Cross-reference object_name: CPI_XI_CHANNEL
* Cross-reference taxonomy: XI | CHANNEL | HANDOFF | ERROR
* Source KEDB ID: KEDB-P1-0092
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
