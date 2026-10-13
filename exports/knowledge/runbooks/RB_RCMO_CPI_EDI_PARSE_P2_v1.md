# SAP CPI EDI Parser - EDI document parsing failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_EDI\_PARSE"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0069
RUNBOOK TITLE
SAP CPI EDI Parser - EDI document parsing failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI EDI Parser - EDI document parsing failed.
* Use this runbook only for object\_name CPI\_EDI\_PARSE and taxonomy EDI | PARSE | DOCUMENT | FAILED.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: EDI parsing fails because segment order, version, delimiters, or mandatory segments do not match the B2B agreement.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: EDI Parser.
* Protocol family: EDI/B2B.
* Error pattern: EDI | PARSE | DOCUMENT | FAILED.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0069.
* Source KEDB artifact: KB\_RCMO\_CPI\_EDI\_PARSE\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI EDI Parser - EDI document parsing failed.
* Normalized object\_name: CPI\_EDI\_PARSE.
* Normalized taxonomy: EDI | PARSE | DOCUMENT | FAILED.
* Sample 1 | 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Messages\_Text\_AI4BIZ\_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file
* Sample 2 | 2026-03-27T18:06:40.764 | MessageGuid AGnGxzAhwSMqE-yFCo6gtwINs6s2 | Interface IR01\_IF13\_Fetching\_Failed\_Iflow\_Error\_Message\_Details | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 2; columnNumber: 41; The element type "StartDate" must be terminated by the matching end-tag "</StartDate>"
5. ERROR SIGNATURE
* Title: SAP CPI EDI Parser - EDI document parsing failed.
* Short symptom: EDI parsing fails because segment order, version, delimiters, or mandatory segments do not match the B2B agreement.
* Normalized object name: CPI\_EDI\_PARSE.
* Normalized taxonomy: EDI | PARSE | DOCUMENT | FAILED.
6. KNOWN ROOT CAUSES
* Partner sends an unsupported EDI version or invalid segment order.
* Required EDI segments or delimiters are missing.
* The B2B agreement or MIG does not match the partner payload.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check the failing segment and EDI version in MPL or B2B monitoring.
* Validate the EDI sample against the agreed MIG/interface guideline.
* Compare partner agreement settings with the runtime payload.
* Compare the failing execution with the last successful MPL execution for CPI\_EDI\_PARSE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct the EDI payload or update the partner agreement according to the approved MIG.
* Align delimiters, segment order, and version settings.
* Replay one corrected EDI message after partner confirmation.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_EDI\_PARSE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_EDI\_PARSE and EDI | PARSE | DOCUMENT | FAILED do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

