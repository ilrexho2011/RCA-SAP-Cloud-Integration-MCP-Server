# SAP CPI JSON Converter - Invalid JSON payload parse error

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_CONVERTER\_JSON\_PARSE"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0066
RUNBOOK TITLE
SAP CPI JSON Converter - Invalid JSON payload parse error
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI JSON Converter - Invalid JSON payload parse error.
* Use this runbook only for object\_name CPI\_CONVERTER\_JSON\_PARSE and taxonomy CONVERTER | JSON | PARSE | MALFORMED\_JSON.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: JSON to XML conversion fails because the incoming JSON payload is malformed, empty, truncated, or structurally inconsistent.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: JSON to XML Converter.
* Protocol family: HTTP/JSON.
* Error pattern: CONVERTER | JSON | PARSE | MALFORMED\_JSON.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0066.
* Source KEDB artifact: KB\_RCMO\_CPI\_CONVERTER\_JSON\_PARSE\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI JSON Converter - Invalid JSON payload parse error.
* Normalized object\_name: CPI\_CONVERTER\_JSON\_PARSE.
* Normalized taxonomy: CONVERTER | JSON | PARSE | MALFORMED\_JSON.
* Sample 1: 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file
* Sample 2: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
5. ERROR SIGNATURE
* Title: SAP CPI JSON Converter - Invalid JSON payload parse error.
* Short symptom: JSON to XML conversion fails because the incoming JSON payload is malformed, empty, truncated, or structurally inconsistent.
* Normalized object name: CPI\_CONVERTER\_JSON\_PARSE.
* Normalized taxonomy: CONVERTER | JSON | PARSE | MALFORMED\_JSON.
6. KNOWN ROOT CAUSES
* Sender delivers malformed JSON, invalid arrays, or inconsistent object structures.
* Payload is empty or truncated before the converter step.
* No pre-validation rejects invalid JSON before conversion.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL before the converter step and capture the raw payload sample.
* Validate the JSON with the agreed schema and confirm array/object consistency.
* Confirm that Content-Type and character encoding are correct.
* Compare the failing execution with the last successful MPL execution for CPI\_CONVERTER\_JSON\_PARSE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Reject invalid JSON with a precise sender-facing error response.
* Normalize the JSON structure before conversion when business rules allow correction.
* Add schema validation before the JSON to XML Converter and replay one corrected payload.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_CONVERTER\_JSON\_PARSE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_CONVERTER\_JSON\_PARSE and CONVERTER | JSON | PARSE | MALFORMED\_JSON do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

