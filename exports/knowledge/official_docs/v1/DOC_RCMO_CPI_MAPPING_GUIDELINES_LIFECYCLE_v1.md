# Mapping Guidelines (MAG) Lifecycle

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "MAPPING_GUIDELINES_LIFECYCLE"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-096

DOC TITLE
Mapping Guidelines (MAG) Lifecycle

1. PURPOSE
- This guide condenses the SAP Help pages behind Mapping Guidelines (MAG) Lifecycle into retrieval-friendly checkpoints for RAG ingestion.
- Focus on standards-based mapping design with MIGs, MAGs, codelists, simulation, and controlled change.

2. SCOPE
- Primary source scope: Mapping Guidelines (MAG) Lifecycle and closely related SAP Help pages.
- Chunking hint: model; guide; simulate; version.
- Preferred retrieval anchors: mapping guidelines (mag) lifecycle, model, guide, simulate, guidelines.

3. KEY TERMS
- Model
- Guide
- Simulate
- Version
- Reuse

4. CORE EXPLANATION
- Distinguish design-time mapping assets from runtime mapping execution so retrieval can route questions to the right layer.
- Preserve the distinction between MAG, MIG, custom mapping, and ID mapping because user questions often use these names precisely.
- This guide condenses the SAP Help pages behind Mapping Guidelines (MAG) Lifecycle into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Confusing MIG, MAG, custom mapping, and runtime mapping output.
- Ignoring versioning and simulation steps when reusing standards-based assets.
- Representative question forms:
- What is the intended use of mapping guidelines (mag) lifecycle in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for mapping guidelines (mag) lifecycle?
- What evidence and search anchors should be stored for mapping guidelines (mag) lifecycle, model, guide?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-096
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/working-with-mapping-guideline-mag, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/creating-new-mapping-guideline
