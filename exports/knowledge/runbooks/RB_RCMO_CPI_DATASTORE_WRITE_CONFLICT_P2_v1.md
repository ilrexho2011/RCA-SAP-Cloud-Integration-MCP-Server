# SAP CPI Data Store - Write conflict on existing key

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_DATASTORE\_WRITE\_CONFLICT"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0068
RUNBOOK TITLE
SAP CPI Data Store - Write conflict on existing key
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Data Store - Write conflict on existing key.
* Use this runbook only for object\_name CPI\_DATASTORE\_WRITE\_CONFLICT and taxonomy DATASTORE | WRITE | CONFLICT | KEY\_COLLISION.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Data Store write fails because concurrent messages or duplicate business keys target the same entry.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Data Store.
* Protocol family: CPI Runtime.
* Error pattern: DATASTORE | WRITE | CONFLICT | KEY\_COLLISION.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0068.
* Source KEDB artifact: KB\_RCMO\_CPI\_DATASTORE\_WRITE\_CONFLICT\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Data Store - Write conflict on existing key.
* Normalized object\_name: CPI\_DATASTORE\_WRITE\_CONFLICT.
* Normalized taxonomy: DATASTORE | WRITE | CONFLICT | KEY\_COLLISION.
* Sample 1: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI Data Store - Write conflict on existing key.
* Short symptom: Data Store write fails because concurrent messages or duplicate business keys target the same entry.
* Normalized object name: CPI\_DATASTORE\_WRITE\_CONFLICT.
* Normalized taxonomy: DATASTORE | WRITE | CONFLICT | KEY\_COLLISION.
6. KNOWN ROOT CAUSES
* Multiple messages write the same Data Store key in parallel.
* The key design is not unique for the business object.
* Overwrite handling is not aligned with the process idempotency rule.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for concurrent executions with the same Data Store key.
* Compare the key expression with the business object uniqueness rule.
* Confirm whether overwrite, update, or reject behavior is expected.
* Compare the failing execution with the last successful MPL execution for CPI\_DATASTORE\_WRITE\_CONFLICT.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Use a unique composite key for each independent business object.
* Serialize processing for keys that must be updated sequentially.
* Apply controlled retry only after the conflicting execution is completed.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_DATASTORE\_WRITE\_CONFLICT is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_DATASTORE\_WRITE\_CONFLICT and DATASTORE | WRITE | CONFLICT | KEY\_COLLISION do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

