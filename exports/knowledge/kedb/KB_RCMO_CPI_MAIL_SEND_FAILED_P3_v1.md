# SAP CPI Mail Adapter - SMTP send failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "kedb"
object\_name: "CPI\_MAIL\_SEND\_FAILED"
priority: "P3"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P3-0078
KEDB TITLE
SAP CPI Mail Adapter - SMTP send failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P3
VERSION
v1

1. SYMPTOM
* Mail adapter send fails because SMTP host, port, authentication, TLS, or recipient configuration is invalid.
* Canonical retrieval phrase: SAP CPI Mail Adapter - SMTP send failed.
* Normalized object\_name: CPI\_MAIL\_SEND\_FAILED.
2. ERROR PATTERN
* MAIL | SMTP | SEND | FAILED
3. ROOT CAUSE
* SMTP host, port, authentication, or TLS setting is wrong.
* Mail credential alias is expired or invalid.
* Recipient address or relay policy rejects the message.
4. DIAGNOSIS SIGNALS
* Check MPL for SMTP status, receiver host, and MessageGuid.
* Verify Mail adapter host, port, security mode, credential alias, and recipient list.
* Test relay policy with the mail service owner.
* Preserve runtime evidence: Evidence: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI\_MAIL\_SEND\_FAILED and MAIL | SMTP | SEND | FAILED during search and triage.
5. RESOLUTION
* Correct SMTP host, port, authentication, TLS, and recipient configuration.
* Update expired credentials in CPI Security Material.
* Redeploy and send one controlled test notification.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI\_MAIL\_SEND\_FAILED and MAIL | SMTP | SEND | FAILED do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW\_CUSTOMER\_SYNC.
7. WORKAROUND
* Use the approved alternate alert channel until SMTP recovery is confirmed.
8. RELATED ARTIFACTS
* Primary runbook: RB\_RCMO\_CPI\_MAIL\_SEND\_FAILED\_P3\_v1.md
* Cross-reference object\_name: CPI\_MAIL\_SEND\_FAILED
* Cross-reference taxonomy: MAIL | SMTP | SEND | FAILED
* Source KEDB ID: KEDB-P3-0078
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.

