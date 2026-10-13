# SAP CPI SFTP Adapter - Remote file or directory not found
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SFTP_FILE_NOT_FOUND"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0087
KEDB TITLE
SAP CPI SFTP Adapter - Remote file or directory not found
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* SFTP operation fails because the configured remote path or dynamic filename does not exist.
* Canonical retrieval phrase: SAP CPI SFTP Adapter - Remote file or directory not found.
* Normalized object_name: CPI_SFTP_FILE_NOT_FOUND.
2. ERROR PATTERN
* SFTP | FILESYSTEM | FILE_NOT_FOUND | REMOTE_PATH
3. ROOT CAUSE
* SFTP adapter points to the wrong directory.
* Dynamic filename header is not resolved.
* Target file or directory was removed before CPI access.
4. DIAGNOSIS SIGNALS
* Check MPL for remote path, filename, user, host, and MessageGuid.
* Verify dynamic filename headers before the SFTP adapter step.
* Confirm remote directory existence and permissions on the SFTP server.
* Preserve runtime evidence: Evidence: 2026-04-06T22:30:49.957 | MessageGuid AGnUNBnbavGGocjWdJVbvCyhuISG | Interface IR_IF034_SFTP_Passthrough_Sample_Source_to_Target | Sender n/a | Receiver n/a | Error: An internal server error occured: Cannot connect to sap-sftp://sapci@my-sftp-virtual-host:2288
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SFTP_FILE_NOT_FOUND and SFTP | FILESYSTEM | FILE_NOT_FOUND | REMOTE_PATH during search and triage.
5. RESOLUTION
* Correct the SFTP remote path and dynamic filename expression.
* Create the missing target directory with approved permissions.
* Replay one controlled file after path validation succeeds.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SFTP_FILE_NOT_FOUND and SFTP | FILESYSTEM | FILE_NOT_FOUND | REMOTE_PATH do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Place the missing file manually only when source-system ownership confirms the expected content.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SFTP_FILE_NOT_FOUND_P2_v1.md
* Cross-reference object_name: CPI_SFTP_FILE_NOT_FOUND
* Cross-reference taxonomy: SFTP | FILESYSTEM | FILE_NOT_FOUND | REMOTE_PATH
* Source KEDB ID: KEDB-P2-0087
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
