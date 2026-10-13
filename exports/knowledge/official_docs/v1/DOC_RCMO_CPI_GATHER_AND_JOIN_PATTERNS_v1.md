# Gather and Join Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "GATHER_AND_JOIN_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-042

DOC TITLE
Gather and Join Patterns

1. PURPOSE
- Join and Gather are the return path after a message was branched or split and needs controlled recombination.
- Join brings messages together structurally; Gather adds merge strategy and content combination semantics.

2. SCOPE
- Primary source scope: Gather and Join Patterns and closely related SAP Help pages.
- Chunking hint: branch or split; process parts independently; correlate matching parts; join or gather.
- Preferred retrieval anchors: gather and join patterns, branch or split, process parts independently, correlate matching parts, patterns.

3. KEY TERMS
- Branch or split
- Process parts
- independently
- Correlate matching
- parts
- Join or gather

4. CORE EXPLANATION
- SAP Help highlights that Join is used together with Gather and that Gather can apply strategies when combining messages. For RAG and support, this matters because recombination failures often look like missing data, duplicate data, or malformed output even though each branch executed successfully on its own.
- Correlation is the backbone: if context is incomplete, merge logic becomes unreliable.
- Structural reunion and content merging are not the same operation.
- Branch consistency matters: all participating routes need compatible assumptions for successful recombination.
- Observability should record both branch success and convergence success separately.

5. OPERATIONAL RELEVANCE
- Assuming that successful branch execution guarantees successful recombination.
- Not preserving enough correlation context across branches.
- Using Gather semantics when only structural reunion was intended, or vice versa.
- Inspecting only the final payload and not the branch-by-branch evidence chain.
- Representative question forms:
- What is the intended use of gather and join patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for gather and join patterns?
- What evidence and search anchors should be stored for gather and join patterns, branch or split, process parts independently?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-042
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, RB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md
- Related KEDB: KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, KB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/define-gather-and-join
