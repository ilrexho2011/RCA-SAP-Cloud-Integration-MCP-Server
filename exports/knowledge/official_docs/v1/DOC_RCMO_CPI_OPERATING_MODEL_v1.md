# Operating Model

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "OPERATING_MODEL"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-014

DOC TITLE
Operating Model

1. PURPOSE
- An operating model describes how teams design, deploy, run, and support Cloud Integration in a repeatable way.
- It turns “how we build integration flows” into “how we deliver outcomes”: roles, responsibilities, lifecycle gates, and escalation paths.

2. SCOPE
- Primary source scope: Operating Model and closely related SAP Help pages.
- Chunking hint: roles and responsibilities; change management; quality gates; runtime operations.
- Preferred retrieval anchors: operating model, roles and responsibilities, change management, quality gates, operating.

3. KEY TERMS
- Roles and
- responsibilities
- Change management
- Quality gates
- Runtime operations

4. CORE EXPLANATION
- In delivery and support contexts, integration success depends on how work moves through phases: design/build, package/release, deploy/runtime execution, and continuous operations. The operating model defines governance for each phase, including who can do what, what gets checked, and how issues are escalated.
- People (roles): who designs, who approves, who deploys, who monitors, and who owns incident resolution.
- Process (workflow): how changes move from development to production, including review and promotion rules.
- Quality gates: what must be validated before rollout (tests, tracing checks, configuration sanity checks).
- Operations: how teams handle message processing visibility, troubleshooting routines, and support readiness.

5. OPERATIONAL RELEVANCE
- Documenting roles without defining responsibilities for change and incidents.
- Skipping explicit quality gates and assuming testing is “covered by default”.
- Treating monitoring as an afterthought instead of part of the operating workflow.
- Letting escalation paths be unclear, causing ownership delays during incidents. How to use this in the corpus
- Representative question forms:
- What is the intended use of operating model in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for operating model?
- What evidence and search anchors should be stored for operating model, roles and responsibilities, change management?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-014
- Related runbooks: RB_RCMO_CPI_RUNTIME_DEPLOYMENT_VERSION_MISMATCH_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md, RB_RCMO_CPI_WORKFLOW_TIMER_REMINDER_RULE_MISFIRED_P3_v1.md, RB_RCMO_CPI_ODATA_QUERY_PAGINATION_MISALIGNED_P3_v1.md
- Related KEDB: KB_RCMO_CPI_RUNTIME_DEPLOYMENT_VERSION_MISMATCH_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_DEFAULT_BRANCH_USED_P3_v1.md, KB_RCMO_CPI_WORKFLOW_TIMER_REMINDER_RULE_MISFIRED_P3_v1.md, KB_RCMO_CPI_ODATA_QUERY_PAGINATION_MISALIGNED_P3_v1.md
- Related catalog objects: IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
