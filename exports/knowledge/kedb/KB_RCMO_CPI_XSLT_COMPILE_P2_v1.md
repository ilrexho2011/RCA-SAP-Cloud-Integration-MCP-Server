# SAP CPI XSLT Mapping - Stylesheet compilation error
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_XSLT_COMPILE"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0093
KEDB TITLE
SAP CPI XSLT Mapping - Stylesheet compilation error
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* XSLT mapping fails because the stylesheet contains invalid syntax, unsupported functions, or incompatible runtime constructs.
* Canonical retrieval phrase: SAP CPI XSLT Mapping - Stylesheet compilation error.
* Normalized object_name: CPI_XSLT_COMPILE.
2. ERROR PATTERN
* XSLT | COMPILE | SYNTAX | ERROR
3. ROOT CAUSE
* Stylesheet syntax is invalid.
* Unsupported extension function is used.
* XSLT artifact version is not deployed with the expected content.
4. DIAGNOSIS SIGNALS
* Check MPL for XSLT compile error and exact line or function reference.
* Validate the stylesheet outside CPI with the target XSLT version.
* Confirm deployed XSLT artifact version in the iFlow package.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_XSLT_COMPILE and XSLT | COMPILE | SYNTAX | ERROR during search and triage.
5. RESOLUTION
* Fix stylesheet syntax and remove unsupported functions.
* Redeploy the corrected XSLT artifact with the iFlow.
* Replay one controlled XML message after compilation succeeds.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_XSLT_COMPILE and XSLT | COMPILE | SYNTAX | ERROR do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Use the last known stable XSLT version if the corrected artifact fails validation.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_XSLT_COMPILE_P2_v1.md
* Cross-reference object_name: CPI_XSLT_COMPILE
* Cross-reference taxonomy: XSLT | COMPILE | SYNTAX | ERROR
* Source KEDB ID: KEDB-P2-0093
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
