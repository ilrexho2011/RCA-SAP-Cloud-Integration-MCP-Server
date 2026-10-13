# Tasks, Permissions, and Personas

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "TASKS_PERMISSIONS_AND_PERSONAS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-079

DOC TITLE
Tasks, Permissions, and Personas

1. PURPOSE
- This guide condenses the SAP Help pages behind Tasks, Permissions, and Personas into retrieval-friendly checkpoints for RAG ingestion.
- Focus on tenant-level configuration concerns such as roles, access boundaries, endpoints, landscapes, and environment differences.

2. SCOPE
- Primary source scope: Tasks, Permissions, and Personas and closely related SAP Help pages.
- Chunking hint: admin; protect; authorize; connect.
- Preferred retrieval anchors: tasks, permissions, and personas, admin, protect, authorize, tasks.

3. KEY TERMS
- Admin
- Protect
- Authorize
- Connect
- Control

4. CORE EXPLANATION
- Separate tenant-scoped configuration from flow-scoped configuration so troubleshooting does not mix runtime symptoms with administrative causes.
- This guide condenses the SAP Help pages behind Tasks, Permissions, and Personas into retrieval-friendly checkpoints for RAG ingestion.
- Focus on tenant-level configuration concerns such as roles, access boundaries, endpoints, landscapes, and environment differences.

5. OPERATIONAL RELEVANCE
- Treating tenant-wide settings as if they were isolated to one integration flow.
- Changing trust material or roles without mapping the downstream runtime impact.
- Representative question forms:
- What is the intended use of tasks, permissions, and personas in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for tasks, permissions, and personas?
- What evidence and search anchors should be stored for tasks, permissions, and personas, admin, protect?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-079
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_WORKFLOW_TIMER_REMINDER_RULE_MISFIRED_P3_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_WORKFLOW_TIMER_REMINDER_RULE_MISFIRED_P3_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/tasks-and-permissions-neo, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/persona
