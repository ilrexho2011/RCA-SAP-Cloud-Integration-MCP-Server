# Qualifying Nodes and ID Mapping

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "QUALIFYING_NODES_AND_ID_MAPPING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-098

DOC TITLE
Qualifying Nodes and ID Mapping

1. PURPOSE
- This guide condenses the SAP Help pages behind Qualifying Nodes and ID Mapping into retrieval-friendly checkpoints for RAG ingestion.
- Focus on standards-based mapping design with MIGs, MAGs, codelists, simulation, and controlled change.

2. SCOPE
- Primary source scope: Qualifying Nodes and ID Mapping and closely related SAP Help pages.
- Chunking hint: model; guide; simulate; version.
- Preferred retrieval anchors: qualifying nodes and id mapping, model, guide, simulate, qualifying.

3. KEY TERMS
- Model
- Guide
- Simulate
- Version
- Reuse

4. CORE EXPLANATION
- Distinguish design-time mapping assets from runtime mapping execution so retrieval can route questions to the right layer.
- Preserve the distinction between MAG, MIG, custom mapping, and ID mapping because user questions often use these names precisely.
- This guide condenses the SAP Help pages behind Qualifying Nodes and ID Mapping into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Confusing MIG, MAG, custom mapping, and runtime mapping output.
- Ignoring versioning and simulation steps when reusing standards-based assets.
- Representative question forms:
- What is the intended use of qualifying nodes and id mapping in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for qualifying nodes and id mapping?
- What evidence and search anchors should be stored for qualifying nodes and id mapping, model, guide?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-098
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related KEDB: KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, KB_RCMO_CPI_B2B_EDI_PARSE_FAILURE_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/qualifying-nodes, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/define-id-mapping, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/id-mapping-with-splitter, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/id-mapping-with-multicast
