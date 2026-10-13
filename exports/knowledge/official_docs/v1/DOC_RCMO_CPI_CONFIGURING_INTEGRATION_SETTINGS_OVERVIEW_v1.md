# Configuring Integration Settings - Overview

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CONFIGURING_INTEGRATION_SETTINGS_OVERVIEW"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-077

DOC TITLE
Configuring Integration Settings - Overview

1. PURPOSE
- This guide condenses the SAP Help pages behind Configuring Integration Settings - Overview into retrieval-friendly checkpoints for RAG ingestion.
- Focus on tenant-level configuration concerns such as roles, access boundaries, endpoints, landscapes, and environment differences.

2. SCOPE
- Primary source scope: Configuring Integration Settings - Overview and closely related SAP Help pages.
- Chunking hint: admin; protect; authorize; connect.
- Preferred retrieval anchors: configuring integration settings - overview, admin, protect, authorize, configuring settings - overview.

3. KEY TERMS
- Admin
- Protect
- Authorize
- Connect
- Control

4. CORE EXPLANATION
- Separate tenant-scoped configuration from flow-scoped configuration so troubleshooting does not mix runtime symptoms with administrative causes.
- Index certificate, keystore, OAuth, IdP, and role terms explicitly to improve retrieval for auth and trust failures.
- This guide condenses the SAP Help pages behind Configuring Integration Settings - Overview into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Treating tenant-wide settings as if they were isolated to one integration flow.
- Changing trust material or roles without mapping the downstream runtime impact.
- Representative question forms:
- What is the intended use of this overview in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for this overview?
- What evidence and search anchors should be stored for configuring integration settings - overview, admin, protect?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-077
- Related runbooks: RB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, RB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, RB_RCMO_CPI_ODATA_SERVICE_NOT_FOUND_404_P2_v1.md, RB_RCMO_CPI_DATASTORE_WRITE_KEY_CONFLICT_P2_v1.md
- Related KEDB: KB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, KB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, KB_RCMO_CPI_ODATA_SERVICE_NOT_FOUND_404_P2_v1.md, KB_RCMO_CPI_DATASTORE_WRITE_KEY_CONFLICT_P2_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP, IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/configuring-integration-settings, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/access-policies, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/security-content
