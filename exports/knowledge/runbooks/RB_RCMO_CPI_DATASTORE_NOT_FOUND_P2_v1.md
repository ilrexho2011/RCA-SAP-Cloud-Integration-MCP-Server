# SAP CPI Data Store - Entry not found during read

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_DATASTORE\_NOT\_FOUND"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0067
RUNBOOK TITLE
SAP CPI Data Store - Entry not found during read
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Data Store - Entry not found during read.
* Use this runbook only for object\_name CPI\_DATASTORE\_NOT\_FOUND and taxonomy DATASTORE | READ | NOT\_FOUND | KEY\_MISSING.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Data Store read step cannot find the expected entry for the resolved key.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Data Store.
* Protocol family: CPI Runtime.
* Error pattern: DATASTORE | READ | NOT\_FOUND | KEY\_MISSING.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0067.
* Source KEDB artifact: KB\_RCMO\_CPI\_DATASTORE\_NOT\_FOUND\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Data Store - Entry not found during read.
* Normalized object\_name: CPI\_DATASTORE\_NOT\_FOUND.
* Normalized taxonomy: DATASTORE | READ | NOT\_FOUND | KEY\_MISSING.
* Sample 1: 2026-04-10T12:46:07.444 | MessageGuid AGnY8Q-*BPrbVBCyJpSOg5xiFWd* | Interface Football\_Service | Sender n/a | Receiver n/a | Error: An internal server error occured: (404) Not Found \[HTTP/1.1 404 Not Found]
* Sample 2: 2026-04-07T22:40:18.493 | MessageGuid AGnVh9Lo7tcE1ADE6wMcvuI4kf3y | Interface IR16\_IF01\_Northwind\_Orders\_via\_OrderID\_in\_Payload\_using\_Variable | Sender n/a | Receiver n/a | Error: An internal server error occured: No encryption key id could be found or created. Please check the System Log for details
5. ERROR SIGNATURE
* Title: SAP CPI Data Store - Entry not found during read.
* Short symptom: Data Store read step cannot find the expected entry for the resolved key.
* Normalized object name: CPI\_DATASTORE\_NOT\_FOUND.
* Normalized taxonomy: DATASTORE | READ | NOT\_FOUND | KEY\_MISSING.
6. KNOWN ROOT CAUSES
* Read key pattern differs from the write key pattern.
* The write branch was skipped or failed before the read step.
* Retention, cleanup, or wrong store name removed the expected entry.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check the resolved Data Store name and key in MPL properties and headers.
* Verify that the write step completed before the read step for the same key.
* Compare retention settings and cleanup jobs for the target Data Store.
* Compare the failing execution with the last successful MPL execution for CPI\_DATASTORE\_NOT\_FOUND.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Standardize the Data Store key pattern across write and read steps.
* Add an existence check before the read step.
* Replay one controlled message after confirming the key was written.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_DATASTORE\_NOT\_FOUND is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_DATASTORE\_NOT\_FOUND and DATASTORE | READ | NOT\_FOUND | KEY\_MISSING do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

