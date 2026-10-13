# SAP CPI Groovy XML Parser - XML parsing failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_GROOVY\_XML\_PARSE"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0072
RUNBOOK TITLE
SAP CPI Groovy XML Parser - XML parsing failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Groovy XML Parser - XML parsing failed.
* Use this runbook only for object\_name CPI\_GROOVY\_XML\_PARSE and taxonomy GROOVY | XML | PARSE | MALFORMED\_XML.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Groovy XmlSlurper or XML parser fails because the message body is malformed, has an invalid encoding, or contains an unexpected BOM.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Groovy Script/XML Parser.
* Protocol family: XML.
* Error pattern: GROOVY | XML | PARSE | MALFORMED\_XML.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0072.
* Source KEDB artifact: KB\_RCMO\_CPI\_GROOVY\_XML\_PARSE\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Groovy XML Parser - XML parsing failed.
* Normalized object\_name: CPI\_GROOVY\_XML\_PARSE.
* Normalized taxonomy: GROOVY | XML | PARSE | MALFORMED\_XML.
* Sample 1 | 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file.
* Sample 2 | 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
5. ERROR SIGNATURE
* Title: SAP CPI Groovy XML Parser - XML parsing failed.
* Short symptom: Groovy XmlSlurper or XML parser fails because the message body is malformed, has an invalid encoding, or contains an unexpected BOM.
* Normalized object name: CPI\_GROOVY\_XML\_PARSE.
* Normalized taxonomy: GROOVY | XML | PARSE | MALFORMED\_XML.
6. KNOWN ROOT CAUSES
* Incoming XML payload is malformed or incomplete.
* Character encoding or BOM prevents the parser from reading the body.
* The script parses the body before XML validation.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL payload before the Groovy step and preserve the exact parser error.
* Validate XML well-formedness and encoding outside CPI.
* Confirm whether a BOM or unsupported character exists in the body.
* Compare the failing execution with the last successful MPL execution for CPI\_GROOVY\_XML\_PARSE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Sanitize the XML payload before the Groovy parser step.
* Strip BOM and normalize encoding when approved by the interface contract.
* Validate XML before parsing and replay one corrected message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_GROOVY\_XML\_PARSE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_GROOVY\_XML\_PARSE and GROOVY | XML | PARSE | MALFORMED\_XML do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

