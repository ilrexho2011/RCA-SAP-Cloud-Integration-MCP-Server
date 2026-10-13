# SAP CPI Groovy Script - NullPointerException during processing

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_GROOVY\_NPE"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0071
RUNBOOK TITLE
SAP CPI Groovy Script - NullPointerException during processing
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Groovy Script - NullPointerException during processing.
* Use this runbook only for object\_name CPI\_GROOVY\_NPE and taxonomy GROOVY | SCRIPT | NULL\_POINTER | NPE.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Groovy script fails with NullPointerException because a property, header, body node, or parsed value is missing.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Groovy Script.
* Protocol family: CPI Runtime.
* Error pattern: GROOVY | SCRIPT | NULL\_POINTER | NPE.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0071.
* Source KEDB artifact: KB\_RCMO\_CPI\_GROOVY\_NPE\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Groovy Script - NullPointerException during processing.
* Normalized object\_name: CPI\_GROOVY\_NPE.
* Normalized taxonomy: GROOVY | SCRIPT | NULL\_POINTER | NPE.
* Sample 1: Business process | Scenario-dependent CPI integration processing | Critical | Script step fails with NullPointerException
* Sample 1 | 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
5. ERROR SIGNATURE
* Title: SAP CPI Groovy Script - NullPointerException during processing.
* Short symptom: Groovy script fails with NullPointerException because a property, header, body node, or parsed value is missing.
* Normalized object name: CPI\_GROOVY\_NPE.
* Normalized taxonomy: GROOVY | SCRIPT | NULL\_POINTER | NPE.
6. KNOWN ROOT CAUSES
* Script reads a missing property, header, or body node without a null check.
* Payload validation is missing before script access.
* Default values are not defined for optional fields.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL exception details and identify the exact script line or missing value.
* Verify all required headers, properties, and payload nodes before the script step.
* Compare failing payload with the last successful payload.
* Compare the failing execution with the last successful MPL execution for CPI\_GROOVY\_NPE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Add defensive null checks before reading properties, headers, or body nodes.
* Set approved default values for optional fields.
* Reject payloads with missing mandatory values before the Groovy step.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_GROOVY\_NPE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_GROOVY\_NPE and GROOVY | SCRIPT | NULL\_POINTER | NPE do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

