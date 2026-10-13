# SAP CPI Runtime - Deployed artifact version mismatch

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_RUNTIME\_VERSION\_MISMATCH"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0084
RUNBOOK TITLE
SAP CPI Runtime - Deployed artifact version mismatch
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Runtime - Deployed artifact version mismatch.
* Use this runbook only for object\_name CPI\_RUNTIME\_VERSION\_MISMATCH and taxonomy RUNTIME | DEPLOYMENT | VERSION\_MISMATCH | OLD\_ARTIFACT.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Runtime behavior differs from design expectation because an old or incomplete artifact version is active.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: CPI Runtime/Deployment.
* Protocol family: CPI Runtime.
* Error pattern: RUNTIME | DEPLOYMENT | VERSION\_MISMATCH | OLD\_ARTIFACT.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0084.
* Source KEDB artifact: KB\_RCMO\_CPI\_RUNTIME\_VERSION\_MISMATCH\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Runtime - Deployed artifact version mismatch.
* Normalized object\_name: CPI\_RUNTIME\_VERSION\_MISMATCH.
* Normalized taxonomy: RUNTIME | DEPLOYMENT | VERSION\_MISMATCH | OLD\_ARTIFACT.
* Sample 1: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Sample 2: Check MPL API for the failing time window and correlate the MessageGuid with the runtime error.
5. ERROR SIGNATURE
* Title: SAP CPI Runtime - Deployed artifact version mismatch.
* Short symptom: Runtime behavior differs from design expectation because an old or incomplete artifact version is active.
* Normalized object name: CPI\_RUNTIME\_VERSION\_MISMATCH.
* Normalized taxonomy: RUNTIME | DEPLOYMENT | VERSION\_MISMATCH | OLD\_ARTIFACT.
6. KNOWN ROOT CAUSES
* Old artifact version remains deployed.
* Transport or deployment pipeline did not complete.
* Multiple package versions create ambiguity for operators.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check deployed artifact version in CPI Monitor and Design view.
* Compare runtime timestamp with the expected transport or deployment record.
* Verify that the intended package version is active.
* Compare the failing execution with the last successful MPL execution for CPI\_RUNTIME\_VERSION\_MISMATCH.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Redeploy the target artifact version from the approved package.
* Clean failed or incomplete transport pipeline state.
* Run one controlled test message after deployment completes.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_RUNTIME\_VERSION\_MISMATCH is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_RUNTIME\_VERSION\_MISMATCH and RUNTIME | DEPLOYMENT | VERSION\_MISMATCH | OLD\_ARTIFACT do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

