# SAP CPI Groovy XML Parser - XML parsing failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_GROOVY_XML_PARSE"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0072
KEDB TITLE
SAP CPI Groovy XML Parser - XML parsing failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* Groovy XmlSlurper or XML parser fails because the message body is malformed, has an invalid encoding, or contains an unexpected BOM.
* Canonical retrieval phrase: SAP CPI Groovy XML Parser - XML parsing failed.
* Normalized object_name: CPI_GROOVY_XML_PARSE.
2. ERROR PATTERN
* GROOVY | XML | PARSE | MALFORMED_XML
3. ROOT CAUSE
* Incoming XML payload is malformed or incomplete.
* Character encoding or BOM prevents the parser from reading the body.
* The script parses the body before XML validation.
4. DIAGNOSIS SIGNALS
* Check MPL payload before the Groovy step and preserve the exact parser error.
* Validate XML well-formedness and encoding outside CPI.
* Confirm whether a BOM or unsupported character exists in the body.
* Preserve runtime evidence: Evidence: 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_GROOVY_XML_PARSE and GROOVY | XML | PARSE | MALFORMED_XML during search and triage.
5. RESOLUTION
* Sanitize the XML payload before the Groovy parser step.
* Strip BOM and normalize encoding when approved by the interface contract.
* Validate XML before parsing and replay one corrected message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_GROOVY_XML_PARSE and GROOVY | XML | PARSE | MALFORMED_XML do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Route malformed XML to an error folder and request a corrected source payload.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_GROOVY_XML_PARSE_P1_v1.md
* Cross-reference object_name: CPI_GROOVY_XML_PARSE
* Cross-reference taxonomy: GROOVY | XML | PARSE | MALFORMED_XML
* Source KEDB ID: KEDB-P1-0072
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
