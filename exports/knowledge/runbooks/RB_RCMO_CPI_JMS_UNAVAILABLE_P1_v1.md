# SAP CPI JMS Adapter - JMS queue unavailable

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_JMS\_UNAVAILABLE"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0077
RUNBOOK TITLE
SAP CPI JMS Adapter - JMS queue unavailable
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI JMS Adapter - JMS queue unavailable.
* Use this runbook only for object\_name CPI\_JMS\_UNAVAILABLE and taxonomy JMS | QUEUE | UNAVAILABLE | SERVICE\_OR\_QUOTA.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: JMS publish or consume fails because the queue is disabled, quota is reached, or the JMS service is unavailable.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: JMS Adapter.
* Protocol family: JMS.
* Error pattern: JMS | QUEUE | UNAVAILABLE | SERVICE\_OR\_QUOTA.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0077.
* Source KEDB artifact: KB\_RCMO\_CPI\_JMS\_UNAVAILABLE\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI JMS Adapter - JMS queue unavailable.
* Normalized object\_name: CPI\_JMS\_UNAVAILABLE.
* Normalized taxonomy: JMS | QUEUE | UNAVAILABLE | SERVICE\_OR\_QUOTA.
* Sample 1: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI JMS Adapter - JMS queue unavailable.
* Short symptom: JMS publish or consume fails because the queue is disabled, quota is reached, or the JMS service is unavailable.
* Normalized object name: CPI\_JMS\_UNAVAILABLE.
* Normalized taxonomy: JMS | QUEUE | UNAVAILABLE | SERVICE\_OR\_QUOTA.
6. KNOWN ROOT CAUSES
* JMS queue is disabled or deleted.
* Tenant JMS quota is reached.
* Temporary JMS service outage affects publish or consume operations.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check JMS queue state, quota, and current backlog in CPI monitor.
* Check MPL for queue name, operation, MessageGuid, and error text.
* Confirm whether the issue affects one queue or the whole JMS service.
* Compare the failing execution with the last successful MPL execution for CPI\_JMS\_UNAVAILABLE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Enable or recreate the approved JMS queue configuration.
* Reduce load or clear backlog when quota is reached.
* Restart affected processing only after queue health is confirmed.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_JMS\_UNAVAILABLE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_JMS\_UNAVAILABLE and JMS | QUEUE | UNAVAILABLE | SERVICE\_OR\_QUOTA do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

