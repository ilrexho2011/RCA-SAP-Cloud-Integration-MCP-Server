# Reusable Script Utilities and Collections

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "REUSABLE_SCRIPT_UTILITIES_AND_COLLECTIONS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-133

DOC TITLE
Reusable Script Utilities and Collections

1. PURPOSE
- This guide condenses the SAP Help pages behind Reusable Script Utilities and Collections into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: reusable, script collection, groovy.

2. SCOPE
- Primary source scope: Reusable Script Utilities and Collections and closely related SAP Help pages.
- Chunking hint: read; change; validate; return.
- Preferred retrieval anchors: reusable script utilities and collections, read, change, validate, reusable.

3. KEY TERMS
- Read
- Change
- Validate
- Return

4. CORE EXPLANATION
- Keep exact SAP terminology for reusable so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Reusable Script Utilities and Collections into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating reusable as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of reusable script utilities and collections in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for reusable script utilities and collections?
- What evidence and search anchors should be stored for reusable script utilities and collections, read, change?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-133
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/general-scripting-guidelines
