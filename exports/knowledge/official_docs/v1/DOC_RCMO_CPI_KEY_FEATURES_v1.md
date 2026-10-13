# Key Features

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "KEY_FEATURES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-009

DOC TITLE
Key Features

1. PURPOSE
- Cloud Integration is typically valued for combining connectivity, message processing, transformation, security, deployment, and monitoring in one managed integration capability.
- The most practical feature lens is not a long catalog, but a working chain: connect systems, model the flow, secure it, run it, and monitor it.

2. SCOPE
- Primary source scope: Key Features and closely related SAP Help pages.
- Chunking hint: connectivity; flow design; transformation; security.
- Preferred retrieval anchors: key features, connectivity, flow design, transformation, key.

3. KEY TERMS
- Connectivity
- Flow design
- Transformation
- Security
- Deployment
- Monitoring

4. CORE EXPLANATION
- Connectivity and adapters: Cloud Integration is commonly used to connect heterogeneous systems through protocol- and application-oriented endpoints. In practical terms, this is where sender and receiver communication begins.
- Integration flow modeling: The integration flow is the central artifact for implementing routes, processing steps, mappings, and exception handling.
- Message transformation: Teams rely on transformation features to reshape payloads, normalize formats, and prepare data for target-side contracts.
- Security handling: Authentication, authorization, credential usage, and secure transport are treated as first-class concerns rather than afterthoughts.
- Deployment and lifecycle management: Design artifacts are packaged, versioned, configured, and promoted toward runtime execution.

5. OPERATIONAL RELEVANCE
- Treating “features” as marketing language instead of operational capabilities that affect implementation design.
- Over-focusing on connectivity while underestimating transformation, security, and monitoring requirements.
- Assuming that design-time convenience automatically guarantees runtime observability and support readiness.
- Using this overview as a substitute for the feature-specific SAP Help sections that explain exact tenant behavior and release details.
- Representative question forms:
- What is the intended use of key features in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for key features?
- What evidence and search anchors should be stored for key features, connectivity, flow design?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-009
- Related runbooks: RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, RB_RCMO_CPI_RUNTIME_DEPLOYMENT_VERSION_MISMATCH_P2_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P3_v1.md
- Related KEDB: KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P2_v1.md, KB_RCMO_CPI_RUNTIME_DEPLOYMENT_VERSION_MISMATCH_P2_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR01_IF06_Test_SMS_Message, IR16_IF00_Global_Variables, IR16_IF01_Northwind_Orders_via_OrderID_in_Payload_using_Variable
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
