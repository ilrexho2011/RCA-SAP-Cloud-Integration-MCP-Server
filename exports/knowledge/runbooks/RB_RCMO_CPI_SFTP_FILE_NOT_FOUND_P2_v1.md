# SAP CPI SFTP Adapter - Remote file or directory not found

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SFTP\_FILE\_NOT\_FOUND"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0087
RUNBOOK TITLE
SAP CPI SFTP Adapter - Remote file or directory not found
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI SFTP Adapter - Remote file or directory not found.
* Use this runbook only for object\_name CPI\_SFTP\_FILE\_NOT\_FOUND and taxonomy SFTP | FILESYSTEM | FILE\_NOT\_FOUND | REMOTE\_PATH.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: SFTP operation fails because the configured remote path or dynamic filename does not exist.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: SFTP Adapter.
* Protocol family: SFTP.
* Error pattern: SFTP | FILESYSTEM | FILE\_NOT\_FOUND | REMOTE\_PATH.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0087.
* Source KEDB artifact: KB\_RCMO\_CPI\_SFTP\_FILE\_NOT\_FOUND\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI SFTP Adapter - Remote file or directory not found.
* Normalized object\_name: CPI\_SFTP\_FILE\_NOT\_FOUND.
* Normalized taxonomy: SFTP | FILESYSTEM | FILE\_NOT\_FOUND | REMOTE\_PATH.
* Sample 1: 2026-04-06T22:30:49.957 | MessageGuid AGnUNBnbavGGocjWdJVbvCyhuISG | Interface IR\_IF034\_SFTP\_Passthrough\_Sample\_Source\_to\_Target | Sender n/a | Receiver n/a | Error: An internal server error occured: Cannot connect to sap-sftp://sapci@my-sftp-virtual-host:2288
* Sample 2: 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file
5. ERROR SIGNATURE
* Title: SAP CPI SFTP Adapter - Remote file or directory not found.
* Short symptom: SFTP operation fails because the configured remote path or dynamic filename does not exist.
* Normalized object name: CPI\_SFTP\_FILE\_NOT\_FOUND.
* Normalized taxonomy: SFTP | FILESYSTEM | FILE\_NOT\_FOUND | REMOTE\_PATH.
6. KNOWN ROOT CAUSES
* SFTP adapter points to the wrong directory.
* Dynamic filename header is not resolved.
* Target file or directory was removed before CPI access.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for remote path, filename, user, host, and MessageGuid.
* Verify dynamic filename headers before the SFTP adapter step.
* Confirm remote directory existence and permissions on the SFTP server.
* Compare the failing execution with the last successful MPL execution for CPI\_SFTP\_FILE\_NOT\_FOUND.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct the SFTP remote path and dynamic filename expression.
* Create the missing target directory with approved permissions.
* Replay one controlled file after path validation succeeds.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SFTP\_FILE\_NOT\_FOUND is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SFTP\_FILE\_NOT\_FOUND and SFTP | FILESYSTEM | FILE\_NOT\_FOUND | REMOTE\_PATH do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

