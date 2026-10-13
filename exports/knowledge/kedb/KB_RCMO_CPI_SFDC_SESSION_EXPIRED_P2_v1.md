# SAP CPI Salesforce Adapter - Session expired authentication failure
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SFDC_SESSION_EXPIRED"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0085
KEDB TITLE
SAP CPI Salesforce Adapter - Session expired authentication failure
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Salesforce call fails because the session token or connected app authentication state has expired.
* Canonical retrieval phrase: SAP CPI Salesforce Adapter - Session expired authentication failure.
* Normalized object_name: CPI_SFDC_SESSION_EXPIRED.
2. ERROR PATTERN
* SALESFORCE | AUTHENTICATION | SESSION_EXPIRED | TOKEN_REFRESH
3. ROOT CAUSE
* CPI Salesforce credential or session token is stale.
* Connected app session policy changed.
* Token refresh configuration is not valid for the adapter.
4. DIAGNOSIS SIGNALS
* Check MPL for Salesforce session expired or authentication failure text.
* Verify CPI Security Material and Salesforce connected app settings.
* Confirm session policy and token refresh behavior with the Salesforce owner.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SFDC_SESSION_EXPIRED and SALESFORCE | AUTHENTICATION | SESSION_EXPIRED | TOKEN_REFRESH during search and triage.
5. RESOLUTION
* Refresh the Salesforce connection or credential alias in CPI.
* Update connected app session settings when policy changed.
* Retest the iFlow with one controlled Salesforce call.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SFDC_SESSION_EXPIRED and SALESFORCE | AUTHENTICATION | SESSION_EXPIRED | TOKEN_REFRESH do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Pause automatic retries until a refreshed session succeeds.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SFDC_SESSION_EXPIRED_P2_v1.md
* Cross-reference object_name: CPI_SFDC_SESSION_EXPIRED
* Cross-reference taxonomy: SALESFORCE | AUTHENTICATION | SESSION_EXPIRED | TOKEN_REFRESH
* Source KEDB ID: KEDB-P2-0085
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
