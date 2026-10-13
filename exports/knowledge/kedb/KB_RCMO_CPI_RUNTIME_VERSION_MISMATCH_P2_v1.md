# SAP CPI Runtime - Deployed artifact version mismatch
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_RUNTIME_VERSION_MISMATCH"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0084
KEDB TITLE
SAP CPI Runtime - Deployed artifact version mismatch
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Runtime behavior differs from design expectation because an old or incomplete artifact version is active.
* Canonical retrieval phrase: SAP CPI Runtime - Deployed artifact version mismatch.
* Normalized object_name: CPI_RUNTIME_VERSION_MISMATCH.
2. ERROR PATTERN
* RUNTIME | DEPLOYMENT | VERSION_MISMATCH | OLD_ARTIFACT
3. ROOT CAUSE
* Old artifact version remains deployed.
* Transport or deployment pipeline did not complete.
* Multiple package versions create ambiguity for operators.
4. DIAGNOSIS SIGNALS
* Check deployed artifact version in CPI Monitor and Design view.
* Compare runtime timestamp with the expected transport or deployment record.
* Verify that the intended package version is active.
* Preserve runtime evidence: Correlate MPL evidence: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD_oyD8gRzoUxifc | Interface IR01_IF09_Access_Message_Processing_ErrorLogs_2 | Sender n/a | Receiver n/a.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_RUNTIME_VERSION_MISMATCH and RUNTIME | DEPLOYMENT | VERSION_MISMATCH | OLD_ARTIFACT during search and triage.
5. RESOLUTION
* Redeploy the target artifact version from the approved package.
* Clean failed or incomplete transport pipeline state.
* Run one controlled test message after deployment completes.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_RUNTIME_VERSION_MISMATCH and RUNTIME | DEPLOYMENT | VERSION_MISMATCH | OLD_ARTIFACT do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Rollback to the last known stable artifact version if the new deployment fails validation.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_RUNTIME_VERSION_MISMATCH_P2_v1.md
* Cross-reference object_name: CPI_RUNTIME_VERSION_MISMATCH
* Cross-reference taxonomy: RUNTIME | DEPLOYMENT | VERSION_MISMATCH | OLD_ARTIFACT
* Source KEDB ID: KEDB-P2-0084
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
