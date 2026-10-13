# SAP CPI ProcessDirect - No consumer found for local call

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_PROCESSDIRECT\_NO\_CONSUMER"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0082
RUNBOOK TITLE
SAP CPI ProcessDirect - No consumer found for local call
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI ProcessDirect - No consumer found for local call.
* Use this runbook only for object\_name CPI\_PROCESSDIRECT\_NO\_CONSUMER and taxonomy PROCESSDIRECT | LOCAL\_CALL | NO\_CONSUMER | ADDRESS\_NOT\_FOUND.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: ProcessDirect handoff fails because no deployed consumer listens on the configured local address.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: ProcessDirect Adapter.
* Protocol family: ProcessDirect.
* Error pattern: PROCESSDIRECT | LOCAL\_CALL | NO\_CONSUMER | ADDRESS\_NOT\_FOUND.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0082.
* Source KEDB artifact: KB\_RCMO\_CPI\_PROCESSDIRECT\_NO\_CONSUMER\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI ProcessDirect - No consumer found for local call.
* Normalized object\_name: CPI\_PROCESSDIRECT\_NO\_CONSUMER.
* Normalized taxonomy: PROCESSDIRECT | LOCAL\_CALL | NO\_CONSUMER | ADDRESS\_NOT\_FOUND.
* Sample 1: 2026-03-12T16:59:10.455 | MessageGuid AGmy8N7MbWDxTupNLUDi3QduwW9Y | Interface IR01\_IF12\_MessageLogs\_Alert | Sender n/a | Receiver n/a | Error: HTTP operation failed invoking https://clm-sl-ans-live-ans-service-api.cfapps.us10.hana.ondemand.com/cf/consumer/v1/matched-events with statusCode: 401
* Sample 2: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI ProcessDirect - No consumer found for local call.
* Short symptom: ProcessDirect handoff fails because no deployed consumer listens on the configured local address.
* Normalized object name: CPI\_PROCESSDIRECT\_NO\_CONSUMER.
* Normalized taxonomy: PROCESSDIRECT | LOCAL\_CALL | NO\_CONSUMER | ADDRESS\_NOT\_FOUND.
6. KNOWN ROOT CAUSES
* ProcessDirect address is wrong or inconsistent between producer and consumer.
* Target iFlow is not deployed or sender adapter is inactive.
* Consumer endpoint was renamed without updating the caller.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for ProcessDirect address and no consumer error text.
* Compare producer receiver address with the consumer sender address.
* Verify that the consumer iFlow is deployed and started.
* Compare the failing execution with the last successful MPL execution for CPI\_PROCESSDIRECT\_NO\_CONSUMER.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct the ProcessDirect address in producer or consumer iFlow.
* Deploy or restart the consumer iFlow.
* Replay one controlled message after local address resolution succeeds.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_PROCESSDIRECT\_NO\_CONSUMER is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_PROCESSDIRECT\_NO\_CONSUMER and PROCESSDIRECT | LOCAL\_CALL | NO\_CONSUMER | ADDRESS\_NOT\_FOUND do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

