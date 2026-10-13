# Router and Content-Based Routing

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "ROUTER_AND_CONTENT_BASED_ROUTING"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-040

DOC TITLE
Router and Content-Based Routing

1. PURPOSE
- Routing is where a message is classified and sent to the correct branch or receiver path.
- Most router incidents are not “hard failures” first; they begin as wrong branch selection, no-match conditions, or fallback behavior.

2. SCOPE
- Primary source scope: Router and Content-Based Routing and closely related SAP Help pages.
- Chunking hint: evaluate routing inputs; apply condition logic; select explicit branch or fallback; confirm downstream receiver/step path why this topic matters in daily work.
- Preferred retrieval anchors: router and content-based routing, evaluate routing inputs, apply condition logic, select explicit branch or fallback.

3. KEY TERMS
- Evaluate routing inputs
- Apply condition logic
- Select explicit branch
- or fallback
- Confirm downstream
- receiver/step path W…

4. CORE EXPLANATION
- downstream receiver/step path SAP Help explicitly connects the Router to content-based and dynamic routing choices. In support terms, that means the Router is a decision gate: when it fails or classifies incorrectly, all downstream evidence can be misleading because the wrong path was taken even though later steps are technically “working”.
- Condition quality: the route is only as good as the data elements, headers, or properties it evaluates.
- No-match behavior matters: absence of a match is often its own defect category and should be logged clearly.
- Fallback usage is evidence: a default branch can indicate expected resilience or hidden classification failure.
- Dynamic routing increases flexibility but also widens the surface for configuration drift.

5. OPERATIONAL RELEVANCE
- Debugging the receiver before confirming the selected route.
- Using overly fragile conditions tied to optional or poorly normalized fields.
- Treating fallback branch execution as success without validating business intent.
- Not exposing route decision inputs in logs or support evidence.
- Representative question forms:
- What is the intended use of router and content-based routing in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for router and content-based routing?
- What evidence and search anchors should be stored for router and content-based routing, evaluate routing inputs, apply condition logic?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-040
- Related runbooks: RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, RB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md
- Related KEDB: KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md, KB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/integration-suite/sap-integration-suite/define-router, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/content-based-routing, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/variant-dynamic-routing
