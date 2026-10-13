# SAP CPI HTTP Receiver - 404 Not Found response

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_NOT\_FOUND\_404\_HTTP\_1\_1"
priority: "P2"
interface\_id: "IR16\_IF05\_MY\_MPL\_Alert\_System"
integration\_flow\_id: "IR16\_IF05\_MY\_MPL\_Alert\_System"
integration\_flow\_name: "IR16\_IF05\_MY\_MPL\_Alert\_System"
package\_name: "16 - Variables and Exception Handling in SAP CPI"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0081
RUNBOOK TITLE
SAP CPI HTTP Receiver - 404 Not Found response
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI HTTP Receiver - 404 Not Found response.
* Use this runbook only for object\_name CPI\_NOT\_FOUND\_404\_HTTP\_1\_1 and taxonomy HTTP | CLIENT\_ERROR | NOT\_FOUND | 404.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IR16\_IF05\_MY\_MPL\_Alert\_System.
* Impact: HTTP receiver call returns 404 Not Found because the endpoint path, resource, route, or receiver deployment is missing.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: 16 - Variables and Exception Handling in SAP CPI.
* Integration flow ID: IR16\_IF05\_MY\_MPL\_Alert\_System.
* Integration flow name: IR16\_IF05\_MY\_MPL\_Alert\_System.
* Processing component: HTTP Receiver Adapter.
* Protocol family: HTTP/HTTPS.
* Error pattern: HTTP | CLIENT\_ERROR | NOT\_FOUND | 404.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0081.
* Source KEDB artifact: KB\_RCMO\_CPI\_NOT\_FOUND\_404\_HTTP\_1\_1\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI HTTP Receiver - 404 Not Found response.
* Normalized object\_name: CPI\_NOT\_FOUND\_404\_HTTP\_1\_1.
* Normalized taxonomy: HTTP | CLIENT\_ERROR | NOT\_FOUND | 404.
* Sample 1: Impact | Not Found : 404 : HTTP/1.1
* Sample 1 | 2026-03-13T12:52:43.000 | MessageGuid AGm0CJt6P7wQFmv1KE9oS6De-wOi | Interface IR16\_IF06\_Email\_Alert\_Notifications\_For\_SAP\_CPI | Sender n/a | Receiver n/a | Error Not Found : 404 : HTTP/1.1
5. ERROR SIGNATURE
* Title: SAP CPI HTTP Receiver - 404 Not Found response.
* Short symptom: HTTP receiver call returns 404 Not Found because the endpoint path, resource, route, or receiver deployment is missing.
* Normalized object name: CPI\_NOT\_FOUND\_404\_HTTP\_1\_1.
* Normalized taxonomy: HTTP | CLIENT\_ERROR | NOT\_FOUND | 404.
6. KNOWN ROOT CAUSES
* Receiver URL path or resource name is wrong.
* Target service route is not deployed or not exposed.
* Externalized endpoint parameter points to a stale receiver path.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package 16 - Variables and Exception Handling in SAP CPI and interface IR16\_IF05\_MY\_MPL\_Alert\_System.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for HTTP/1.1 404 Not Found, receiver URL, MessageGuid, and timestamp.
* Verify the receiver endpoint path against the current API specification.
* Confirm route exposure, API management path, and deployment state.
* Compare the failing execution with the last successful MPL execution for CPI\_NOT\_FOUND\_404\_HTTP\_1\_1.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct the receiver URL path or externalized endpoint parameter.
* Deploy or expose the missing target service route.
* Redeploy the iFlow and replay one controlled HTTP message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_NOT\_FOUND\_404\_HTTP\_1\_1 is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_NOT\_FOUND\_404\_HTTP\_1\_1 and HTTP | CLIENT\_ERROR | NOT\_FOUND | 404 do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

