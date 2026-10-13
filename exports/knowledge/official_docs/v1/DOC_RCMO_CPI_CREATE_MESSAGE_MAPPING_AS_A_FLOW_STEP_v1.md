# Create Message Mapping as a Flow Step

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CREATE_MESSAGE_MAPPING_AS_A_FLOW_STEP"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-102

DOC TITLE
Create Message Mapping as a Flow Step

1. PURPOSE
- This guide condenses the SAP Help pages behind Create Message Mapping as a Flow Step into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: mapping, flow step, processing order.

2. SCOPE
- Primary source scope: Create Message Mapping as a Flow Step and closely related SAP Help pages.
- Chunking hint: model; transform; validate; reuse.
- Preferred retrieval anchors: create message mapping as a flow step, model, transform, validate, step.

3. KEY TERMS
- Model
- Transform
- Validate
- Reuse

4. CORE EXPLANATION
- Keep exact SAP terminology for mapping so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Create Message Mapping as a Flow Step into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating mapping as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of create message mapping as a flow step in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for create message mapping as a flow step?
- What evidence and search anchors should be stored for create message mapping as a flow step, model, transform?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-102
- Related runbooks: RB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md, RB_RCMO_CPI_XSLT_TRANSFORMATION_COMPILE_OR_RUNTIME_ERROR_P2_v1.md, RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, KB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md, KB_RCMO_CPI_XSLT_TRANSFORMATION_COMPILE_OR_RUNTIME_ERROR_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-mapping-guidelines-basics, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/getting-started-with-integration-flow-development
