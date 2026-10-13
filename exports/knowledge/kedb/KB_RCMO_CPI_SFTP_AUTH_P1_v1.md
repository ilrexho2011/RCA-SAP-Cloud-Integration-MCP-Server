# SAP CPI SFTP Adapter - Authentication failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SFTP_AUTH"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0086
KEDB TITLE
SAP CPI SFTP Adapter - Authentication failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* SFTP login fails because SSH key, user, password, known host, or account status is invalid.
* Canonical retrieval phrase: SAP CPI SFTP Adapter - Authentication failed.
* Normalized object_name: CPI_SFTP_AUTH.
2. ERROR PATTERN
* SFTP | AUTHENTICATION | LOGIN_FAILURE | CONNECTION_DENIED
3. ROOT CAUSE
* SSH key pair or credential alias is wrong or expired.
* SFTP user is disabled or mapped to the wrong home folder.
* Known host entry or algorithm policy rejects the connection.
4. DIAGNOSIS SIGNALS
* Check MPL for SFTP authentication error, user, host, and MessageGuid.
* Verify credential alias, SSH key pair, known host, and username.
* Confirm account status and home folder mapping with SFTP administrator.
* Preserve runtime evidence: Evidence: 2026-04-06T22:30:49.957 | MessageGuid AGnUNBnbavGGocjWdJVbvCyhuISG | Interface IR_IF034_SFTP_Passthrough_Sample_Source_to_Target | Sender n/a | Receiver n/a | Error: An internal server error occured: Cannot connect to sap-sftp://sapci@my-sftp-virtual-host:2288
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SFTP_AUTH and SFTP | AUTHENTICATION | LOGIN_FAILURE | CONNECTION_DENIED during search and triage.
5. RESOLUTION
* Upload the correct SSH key pair and credential alias.
* Correct username, known host, and home folder mapping.
* Test the SFTP adapter connection and replay one controlled file.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SFTP_AUTH and SFTP | AUTHENTICATION | LOGIN_FAILURE | CONNECTION_DENIED do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Use the approved backup SFTP account only if access and audit rules allow it.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SFTP_AUTH_P1_v1.md
* Cross-reference object_name: CPI_SFTP_AUTH
* Cross-reference taxonomy: SFTP | AUTHENTICATION | LOGIN_FAILURE | CONNECTION_DENIED
* Source KEDB ID: KEDB-P1-0086
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
