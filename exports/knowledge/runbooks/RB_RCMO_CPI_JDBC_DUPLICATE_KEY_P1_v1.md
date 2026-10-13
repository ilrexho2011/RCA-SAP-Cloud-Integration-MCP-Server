# SAP CPI JDBC Adapter - SQL duplicate key violation

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_JDBC\_DUPLICATE\_KEY"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0076
RUNBOOK TITLE
SAP CPI JDBC Adapter - SQL duplicate key violation
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI JDBC Adapter - SQL duplicate key violation.
* Use this runbook only for object\_name CPI\_JDBC\_DUPLICATE\_KEY and taxonomy JDBC | SQL | DUPLICATE\_KEY | UNIQUE\_CONSTRAINT.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: JDBC insert or update fails because the target table unique constraint already contains the business key.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: JDBC Receiver Adapter.
* Protocol family: JDBC/SQL.
* Error pattern: JDBC | SQL | DUPLICATE\_KEY | UNIQUE\_CONSTRAINT.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0076.
* Source KEDB artifact: KB\_RCMO\_CPI\_JDBC\_DUPLICATE\_KEY\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI JDBC Adapter - SQL duplicate key violation.
* Normalized object\_name: CPI\_JDBC\_DUPLICATE\_KEY.
* Normalized taxonomy: JDBC | SQL | DUPLICATE\_KEY | UNIQUE\_CONSTRAINT.
* Sample 1: Use this runbook for SAP CPI operations and incident guidance when the JDBC Adapter fails on a duplicate key condition.
* Sample 1: No directly matching MPL example available in the provided export.
5. ERROR SIGNATURE
* Title: SAP CPI JDBC Adapter - SQL duplicate key violation.
* Short symptom: JDBC insert or update fails because the target table unique constraint already contains the business key.
* Normalized object name: CPI\_JDBC\_DUPLICATE\_KEY.
* Normalized taxonomy: JDBC | SQL | DUPLICATE\_KEY | UNIQUE\_CONSTRAINT.
6. KNOWN ROOT CAUSES
* Payload contains an already processed business key.
* The interface uses insert logic where upsert or idempotency is required.
* Replay sends duplicate records without duplicate control.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL and database error for duplicate key or unique constraint text.
* Identify the business key and confirm whether the target row already exists.
* Compare replay history and idempotency repository for the same key.
* Compare the failing execution with the last successful MPL execution for CPI\_JDBC\_DUPLICATE\_KEY.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Implement deduplication before the JDBC write.
* Use upsert logic only when the target design allows update on existing keys.
* Record processed business keys in an idempotency repository.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_JDBC\_DUPLICATE\_KEY is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_JDBC\_DUPLICATE\_KEY and JDBC | SQL | DUPLICATE\_KEY | UNIQUE\_CONSTRAINT do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

