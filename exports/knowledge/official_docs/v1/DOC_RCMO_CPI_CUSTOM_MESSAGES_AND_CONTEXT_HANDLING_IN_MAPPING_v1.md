# Custom Messages and Context Handling in Mapping

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CUSTOM_MESSAGES_AND_CONTEXT_HANDLING_IN_MAPPING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-104

DOC TITLE
Custom Messages and Context Handling in Mapping

1. PURPOSE
- This guide condenses the SAP Help pages behind Custom Messages and Context Handling in Mapping into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: mapping, custom message, context.

2. SCOPE
- Primary source scope: Custom Messages and Context Handling in Mapping and closely related SAP Help pages.
- Chunking hint: model; transform; validate; reuse.
- Preferred retrieval anchors: custom messages and context handling in mapping, model, transform, validate, messages.

3. KEY TERMS
- Model
- Transform
- Validate
- Reuse

4. CORE EXPLANATION
- Keep exact SAP terminology for mapping so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Custom Messages and Context Handling in Mapping into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating mapping as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of custom messages and context handling in mapping in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for custom messages and context handling in mapping?
- What evidence and search anchors should be stored for custom messages and context handling in mapping, model, transform?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-104
- Related runbooks: RB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, RB_RCMO_CPI_XSLT_TRANSFORMATION_COMPILE_OR_RUNTIME_ERROR_P2_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, KB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/adding-custom-message, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-mapping-guidelines-basics
