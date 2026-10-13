# ID Mapping with Splitter

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "ID_MAPPING_WITH_SPLITTER"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-118

DOC TITLE
ID Mapping with Splitter

1. PURPOSE
- This guide condenses the SAP Help pages behind ID Mapping with Splitter into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: id mapping, splitter.

2. SCOPE
- Primary source scope: ID Mapping with Splitter and closely related SAP Help pages.
- Chunking hint: model; transform; validate; reuse.
- Preferred retrieval anchors: id mapping with splitter, model, transform, validate.

3. KEY TERMS
- Model
- Transform
- Validate
- Reuse

4. CORE EXPLANATION
- Keep exact SAP terminology for id mapping so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind ID Mapping with Splitter into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating id mapping as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of id mapping with splitter in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for id mapping with splitter?
- What evidence and search anchors should be stored for id mapping with splitter, model, transform?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-118
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_B2B_AS2_MDN_VALIDATION_FAILED_P1_v1.md, RB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_B2B_AS2_MDN_VALIDATION_FAILED_P1_v1.md, KB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/id-mapping-with-splitter
