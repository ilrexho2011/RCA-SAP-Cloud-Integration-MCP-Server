# SAP CPI XSLT Mapping - Stylesheet compilation error

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_XSLT\_COMPILE"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0093
RUNBOOK TITLE
SAP CPI XSLT Mapping - Stylesheet compilation error
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI XSLT Mapping - Stylesheet compilation error.
* Use this runbook only for object\_name CPI\_XSLT\_COMPILE and taxonomy XSLT | COMPILE | SYNTAX | ERROR.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: XSLT mapping fails because the stylesheet contains invalid syntax, unsupported functions, or incompatible runtime constructs.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: XSLT Mapping.
* Protocol family: XML/XSLT.
* Error pattern: XSLT | COMPILE | SYNTAX | ERROR.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0093.
* Source KEDB artifact: KB\_RCMO\_CPI\_XSLT\_COMPILE\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI XSLT Mapping - Stylesheet compilation error.
* Normalized object\_name: CPI\_XSLT\_COMPILE.
* Normalized taxonomy: XSLT | COMPILE | SYNTAX | ERROR.
* Sample 1: MPL evidence | Sample 1: No directly matching MPL example available in the provided export.
* Sample 2: Evidence required | MessageGuid | time window | failing step if known | error text | configuration delta | replay outcome
5. ERROR SIGNATURE
* Title: SAP CPI XSLT Mapping - Stylesheet compilation error.
* Short symptom: XSLT mapping fails because the stylesheet contains invalid syntax, unsupported functions, or incompatible runtime constructs.
* Normalized object name: CPI\_XSLT\_COMPILE.
* Normalized taxonomy: XSLT | COMPILE | SYNTAX | ERROR.
6. KNOWN ROOT CAUSES
* Stylesheet syntax is invalid.
* Unsupported extension function is used.
* XSLT artifact version is not deployed with the expected content.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for XSLT compile error and exact line or function reference.
* Validate the stylesheet outside CPI with the target XSLT version.
* Confirm deployed XSLT artifact version in the iFlow package.
* Compare the failing execution with the last successful MPL execution for CPI\_XSLT\_COMPILE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Fix stylesheet syntax and remove unsupported functions.
* Redeploy the corrected XSLT artifact with the iFlow.
* Replay one controlled XML message after compilation succeeds.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_XSLT\_COMPILE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_XSLT\_COMPILE and XSLT | COMPILE | SYNTAX | ERROR do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

