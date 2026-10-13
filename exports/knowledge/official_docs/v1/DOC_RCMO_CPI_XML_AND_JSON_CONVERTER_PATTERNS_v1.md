# XML and JSON Converter Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "XML_AND_JSON_CONVERTER_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-126

DOC TITLE
XML and JSON Converter Patterns

1. PURPOSE
- This guide condenses the SAP Help pages behind XML and JSON Converter Patterns into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: xml, json, converter.

2. SCOPE
- Primary source scope: XML and JSON Converter Patterns and closely related SAP Help pages.
- Chunking hint: define; configure; validate; operate.
- Preferred retrieval anchors: xml and json converter patterns, define, configure, validate, xml.

3. KEY TERMS
- Define
- Configure
- Validate
- Operate

4. CORE EXPLANATION
- Keep exact SAP terminology for xml so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind XML and JSON Converter Patterns into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating xml as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of xml and json converter patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for xml and json converter patterns?
- What evidence and search anchors should be stored for xml and json converter patterns, define, configure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-126
- Related runbooks: RB_RCMO_CPI_PAYLOAD_JSON_PARSE_FAILURE_P2_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, RB_RCMO_CPI_FILE_ENCODING_UTF8_BOM_WARNING_P3_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md, KB_RCMO_CPI_PAYLOAD_JSON_PARSE_FAILURE_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
