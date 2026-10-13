# Cloud Integration Best Practices

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CLOUD_INTEGRATION_BEST_PRACTICES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-032

DOC TITLE
Cloud Integration Best Practices

1. PURPOSE
- Best practices in Cloud Integration are about building *change-safe* and *supportable* integrations, not only about making flows work once.
- Design with operations in mind: observability, consistent error handling, and traceability from build to runtime.

2. SCOPE
- Primary source scope: Best Practices and closely related SAP Help pages.
- Chunking hint: best practices.
- Preferred retrieval anchors: best practices.

3. KEY TERMS
- Best Practices

4. CORE EXPLANATION
- Best practices in Cloud Integration are about building *change-safe* and *supportable* integrations, not only about making flows work once.
- Design with operations in mind: observability, consistent error handling, and traceability from build to runtime.
- Prefer evidence-based troubleshooting: update runbooks and KEDB when you learn what signals actually reduce triage time.

5. OPERATIONAL RELEVANCE
- Treating best practices as isolated from the end-to-end flow lifecycle.
- Capturing configuration steps without preserving constraints, prerequisites, and runtime evidence.
- Representative question forms:
- What is the intended use of best practices in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for best practices?
- What evidence and search anchors should be stored for best practices?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-032
- Related runbooks: RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR01_IF06_Test_SMS_Message, IR01_IF07_Test_Email_with_OAuth2_Code, IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
