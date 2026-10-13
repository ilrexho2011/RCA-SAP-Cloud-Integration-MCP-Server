# SAP CPI SFTP Adapter - Authentication failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SFTP\_AUTH"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0086
RUNBOOK TITLE
SAP CPI SFTP Adapter - Authentication failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI SFTP Adapter - Authentication failed.
* Use this runbook only for object\_name CPI\_SFTP\_AUTH and taxonomy SFTP | AUTHENTICATION | LOGIN\_FAILURE | CONNECTION\_DENIED.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: SFTP login fails because SSH key, user, password, known host, or account status is invalid.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: SFTP Adapter.
* Protocol family: SFTP.
* Error pattern: SFTP | AUTHENTICATION | LOGIN\_FAILURE | CONNECTION\_DENIED.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0086.
* Source KEDB artifact: KB\_RCMO\_CPI\_SFTP\_AUTH\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI SFTP Adapter - Authentication failed.
* Normalized object\_name: CPI\_SFTP\_AUTH.
* Normalized taxonomy: SFTP | AUTHENTICATION | LOGIN\_FAILURE | CONNECTION\_DENIED.
* Sample 1: 2026-04-06T22:30:49.957 | MessageGuid AGnUNBnbavGGocjWdJVbvCyhuISG | Interface IR\_IF034\_SFTP\_Passthrough\_Sample\_Source\_to\_Target | Sender n/a | Receiver n/a | Error: An internal server error occured: Cannot connect to sap-sftp://sapci@my-sftp-virtual-host:2288
* Sample 2: 2026-04-06T19:48:07.956 | MessageGuid AGnUDfc8gJdz30wC7Gpxjhs\_tuwP | Interface Test\_Email\_with\_OAuth2\_Code | Sender n/a | Receiver n/a | Error: An internal server error occured: OAUTH2 asked for more
5. ERROR SIGNATURE
* Title: SAP CPI SFTP Adapter - Authentication failed.
* Short symptom: SFTP login fails because SSH key, user, password, known host, or account status is invalid.
* Normalized object name: CPI\_SFTP\_AUTH.
* Normalized taxonomy: SFTP | AUTHENTICATION | LOGIN\_FAILURE | CONNECTION\_DENIED.
6. KNOWN ROOT CAUSES
* SSH key pair or credential alias is wrong or expired.
* SFTP user is disabled or mapped to the wrong home folder.
* Known host entry or algorithm policy rejects the connection.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for SFTP authentication error, user, host, and MessageGuid.
* Verify credential alias, SSH key pair, known host, and username.
* Confirm account status and home folder mapping with SFTP administrator.
* Compare the failing execution with the last successful MPL execution for CPI\_SFTP\_AUTH.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Upload the correct SSH key pair and credential alias.
* Correct username, known host, and home folder mapping.
* Test the SFTP adapter connection and replay one controlled file.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SFTP\_AUTH is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SFTP\_AUTH and SFTP | AUTHENTICATION | LOGIN\_FAILURE | CONNECTION\_DENIED do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

