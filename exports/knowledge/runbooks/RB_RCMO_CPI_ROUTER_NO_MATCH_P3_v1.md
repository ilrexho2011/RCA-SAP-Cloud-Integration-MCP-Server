# SAP CPI Router - No condition matched

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_ROUTER\_NO\_MATCH"
priority: "P3"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P3-0083
RUNBOOK TITLE
SAP CPI Router - No condition matched
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P3
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Router - No condition matched.
* Use this runbook only for object\_name CPI\_ROUTER\_NO\_MATCH and taxonomy ROUTER | CONDITION | NO\_MATCH | DEFAULT\_MISSING.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Router does not select any branch because predicates do not cover the message variant or no default route exists.
* Priority: P3.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Router Step.
* Protocol family: CPI Runtime.
* Error pattern: ROUTER | CONDITION | NO\_MATCH | DEFAULT\_MISSING.
* System type: CPI.
* Source KEDB ID(s): KEDB-P3-0083.
* Source KEDB artifact: KB\_RCMO\_CPI\_ROUTER\_NO\_MATCH\_P3\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Router - No condition matched.
* Normalized object\_name: CPI\_ROUTER\_NO\_MATCH.
* Normalized taxonomy: ROUTER | CONDITION | NO\_MATCH | DEFAULT\_MISSING.
* Sample 1: 2026-03-27T18:54:27.780 | MessageGuid AGnG0mNnmIUL5nAp0d4ysw8CDqZA | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: Could not match segment: 'MessageProcessingLogs('AGmt6OsRi31wm\_R6tJgjIJkgS3s0')/ErrorInformation/$value'
* Sample 2: 2026-03-27T18:35:58.153 | MessageGuid AGnGzg4AqBu2lLPf7xAP6hIeffnB | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: Could not match segment: 'MessageProcessingLogs('AGmt6OsRi31wm\_R6tJgjIJkgS3s0')/ErrorInformation/$value'
5. ERROR SIGNATURE
* Title: SAP CPI Router - No condition matched.
* Short symptom: Router does not select any branch because predicates do not cover the message variant or no default route exists.
* Normalized object name: CPI\_ROUTER\_NO\_MATCH.
* Normalized taxonomy: ROUTER | CONDITION | NO\_MATCH | DEFAULT\_MISSING.
6. KNOWN ROOT CAUSES
* Message variant is not covered by router predicates.
* Default branch is missing.
* Predicate logic is not null-safe for optional fields.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL before the Router step and inspect fields used by predicates.
* Evaluate each router condition against the failing payload.
* Confirm whether a default branch exists for unmatched messages.
* Compare the failing execution with the last successful MPL execution for CPI\_ROUTER\_NO\_MATCH.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Add a default branch for unmatched messages.
* Update router predicates to cover current message variants.
* Add null-safe checks to predicate expressions and replay one controlled message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_ROUTER\_NO\_MATCH is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_ROUTER\_NO\_MATCH and ROUTER | CONDITION | NO\_MATCH | DEFAULT\_MISSING do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

