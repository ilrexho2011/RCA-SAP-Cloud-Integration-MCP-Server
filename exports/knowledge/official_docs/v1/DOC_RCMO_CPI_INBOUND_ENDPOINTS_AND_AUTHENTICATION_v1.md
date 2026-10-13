# Inbound Endpoints and Authentication

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "INBOUND_ENDPOINTS_AND_AUTHENTICATION"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-049

DOC TITLE
Inbound Endpoints and Authentication

1. PURPOSE
- Inbound endpoint setup is where reachability, authentication, and caller trust are established for flows exposed to external systems.
- SAP Help emphasizes endpoint connection setup and also notes Cloud Foundry-specific requirements such as SNI for clients calling integration flow endpoints.

2. SCOPE
- Primary source scope: Inbound Endpoints and Authentication and closely related SAP Help pages.
- Chunking hint: define inbound endpoint; choose authentication model; prepare credentials/certificates; validate caller connectivity.
- Preferred retrieval anchors: inbound endpoints and authentication, define inbound endpoint, choose authentication model, prepare credentials/certificates, inbound.

3. KEY TERMS
- Define inbound
- endpoint
- Choose authentication
- model
- Prepare
- credentials/certificates
- Validate caller
- connectivity
- Monitor real call
- behavior Why this to…

4. CORE EXPLANATION
- SAP Help provides dedicated guidance on inbound communication and secure authentication methods. This matters operationally because endpoint problems often appear as generic receiver or connectivity errors even though the real issue is identity, trust, or environment-specific caller setup.
- Reachability and authentication must be treated together; one without the other is not a usable inbound interface.
- Environment details matter: caller expectations and platform constraints can differ between runtimes.
- Certificate-based trust introduces lifecycle questions such as expiry, host validation, and renewal.
- Inbound authentication design affects both security and the quality of support evidence available later.

5. OPERATIONAL RELEVANCE
- Testing business logic before confirming that the caller is authenticated the way the flow expects.
- Treating all auth failures as credential errors when some are certificate or environment-routing errors.
- Ignoring certificate lifecycle and only reacting at expiry time.
- Not recording which exact endpoint and authentication option the partner was told to use.
- Representative question forms:
- What is the intended use of inbound endpoints and authentication in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for inbound endpoints and authentication?
- What evidence and search anchors should be stored for inbound endpoints and authentication, define inbound endpoint, choose authentication model?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-049
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, RB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md
- Related catalog objects: IR01_IF07_Test_Email_with_OAuth2_Code
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/connection-setup-for-inbound-communication-integration-flow-endpoints, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/use-secure-authentication-methods, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/authentication-options-inbound, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/configuring-inbound-http-connections-cloud-foundry-environment
