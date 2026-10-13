# Mapping Function Families and Use Cases

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "MAPPING_FUNCTION_FAMILIES_AND_USE_CASES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-105

DOC TITLE
Mapping Function Families and Use Cases

1. PURPOSE
- This guide condenses the SAP Help pages behind Mapping Function Families and Use Cases into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: mapping, string, date, node.

2. SCOPE
- Primary source scope: Mapping Function Families and Use Cases and closely related SAP Help pages.
- Chunking hint: model; transform; validate; reuse.
- Preferred retrieval anchors: mapping function families and use cases, model, transform, validate, function.

3. KEY TERMS
- Model
- Transform
- Validate
- Reuse

4. CORE EXPLANATION
- Keep exact SAP terminology for mapping so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Mapping Function Families and Use Cases into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating mapping as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of mapping function families and use cases in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for mapping function families and use cases?
- What evidence and search anchors should be stored for mapping function families and use cases, model, transform?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-105
- Related runbooks: RB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md, RB_RCMO_CPI_XSLT_TRANSFORMATION_COMPILE_OR_RUNTIME_ERROR_P2_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related catalog objects: IR16_IF01_Northwind_Orders_via_OrderID_in_Payload_using_Variable
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-mapping-guidelines-basics
