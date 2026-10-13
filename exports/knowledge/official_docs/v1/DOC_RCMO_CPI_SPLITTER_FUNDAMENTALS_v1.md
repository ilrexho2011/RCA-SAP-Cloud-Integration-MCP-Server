# Splitter Fundamentals

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SPLITTER_FUNDAMENTALS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-136

DOC TITLE
Splitter Fundamentals

1. PURPOSE
- This guide condenses the SAP Help pages behind Splitter Fundamentals into retrieval-friendly checkpoints for RAG ingestion.
- Focus on the design choices that most affect implementation, searchability, and runtime diagnosis: splitter, split.

2. SCOPE
- Primary source scope: Splitter Fundamentals and closely related SAP Help pages.
- Chunking hint: route; branch; handle; observe.
- Preferred retrieval anchors: splitter fundamentals, route, branch, handle.

3. KEY TERMS
- Route
- Branch
- Handle
- Observe

4. CORE EXPLANATION
- Keep exact SAP terminology for splitter so retrieval can answer concept-first and action-first questions.
- Preserve restrictions, prerequisites, and runtime side effects with the same chunk family.
- This guide condenses the SAP Help pages behind Splitter Fundamentals into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating splitter as an isolated feature instead of part of the end-to-end flow design.
- Capturing only configuration steps while omitting constraints, edge cases, or monitoring evidence.
- Representative question forms:
- What is the intended use of splitter fundamentals in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for splitter fundamentals?
- What evidence and search anchors should be stored for splitter fundamentals, route, branch?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-136
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-integration-content-with-sap-cloud-integration
