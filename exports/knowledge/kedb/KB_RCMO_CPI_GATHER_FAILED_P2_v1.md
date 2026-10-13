# SAP CPI Gather - Aggregation failed after split branches
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_GATHER_FAILED"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0070
KEDB TITLE
SAP CPI Gather - Aggregation failed after split branches
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Gather aggregation fails because split branches cannot be correlated or return incompatible message structures.
* Canonical retrieval phrase: SAP CPI Gather - Aggregation failed after split branches.
* Normalized object_name: CPI_GATHER_FAILED.
2. ERROR PATTERN
* GATHER | AGGREGATION | FAILED | CORRELATION_ERROR
3. ROOT CAUSE
* Correlation ID is missing in one or more branches.
* A branch fails before the Gather step.
* Branch output structure differs from the expected aggregation format.
4. DIAGNOSIS SIGNALS
* Check each split branch in MPL and confirm branch completion before Gather.
* Verify that the correlation ID is preserved across all branches.
* Compare branch output body and headers before aggregation.
* Preserve runtime evidence: MPL API | Exception Subprocess | Security Material Check | Evidence: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD_oyD8gRzoUxifc | Interface IR01_IF09_Access_Message_Processing_ErrorLogs_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_GATHER_FAILED and GATHER | AGGREGATION | FAILED | CORRELATION_ERROR during search and triage.
5. RESOLUTION
* Preserve correlation IDs across all split branches.
* Normalize branch output structures before Gather.
* Handle failed branches before aggregation and replay one controlled message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_GATHER_FAILED and GATHER | AGGREGATION | FAILED | CORRELATION_ERROR do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Process the affected records through a sequential recovery path until branch consistency is restored.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_GATHER_FAILED_P2_v1.md
* Cross-reference object_name: CPI_GATHER_FAILED
* Cross-reference taxonomy: GATHER | AGGREGATION | FAILED | CORRELATION_ERROR
* Source KEDB ID: KEDB-P2-0070
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
