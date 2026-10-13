# Cloud Integration - Core Concepts

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CORE_CONCEPTS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-002

DOC TITLE
Cloud Integration - Core Concepts

1. PURPOSE
- A tenant hosts your integration capability and runtime context.
- Packages organize artifacts; integration flows are the main executable design objects.

2. SCOPE
- Primary source scope: Core Concepts and closely related SAP Help pages.
- Chunking hint: tenant; package; iflow; adapters.
- Preferred retrieval anchors: core concepts, tenant, package, iflow.

3. KEY TERMS
- Tenant
- Package
- iFlow
- Adapters
- Runtime

4. CORE EXPLANATION
- Tenant: the environment where the capability runs and is administered.
- Package: a logical container used to group related integration artifacts.
- Artifact: a design-time object such as an integration flow or related configuration asset.
- Integration flow: the main executable process that orchestrates sender, processing logic, and receiver handling.
- Sender adapter: defines how a message is accepted into the flow.

5. OPERATIONAL RELEVANCE
- Using package and flow as if they mean the same thing.
- Hard-coding environment-specific values instead of externalizing them.
- Ignoring security material until the end.
- Representative question forms:
- What is the intended use of core concepts in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for core concepts?
- What evidence and search anchors should be stored for core concepts, tenant, package?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-002
- Related runbooks: RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, RB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P2_v1.md, RB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P3_v1.md
- Related KEDB: KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, KB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P2_v1.md, KB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P3_v1.md
- Related catalog objects: IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration, https://help.sap.com/docs/integration-suite/sap-integration-suite/capabilities, https://help.sap.com/doc/978cdb2059244c10b55a8bd916484a63/CLOUD/en-US/b97b0ec26c871014bc6ce3c22a1e81b1.html, https://help.sap.com/docs/integration-suite/sap-integration-suite/what-is-sap-integration-suite
