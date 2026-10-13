# SAP CPI EDI Parser - EDI document parsing failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_EDI_PARSE"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0069
KEDB TITLE
SAP CPI EDI Parser - EDI document parsing failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* EDI parsing fails because segment order, version, delimiters, or mandatory segments do not match the B2B agreement.
* Canonical retrieval phrase: SAP CPI EDI Parser - EDI document parsing failed.
* Normalized object_name: CPI_EDI_PARSE.
2. ERROR PATTERN
* EDI | PARSE | DOCUMENT | FAILED
3. ROOT CAUSE
* Partner sends an unsupported EDI version or invalid segment order.
* Required EDI segments or delimiters are missing.
* The B2B agreement or MIG does not match the partner payload.
4. DIAGNOSIS SIGNALS
* Check the failing segment and EDI version in MPL or B2B monitoring.
* Validate the EDI sample against the agreed MIG/interface guideline.
* Compare partner agreement settings with the runtime payload.
* Preserve runtime evidence: Evidence: 2026-04-06T19:45:55.902 | MessageGuid AGnUDXMPO5FvNlGgQRQdYZQ-o65c | Interface IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP | Sender n/a | Receiver n/a | Error: An internal server error occured: Failure converting a node of class javax.xml.transform.sax.SAXSource: org.xml.sax.SAXParseException; lineNumber: 1; columnNumber: 1; Premature end of file
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_EDI_PARSE and EDI | PARSE | DOCUMENT | FAILED during search and triage.
5. RESOLUTION
* Correct the EDI payload or update the partner agreement according to the approved MIG.
* Align delimiters, segment order, and version settings.
* Replay one corrected EDI message after partner confirmation.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_EDI_PARSE and EDI | PARSE | DOCUMENT | FAILED do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Hold invalid EDI files in the error folder and request corrected payload from the partner.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_EDI_PARSE_P2_v1.md
* Cross-reference object_name: CPI_EDI_PARSE
* Cross-reference taxonomy: EDI | PARSE | DOCUMENT | FAILED
* Source KEDB ID: KEDB-P2-0069
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
