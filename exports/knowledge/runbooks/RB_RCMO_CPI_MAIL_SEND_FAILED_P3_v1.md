# SAP CPI Mail Adapter - SMTP send failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_MAIL\_SEND\_FAILED"
priority: "P3"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P3-0078
RUNBOOK TITLE
SAP CPI Mail Adapter - SMTP send failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P3
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Mail Adapter - SMTP send failed.
* Use this runbook only for object\_name CPI\_MAIL\_SEND\_FAILED and taxonomy MAIL | SMTP | SEND | FAILED.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Mail adapter send fails because SMTP host, port, authentication, TLS, or recipient configuration is invalid.
* Priority: P3.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Mail Receiver Adapter.
* Protocol family: SMTP.
* Error pattern: MAIL | SMTP | SEND | FAILED.
* System type: CPI.
* Source KEDB ID(s): KEDB-P3-0078.
* Source KEDB artifact: KB\_RCMO\_CPI\_MAIL\_SEND\_FAILED\_P3\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Mail Adapter - SMTP send failed.
* Normalized object\_name: CPI\_MAIL\_SEND\_FAILED.
* Normalized taxonomy: MAIL | SMTP | SEND | FAILED.
* Sample 1 | 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Sample 2 | 2026-03-27T15:43:25.113 | MessageGuid AGnGpZ3UHQ5QWS1Qbv9-YTFqTEQ1 | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: org.codehaus.groovy.control.MultipleCompilationErrorsException: startup failed: script2\_\_Script.groovy: 2: unable to resolve class groovy.xml.XmlSlurper @ line 2, column 1. import groovy.xml.XmlSlurper ^ 1 error
5. ERROR SIGNATURE
* Title: SAP CPI Mail Adapter - SMTP send failed.
* Short symptom: Mail adapter send fails because SMTP host, port, authentication, TLS, or recipient configuration is invalid.
* Normalized object name: CPI\_MAIL\_SEND\_FAILED.
* Normalized taxonomy: MAIL | SMTP | SEND | FAILED.
6. KNOWN ROOT CAUSES
* SMTP host, port, authentication, or TLS setting is wrong.
* Mail credential alias is expired or invalid.
* Recipient address or relay policy rejects the message.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for SMTP status, receiver host, and MessageGuid.
* Verify Mail adapter host, port, security mode, credential alias, and recipient list.
* Test relay policy with the mail service owner.
* Compare the failing execution with the last successful MPL execution for CPI\_MAIL\_SEND\_FAILED.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct SMTP host, port, authentication, TLS, and recipient configuration.
* Update expired credentials in CPI Security Material.
* Redeploy and send one controlled test notification.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_MAIL\_SEND\_FAILED is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_MAIL\_SEND\_FAILED and MAIL | SMTP | SEND | FAILED do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

