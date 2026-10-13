# SAP CPI Groovy Script - NullPointerException during processing
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_GROOVY_NPE"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0071
KEDB TITLE
SAP CPI Groovy Script - NullPointerException during processing
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* Groovy script fails with NullPointerException because a property, header, body node, or parsed value is missing.
* Canonical retrieval phrase: SAP CPI Groovy Script - NullPointerException during processing.
* Normalized object_name: CPI_GROOVY_NPE.
2. ERROR PATTERN
* GROOVY | SCRIPT | NULL_POINTER | NPE
3. ROOT CAUSE
* Script reads a missing property, header, or body node without a null check.
* Payload validation is missing before script access.
* Default values are not defined for optional fields.
4. DIAGNOSIS SIGNALS
* Check MPL exception details and identify the exact script line or missing value.
* Verify all required headers, properties, and payload nodes before the script step.
* Compare failing payload with the last successful payload.
* Preserve runtime evidence: Script step fails with NullPointerException.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_GROOVY_NPE and GROOVY | SCRIPT | NULL_POINTER | NPE during search and triage.
5. RESOLUTION
* Add defensive null checks before reading properties, headers, or body nodes.
* Set approved default values for optional fields.
* Reject payloads with missing mandatory values before the Groovy step.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_GROOVY_NPE and GROOVY | SCRIPT | NULL_POINTER | NPE do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Route messages with missing optional fields to a controlled exception branch until the script is corrected.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_GROOVY_NPE_P1_v1.md
* Cross-reference object_name: CPI_GROOVY_NPE
* Cross-reference taxonomy: GROOVY | SCRIPT | NULL_POINTER | NPE
* Source KEDB ID: KEDB-P1-0071
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
