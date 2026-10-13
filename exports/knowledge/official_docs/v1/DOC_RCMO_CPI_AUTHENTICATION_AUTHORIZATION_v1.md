# Authentication and Authorization

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "AUTHENTICATION_AUTHORIZATION"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-027

DOC TITLE
Authentication and Authorization

1. PURPOSE
- Authentication answers: who are you? Authorization answers: what are you allowed to do?
- In Cloud Integration, these concerns appear at multiple layers: adapter-side access to targets, internal service access, and secure material handling.

2. SCOPE
- Primary source scope: Authentication and Authorization and closely related SAP Help pages.
- Chunking hint: identity/credentials; secure transport; authorization checks; adapter execution.
- Preferred retrieval anchors: authentication and authorization, identity/credentials, secure transport, authorization checks.

3. KEY TERMS
- Identity/credentials
- secure transport
- authorization checks
- adapter execution
- monitoring signals
- evidence & remediation

4. CORE EXPLANATION
- A recurring delivery issue is mixing authentication failures with authorization failures or mixing both with payload/schema failures. Clear separation improves diagnosis speed and prevents chasing the wrong fix.
- Authentication: credentials, client identity, certificates/keys, host trust/verification, and secure channel establishment.
- Authorization: permissions/roles on the target side, allowed operations, and access scope for the requested action.
- Security materials: how keys/certificates/secrets are stored, referenced, and kept consistent with runtime environment expectations.
- Step 1: identify where auth should apply (sender vs receiver; adapter vs target system).

5. OPERATIONAL RELEVANCE
- Assuming an auth error is a payload mapping issue because the message fails after some processing.
- Updating runbooks without adding evidence steps for auth categories, causing repeat triage loops.
- Not distinguishing host trust failures from credential failures.
- Not confirming authorization on the target side (roles/permissions), leading to repeated reattempts.
- Representative question forms:
- What is the intended use of authentication and authorization in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for authentication and authorization?
- What evidence and search anchors should be stored for authentication and authorization, identity/credentials, secure transport?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-027
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md, RB_RCMO_CPI_CLOUD_AUTH_SESSION_EXPIRED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md, KB_RCMO_CPI_CLOUD_AUTH_SESSION_EXPIRED_P2_v1.md
- Related catalog objects: IR01_IF06_Test_SMS_Message, IR01_IF07_Test_Email_with_OAuth2_Code, IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1, IR27_IF03_Dynamic_Process_Football_OData_Scores
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
