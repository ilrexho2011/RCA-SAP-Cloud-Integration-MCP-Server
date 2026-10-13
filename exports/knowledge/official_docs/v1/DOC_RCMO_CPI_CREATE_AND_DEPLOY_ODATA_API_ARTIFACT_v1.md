# Create and Deploy an OData API Artifact

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CREATE_AND_DEPLOY_ODATA_API_ARTIFACT"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-061

DOC TITLE
Create and Deploy an OData API Artifact

1. PURPOSE
- This guide condenses the SAP Help pages behind Create and Deploy an OData API Artifact into retrieval-friendly checkpoints for RAG ingestion.
- Focus on API exposure and OData-specific behavior: modeling, deployment, invocation, client setup, and query behavior.

2. SCOPE
- Primary source scope: Create and Deploy an OData API Artifact and closely related SAP Help pages.
- Chunking hint: model; secure; deploy; invoke.
- Preferred retrieval anchors: create and deploy an odata api artifact, model, secure, deploy, odata.

3. KEY TERMS
- Model
- Secure
- Deploy
- Invoke
- Govern

4. CORE EXPLANATION
- Anchor retrieval on the concrete artifact type and on the lifecycle verb: create, configure, deploy, invoke, import, or transport.
- Prefer keywords such as service root, query options, batch requests, active status, and inbound API client when chunking this source.
- This guide condenses the SAP Help pages behind Create and Deploy an OData API Artifact into retrieval-friendly checkpoints for RAG ingestion.

5. OPERATIONAL RELEVANCE
- Mixing API client setup with business-flow adapter setup.
- Diagnosing OData problems without separating authentication, query semantics, and payload contract issues.
- Representative question forms:
- What is the intended use of create and deploy an odata api artifact in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for create and deploy an odata api artifact?
- What evidence and search anchors should be stored for create and deploy an odata api artifact, model, secure?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-061
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md
- Related catalog objects: IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/create-and-deploy-odata-api-artifact, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/developing-odata-api-project
