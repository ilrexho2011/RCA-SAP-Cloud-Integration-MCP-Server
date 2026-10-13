# SAP CPI HTTP Receiver - 404 Not Found response
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_NOT_FOUND_404_HTTP_1_1"
priority: "P2"
interface_id: "IR16_IF05_MY_MPL_Alert_System"
integration_flow_id: "IR16_IF05_MY_MPL_Alert_System"
integration_flow_name: "IR16_IF05_MY_MPL_Alert_System"
package_name: "16 - Variables and Exception Handling in SAP CPI"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0081
KEDB TITLE
SAP CPI HTTP Receiver - 404 Not Found response
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* HTTP receiver call returns 404 Not Found because the endpoint path, resource, route, or receiver deployment is missing.
* Canonical retrieval phrase: SAP CPI HTTP Receiver - 404 Not Found response.
* Normalized object_name: CPI_NOT_FOUND_404_HTTP_1_1.
2. ERROR PATTERN
* HTTP | CLIENT_ERROR | NOT_FOUND | 404
3. ROOT CAUSE
* Receiver URL path or resource name is wrong.
* Target service route is not deployed or not exposed.
* Externalized endpoint parameter points to a stale receiver path.
4. DIAGNOSIS SIGNALS
* Check MPL for HTTP/1.1 404 Not Found, receiver URL, MessageGuid, and timestamp.
* Verify the receiver endpoint path against the current API specification.
* Confirm route exposure, API management path, and deployment state.
* Preserve runtime evidence: Not Found : 404 : HTTP/1.1
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_NOT_FOUND_404_HTTP_1_1 and HTTP | CLIENT_ERROR | NOT_FOUND | 404 during search and triage.
5. RESOLUTION
* Correct the receiver URL path or externalized endpoint parameter.
* Deploy or expose the missing target service route.
* Redeploy the iFlow and replay one controlled HTTP message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_NOT_FOUND_404_HTTP_1_1 and HTTP | CLIENT_ERROR | NOT_FOUND | 404 do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IR16_IF05_MY_MPL_Alert_System.
7. WORKAROUND
* Use the previous approved endpoint only if the receiver owner confirms compatibility.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_NOT_FOUND_404_HTTP_1_1_P2_v1.md
* Cross-reference object_name: CPI_NOT_FOUND_404_HTTP_1_1
* Cross-reference taxonomy: HTTP | CLIENT_ERROR | NOT_FOUND | 404
* Source KEDB ID: KEDB-P2-0081
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
