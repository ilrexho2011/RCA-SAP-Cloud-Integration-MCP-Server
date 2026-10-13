# SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV"
priority: "P2"
interface\_id: "IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant"
integration\_flow\_id: "IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant"
integration\_flow\_name: "IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant"
package\_name: "20 - Complex Projects"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0073
RUNBOOK TITLE
SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException.
* Use this runbook only for object\_name CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV and taxonomy HTTP | CONNECTIVITY | DNS\_RESOLUTION | UNKNOWN\_HOST.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant.
* Impact: HTTP receiver call fails with UnknownHostException or Name or service not known because the target hostname cannot be resolved.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: 20 - Complex Projects.
* Integration flow ID: IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant.
* Integration flow name: IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant.
* Processing component: HTTP Receiver Adapter.
* Protocol family: HTTP/HTTPS.
* Error pattern: HTTP | CONNECTIVITY | DNS\_RESOLUTION | UNKNOWN\_HOST.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0073.
* Source KEDB artifact: KB\_RCMO\_CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException.
* Normalized object\_name: CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV.
* Normalized taxonomy: HTTP | CONNECTIVITY | DNS\_RESOLUTION | UNKNOWN\_HOST.
* Sample 1: Impact: HTTP Request failed with error : https: Name or service not known, cause: java.net.UnknownHostException: https: Name or service not known
* Sample 1: 2026-03-13T12:42:28.001 | MessageGuid AGm0BjRKgUBZsuV6ojnD13CEewLM | Interface IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant | Sender n/a | Receiver n/a | Error: HTTP Request failed with error : https: Name or service not known, cause: java.net.UnknownHostException: https: Name or service not known
5. ERROR SIGNATURE
* Title: SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException.
* Short symptom: HTTP receiver call fails with UnknownHostException or Name or service not known because the target hostname cannot be resolved.
* Normalized object name: CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV.
* Normalized taxonomy: HTTP | CONNECTIVITY | DNS\_RESOLUTION | UNKNOWN\_HOST.
6. KNOWN ROOT CAUSES
* Receiver URL contains an invalid hostname or malformed scheme.
* DNS resolution is missing for the target host.
* Cloud Connector or proxy route does not expose the receiver host.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package 20 - Complex Projects and interface IR20\_IF02\_Email\_Alert\_Notifications\_For\_SAP\_CPI\_Tenant.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for UnknownHostException, receiver URL, MessageGuid, and timestamp.
* Verify the receiver endpoint hostname without protocol duplication or malformed path.
* Test DNS, proxy, and Cloud Connector route from the CPI connectivity context.
* Compare the failing execution with the last successful MPL execution for CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct the receiver URL and hostname in the HTTP adapter or externalized parameter.
* Fix DNS, proxy, or Cloud Connector mapping for the target host.
* Redeploy the iFlow and replay one controlled HTTP message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_HTTP\_REQUEST\_FAILED\_WITH\_ERROR\_HTTPS\_NAME\_OR\_SERVICE\_NOT\_KNOWN\_CAUSE\_JAV and HTTP | CONNECTIVITY | DNS\_RESOLUTION | UNKNOWN\_HOST do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

