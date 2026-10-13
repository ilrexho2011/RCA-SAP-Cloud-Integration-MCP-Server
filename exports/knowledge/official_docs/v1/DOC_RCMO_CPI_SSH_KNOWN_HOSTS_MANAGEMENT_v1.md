# SSH and Known Hosts Management

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SSH_KNOWN_HOSTS_MANAGEMENT"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-029

DOC TITLE
SSH and Known Hosts Management

1. PURPOSE
- SSH and known hosts management enable secure, verified connectivity for SSH-based transports (commonly used alongside file transfer scenarios).
- The critical concept is host identity verification: the client must trust the server host key (known hosts) and verify it correctly at runtime.

2. SCOPE
- Primary source scope: SSH and Known Hosts Management and closely related SAP Help pages.
- Chunking hint: host identity (host key); known hosts trust entries; secure ssh channel; adapter/transport connectivity.
- Preferred retrieval anchors: ssh and known hosts management, host identity (host key), known hosts trust entries, secure ssh channel, ssh.

3. KEY TERMS
- Host identity (host key)
- Known hosts trust
- entries
- Secure SSH channel
- Adapter/transport
- connectivity
- Evidence
- Remediation

4. CORE EXPLANATION
- Known-hosts management is about ensuring the runtime only connects to the expected server identity. In practice, teams must align: the SSH host identity they expect, the trust entries they provide, and the runtime security material references that connect them.
- Host key identity: the expected server host key fingerprint/identity.
- Known hosts trust: the trust entries that allow verification.
- Key mismatch handling: how runtime reacts when host identity differs.
- Operational evidence: what monitoring/tracing usually indicates verification failure.

5. OPERATIONAL RELEVANCE
- Assuming that “credentials are correct” implies host verification is correct.
- Copying known hosts entries without validating the server identity and fingerprint.
- Not re-validating after server-side host key rotation.
- Leaving runbooks without explicit “verify host key identity” evidence steps.
- Representative question forms:
- What is the intended use of ssh and known hosts management in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for ssh and known hosts management?
- What evidence and search anchors should be stored for ssh and known hosts management, host identity (host key), known hosts trust entries?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-029
- Related runbooks: RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P2_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_SFTP_AUTH_LOGIN_FAILED_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P2_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP, IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
