# Graphical MAG and Custom Mapping

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "GRAPHICAL_MAG_AND_CUSTOM_MAPPING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-099

DOC TITLE
Graphical MAG and Custom Mapping

1. PURPOSE
- This guide condenses the SAP Help pages behind Graphical MAG and Custom Mapping into retrieval-friendly checkpoints for RAG ingestion.
- Focus on standards-based mapping design with MIGs, MAGs, codelists, simulation, and controlled change.

2. SCOPE
- Primary source scope: Graphical MAG and Custom Mapping and closely related SAP Help pages.
- Chunking hint: model; guide; simulate; version.
- Preferred retrieval anchors: graphical mag and custom mapping, model, guide, simulate, graphical.

3. KEY TERMS
- Model
- Guide
- Simulate
- Version
- Reuse

4. CORE EXPLANATION
- Distinguish design-time mapping assets from runtime mapping execution so retrieval can route questions to the right layer.
- Preserve the distinction between MAG, MIG, custom mapping, and ID mapping because user questions often use these names precisely.
- This guide condenses the SAP Help pages behind Graphical MAG and Custom Mapping into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Confusing MIG, MAG, custom mapping, and runtime mapping output.
- Ignoring versioning and simulation steps when reusing standards-based assets.
- Representative question forms:
- What is the intended use of graphical mag and custom mapping in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for graphical mag and custom mapping?
- What evidence and search anchors should be stored for graphical mag and custom mapping, model, guide?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-099
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/creating-new-mapping-guideline, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/creating-custom-mapping, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/variant-with-message-mapping?locale=en-US
