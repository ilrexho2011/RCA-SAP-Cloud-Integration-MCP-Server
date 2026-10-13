# SAP Integration Advisor - Overview

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SAP_INTEGRATION_ADVISOR_OVERVIEW"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-094

DOC TITLE
SAP Integration Advisor - Overview

1. PURPOSE
- This guide condenses the SAP Help pages behind SAP Integration Advisor - Overview into retrieval-friendly checkpoints for RAG ingestion.
- Focus on standards-based mapping design with MIGs, MAGs, codelists, simulation, and controlled change.

2. SCOPE
- Primary source scope: SAP Integration Advisor - Overview and closely related SAP Help pages.
- Chunking hint: model; guide; simulate; version.
- Preferred retrieval anchors: sap integration advisor - overview, model, guide, simulate, advisor - overview.

3. KEY TERMS
- Model
- Guide
- Simulate
- Version
- Reuse

4. CORE EXPLANATION
- Distinguish design-time mapping assets from runtime mapping execution so retrieval can route questions to the right layer.
- Preserve the distinction between MAG, MIG, custom mapping, and ID mapping because user questions often use these names precisely.
- This guide condenses the SAP Help pages behind SAP Integration Advisor - Overview into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Confusing MIG, MAG, custom mapping, and runtime mapping output.
- Ignoring versioning and simulation steps when reusing standards-based assets.
- Representative question forms:
- What is the intended use of this overview in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for this overview?
- What evidence and search anchors should be stored for sap integration advisor - overview, model, guide?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-094
- Related runbooks: RB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, RB_RCMO_CPI_REST_DATA_QUALITY_OPTIONAL_FIELD_REJECTED_P3_v1.md, RB_RCMO_CPI_FILE_ENCODING_UTF8_BOM_WARNING_P3_v1.md
- Related KEDB: KB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, KB_RCMO_CPI_REST_DATA_QUALITY_OPTIONAL_FIELD_REJECTED_P3_v1.md, KB_RCMO_CPI_FILE_ENCODING_UTF8_BOM_WARNING_P3_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-integration-advisor, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/overview-of-sap-integration-advisor
