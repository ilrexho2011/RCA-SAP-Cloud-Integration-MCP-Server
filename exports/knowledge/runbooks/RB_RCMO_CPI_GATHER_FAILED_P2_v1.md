# SAP CPI Gather - Aggregation failed after split branches

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_GATHER\_FAILED"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0070
RUNBOOK TITLE
SAP CPI Gather - Aggregation failed after split branches
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Gather - Aggregation failed after split branches.
* Use this runbook only for object\_name CPI\_GATHER\_FAILED and taxonomy GATHER | AGGREGATION | FAILED | CORRELATION\_ERROR.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Gather aggregation fails because split branches cannot be correlated or return incompatible message structures.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Gather Step.
* Protocol family: CPI Runtime.
* Error pattern: GATHER | AGGREGATION | FAILED | CORRELATION\_ERROR.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0070.
* Source KEDB artifact: KB\_RCMO\_CPI\_GATHER\_FAILED\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Gather - Aggregation failed after split branches.
* Normalized object\_name: CPI\_GATHER\_FAILED.
* Normalized taxonomy: GATHER | AGGREGATION | FAILED | CORRELATION\_ERROR.
* Sample 1: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Sample 2: 2026-03-27T15:43:25.113 | MessageGuid AGnGpZ3UHQ5QWS1Qbv9-YTFqTEQ1 | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: org.codehaus.groovy.control.MultipleCompilationErrorsException: startup failed: script2\_\_Script.groovy: 2: unable to resolve class groovy.xml.XmlSlurper @ line 2, column 1. import groovy.xml.XmlSlurper ^ 1 error
5. ERROR SIGNATURE
* Title: SAP CPI Gather - Aggregation failed after split branches.
* Short symptom: Gather aggregation fails because split branches cannot be correlated or return incompatible message structures.
* Normalized object name: CPI\_GATHER\_FAILED.
* Normalized taxonomy: GATHER | AGGREGATION | FAILED | CORRELATION\_ERROR.
6. KNOWN ROOT CAUSES
* Correlation ID is missing in one or more branches.
* A branch fails before the Gather step.
* Branch output structure differs from the expected aggregation format.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check each split branch in MPL and confirm branch completion before Gather.
* Verify that the correlation ID is preserved across all branches.
* Compare branch output body and headers before aggregation.
* Compare the failing execution with the last successful MPL execution for CPI\_GATHER\_FAILED.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Preserve correlation IDs across all split branches.
* Normalize branch output structures before Gather.
* Handle failed branches before aggregation and replay one controlled message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_GATHER\_FAILED is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_GATHER\_FAILED and GATHER | AGGREGATION | FAILED | CORRELATION\_ERROR do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

