# Create an Integration Flow

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CREATE_INTEGRATION_FLOW"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-006

DOC TITLE
Create an Integration Flow

1. PURPOSE
- Start from the integration scenario, not from the protocol screen.
- An iFlow usually combines sender, processing logic, receiver, and externalized configuration.

2. SCOPE
- Primary source scope: Create an Integration Flow and closely related SAP Help pages.
- Chunking hint: scenario; package; iflow; configure.
- Preferred retrieval anchors: create an integration flow, scenario, package, iflow, create an flow.

3. KEY TERMS
- Scenario
- Package
- iFlow
- Configure
- Deploy

4. CORE EXPLANATION
- Define the business trigger, source, target, and payload expectations.
- Create or choose the correct package.
- Create the integration flow and name it clearly.
- Configure sender and receiver adapters.
- Add required processing steps such as routing, mapping, or content modification.

5. OPERATIONAL RELEVANCE
- Starting with detailed adapter fields before clarifying the scenario.
- Leaving names too generic to be supportable later.
- Deploying without checking parameterization and operational visibility.
- Representative question forms:
- What is the intended use of create an integration flow in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for create an integration flow?
- What evidence and search anchors should be stored for create an integration flow, scenario, package?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-006
- Related runbooks: RB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration, https://help.sap.com/docs/integration-suite/sap-integration-suite/capabilities, https://help.sap.com/doc/978cdb2059244c10b55a8bd916484a63/CLOUD/en-US/b97b0ec26c871014bc6ce3c22a1e81b1.html, https://help.sap.com/docs/integration-suite/sap-integration-suite/what-is-sap-integration-suite
