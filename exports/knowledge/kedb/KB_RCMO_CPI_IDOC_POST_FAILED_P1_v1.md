# SAP CPI IDoc Receiver - IDoc posting failed in SAP backend

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "kedb"
object\_name: "CPI\_IDOC\_POST\_FAILED"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0074
KEDB TITLE
SAP CPI IDoc Receiver - IDoc posting failed in SAP backend
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. SYMPTOM
* IDoc posting fails because the SAP backend rejects the IDoc package, partner profile, port, or authorization.
* Canonical retrieval phrase: SAP CPI IDoc Receiver - IDoc posting failed in SAP backend.
* Normalized object\_name: CPI\_IDOC\_POST\_FAILED.
2. ERROR PATTERN
* IDOC | POST | RECEIVER | FAILED
3. ROOT CAUSE
* WE20 partner profile or WE21 port is not aligned with the CPI sender.
* IDoc type or extension does not match the backend configuration.
* Receiver user lacks required authorization for IDoc posting.
4. DIAGNOSIS SIGNALS
* Check MPL for IDoc adapter error and capture MessageGuid and receiver system.
* Verify WE20 partner profile, WE21 port, IDoc type, and authorization in SAP backend.
* Compare the outbound IDoc control record with backend requirements.
* Preserve runtime evidence: Use the captured evidence line: 2026-03-27T19:17:32.932 | MessageGuid AGnG18yd-0kZVD\_oyD8gRzoUxifc | Interface IR01\_IF09\_Access\_Message\_Processing\_ErrorLogs\_2 | Sender n/a | Receiver n/a | Error: An internal server error occured: No body available of type: java.io.InputStream but has value: <MessageError> <MessageGuid>AGmt6OsRi31wm\_R6tJgjIJkgS3s0</MessageGuid> <ErrorMessage>com.sap.it.rt.adapter.http.api.exception.HttpResponseException: An internal server error occured...
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI\_IDOC\_POST\_FAILED and IDOC | POST | RECEIVER | FAILED during search and triage.
5. RESOLUTION
* Correct WE20, WE21, IDoc type, or authorization in the receiver SAP system.
* Redeploy the CPI iFlow only if adapter configuration changed.
* Repost one controlled IDoc after backend validation succeeds.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI\_IDOC\_POST\_FAILED and IDOC | POST | RECEIVER | FAILED do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW\_CUSTOMER\_SYNC.
7. WORKAROUND
* Hold failed IDocs in error status and avoid mass repost until backend configuration is corrected.
8. RELATED ARTIFACTS
* Primary runbook: RB\_RCMO\_CPI\_IDOC\_POST\_FAILED\_P1\_v1.md
* Cross-reference object\_name: CPI\_IDOC\_POST\_FAILED
* Cross-reference taxonomy: IDOC | POST | RECEIVER | FAILED
* Source KEDB ID: KEDB-P1-0074
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.

