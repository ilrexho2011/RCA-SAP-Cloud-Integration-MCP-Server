# Create Custom Mapping

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CREATE_CUSTOM_MAPPING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-121

DOC TITLE
Create Custom Mapping

1. PURPOSE
- This guide condenses the SAP Help pages behind Create Custom Mapping into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: custom mapping, mapping.

2. SCOPE
- Primary source scope: Create Custom Mapping and closely related SAP Help pages.
- Chunking hint: model; transform; validate; reuse.
- Preferred retrieval anchors: create custom mapping, model, transform, validate.

3. KEY TERMS
- Model
- Transform
- Validate
- Reuse

4. CORE EXPLANATION
- Keep exact SAP terminology for custom mapping so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Create Custom Mapping into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating custom mapping as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of create custom mapping in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for create custom mapping?
- What evidence and search anchors should be stored for create custom mapping, model, transform?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-121
- Related runbooks: RB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, RB_RCMO_CPI_XSLT_TRANSFORMATION_COMPILE_OR_RUNTIME_ERROR_P2_v1.md, RB_RCMO_CPI_MAPPING_DATA_QUALITY_OPTIONAL_FIELD_TRUNCATED_P3_v1.md
- Related KEDB: KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, KB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/creating-custom-mapping
