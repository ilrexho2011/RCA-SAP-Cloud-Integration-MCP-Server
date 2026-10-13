# SAP CPI ProcessDirect - No consumer found for local call
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_PROCESSDIRECT_NO_CONSUMER"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0082
KEDB TITLE
SAP CPI ProcessDirect - No consumer found for local call
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* ProcessDirect handoff fails because no deployed consumer listens on the configured local address.
* Canonical retrieval phrase: SAP CPI ProcessDirect - No consumer found for local call.
* Normalized object_name: CPI_PROCESSDIRECT_NO_CONSUMER.
2. ERROR PATTERN
* PROCESSDIRECT | LOCAL_CALL | NO_CONSUMER | ADDRESS_NOT_FOUND
3. ROOT CAUSE
* ProcessDirect address is wrong or inconsistent between producer and consumer.
* Target iFlow is not deployed or sender adapter is inactive.
* Consumer endpoint was renamed without updating the caller.
4. DIAGNOSIS SIGNALS
* Check MPL for ProcessDirect address and no consumer error text.
* Compare producer receiver address with the consumer sender address.
* Verify that the consumer iFlow is deployed and started.
* Preserve runtime evidence: Evidence: 2026-03-12T16:59:10.455 | MessageGuid AGmy8N7MbWDxTupNLUDi3QduwW9Y | Interface IR01_IF12_MessageLogs_Alert | Sender n/a | Receiver n/a | Error: HTTP operation failed invoking https://clm-sl-ans-live-ans-service-api.cfapps.us10.hana.ondemand.com/cf/consumer/v1/matched-events with statusCode: 401
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_PROCESSDIRECT_NO_CONSUMER and PROCESSDIRECT | LOCAL_CALL | NO_CONSUMER | ADDRESS_NOT_FOUND during search and triage.
5. RESOLUTION
* Correct the ProcessDirect address in producer or consumer iFlow.
* Deploy or restart the consumer iFlow.
* Replay one controlled message after local address resolution succeeds.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_PROCESSDIRECT_NO_CONSUMER and PROCESSDIRECT | LOCAL_CALL | NO_CONSUMER | ADDRESS_NOT_FOUND do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Temporarily route through the approved backup integration path if available.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_PROCESSDIRECT_NO_CONSUMER_P1_v1.md
* Cross-reference object_name: CPI_PROCESSDIRECT_NO_CONSUMER
* Cross-reference taxonomy: PROCESSDIRECT | LOCAL_CALL | NO_CONSUMER | ADDRESS_NOT_FOUND
* Source KEDB ID: KEDB-P1-0082
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
