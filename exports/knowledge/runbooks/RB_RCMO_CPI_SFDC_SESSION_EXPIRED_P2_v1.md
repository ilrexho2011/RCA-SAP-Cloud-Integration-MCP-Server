# SAP CPI Salesforce Adapter - Session expired authentication failure

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SFDC\_SESSION\_EXPIRED"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0085
RUNBOOK TITLE
SAP CPI Salesforce Adapter - Session expired authentication failure
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Salesforce Adapter - Session expired authentication failure.
* Use this runbook only for object\_name CPI\_SFDC\_SESSION\_EXPIRED and taxonomy SALESFORCE | AUTHENTICATION | SESSION\_EXPIRED | TOKEN\_REFRESH.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Salesforce call fails because the session token or connected app authentication state has expired.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Salesforce Adapter.
* Protocol family: Salesforce API.
* Error pattern: SALESFORCE | AUTHENTICATION | SESSION\_EXPIRED | TOKEN\_REFRESH.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0085.
* Source KEDB artifact: KB\_RCMO\_CPI\_SFDC\_SESSION\_EXPIRED\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Salesforce Adapter - Session expired authentication failure.
* Normalized object\_name: CPI\_SFDC\_SESSION\_EXPIRED.
* Normalized taxonomy: SALESFORCE | AUTHENTICATION | SESSION\_EXPIRED | TOKEN\_REFRESH.
* Sample 1: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI Salesforce Adapter - Session expired authentication failure.
* Short symptom: Salesforce call fails because the session token or connected app authentication state has expired.
* Normalized object name: CPI\_SFDC\_SESSION\_EXPIRED.
* Normalized taxonomy: SALESFORCE | AUTHENTICATION | SESSION\_EXPIRED | TOKEN\_REFRESH.
6. KNOWN ROOT CAUSES
* CPI Salesforce credential or session token is stale.
* Connected app session policy changed.
* Token refresh configuration is not valid for the adapter.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for Salesforce session expired or authentication failure text.
* Verify CPI Security Material and Salesforce connected app settings.
* Confirm session policy and token refresh behavior with the Salesforce owner.
* Compare the failing execution with the last successful MPL execution for CPI\_SFDC\_SESSION\_EXPIRED.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Refresh the Salesforce connection or credential alias in CPI.
* Update connected app session settings when policy changed.
* Retest the iFlow with one controlled Salesforce call.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SFDC\_SESSION\_EXPIRED is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SFDC\_SESSION\_EXPIRED and SALESFORCE | AUTHENTICATION | SESSION\_EXPIRED | TOKEN\_REFRESH do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

