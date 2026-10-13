# SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV"
priority: "P2"
interface_id: "IR20_IF02_Email_Alert_Notifications_For_SAP_CPI_Tenant"
integration_flow_id: "IR20_IF02_Email_Alert_Notifications_For_SAP_CPI_Tenant"
integration_flow_name: "IR20_IF02_Email_Alert_Notifications_For_SAP_CPI_Tenant"
package_name: "20 - Complex Projects"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0073
KEDB TITLE
SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* HTTP receiver call fails with UnknownHostException or Name or service not known because the target hostname cannot be resolved.
* Canonical retrieval phrase: SAP CPI HTTP request failed - HTTPS name or service not known UnknownHostException.
* Normalized object_name: CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV.
2. ERROR PATTERN
* HTTP | CONNECTIVITY | DNS_RESOLUTION | UNKNOWN_HOST
3. ROOT CAUSE
* Receiver URL contains an invalid hostname or malformed scheme.
* DNS resolution is missing for the target host.
* Cloud Connector or proxy route does not expose the receiver host.
4. DIAGNOSIS SIGNALS
* Check MPL for UnknownHostException, receiver URL, MessageGuid, and timestamp.
* Verify the receiver endpoint hostname without protocol duplication or malformed path.
* Test DNS, proxy, and Cloud Connector route from the CPI connectivity context.
* Preserve runtime evidence: HTTP Request failed with error : https: Name or service not known, cause: java.net.UnknownHostException: https: Name or service not known
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV and HTTP | CONNECTIVITY | DNS_RESOLUTION | UNKNOWN_HOST during search and triage.
5. RESOLUTION
* Correct the receiver URL and hostname in the HTTP adapter or externalized parameter.
* Fix DNS, proxy, or Cloud Connector mapping for the target host.
* Redeploy the iFlow and replay one controlled HTTP message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV and HTTP | CONNECTIVITY | DNS_RESOLUTION | UNKNOWN_HOST do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IR20_IF02_Email_Alert_Notifications_For_SAP_CPI_Tenant.
7. WORKAROUND
* Route traffic to the approved backup endpoint only if the receiver owner confirms failover readiness.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV_P2_v1.md
* Cross-reference object_name: CPI_HTTP_REQUEST_FAILED_WITH_ERROR_HTTPS_NAME_OR_SERVICE_NOT_KNOWN_CAUSE_JAV
* Cross-reference taxonomy: HTTP | CONNECTIVITY | DNS_RESOLUTION | UNKNOWN_HOST
* Source KEDB ID: KEDB-P2-0073
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
