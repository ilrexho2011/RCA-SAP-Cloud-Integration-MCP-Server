# SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SF\_THROTTLE"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0088
RUNBOOK TITLE
SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded.
* Use this runbook only for object\_name CPI\_SF\_THROTTLE and taxonomy SUCCESSFACTORS | API | THROTTLING | RATE\_LIMIT\_EXCEEDED.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: SuccessFactors or receiver API rejects calls because the allowed request rate or quota is exceeded.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: SuccessFactors Receiver Adapter.
* Protocol family: OData/API.
* Error pattern: SUCCESSFACTORS | API | THROTTLING | RATE\_LIMIT\_EXCEEDED.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0088.
* Source KEDB artifact: KB\_RCMO\_CPI\_SF\_THROTTLE\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded.
* Normalized object\_name: CPI\_SF\_THROTTLE.
* Normalized taxonomy: SUCCESSFACTORS | API | THROTTLING | RATE\_LIMIT\_EXCEEDED.
* Sample 1: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI SuccessFactors API - Receiver throttling rate limit exceeded.
* Short symptom: SuccessFactors or receiver API rejects calls because the allowed request rate or quota is exceeded.
* Normalized object name: CPI\_SF\_THROTTLE.
* Normalized taxonomy: SUCCESSFACTORS | API | THROTTLING | RATE\_LIMIT\_EXCEEDED.
6. KNOWN ROOT CAUSES
* Polling interval or batch size creates too many calls.
* Parallel requests exceed receiver quota.
* Retry logic lacks backoff and amplifies throttling.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for 429, throttling, rate limit, or quota messages.
* Count calls per time window for the affected interface.
* Confirm receiver quota, paging, and retry policy with the API owner.
* Compare the failing execution with the last successful MPL execution for CPI\_SF\_THROTTLE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Apply paging and reduce payload volume per call.
* Add exponential backoff before retries.
* Reduce parallelism and align polling interval with receiver quota.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SF\_THROTTLE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SF\_THROTTLE and SUCCESSFACTORS | API | THROTTLING | RATE\_LIMIT\_EXCEEDED do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

