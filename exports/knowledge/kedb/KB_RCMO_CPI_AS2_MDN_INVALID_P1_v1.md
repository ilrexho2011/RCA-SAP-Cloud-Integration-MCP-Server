# SAP CPI AS2 MDN_INVALID - AS2 MDN validation failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_AS2_MDN_INVALID"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0065
KEDB TITLE
SAP CPI AS2 MDN_INVALID - AS2 MDN validation failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* AS2 MDN receipt validation fails because the signature, MIC, AS2 ID, or certificate does not match the partner profile.
* Canonical retrieval phrase: SAP CPI AS2 MDN_INVALID - AS2 MDN validation failed.
* Normalized object_name: CPI_AS2_MDN_INVALID.
2. ERROR PATTERN
* AS2 | MDN | VALIDATION | MDN_INVALID
3. ROOT CAUSE
* Certificate mismatch between CPI Security Material and partner profile.
* AS2 ID, MIC algorithm, or MDN mode differs from partner agreement.
* Partner sends an invalid or unsigned MDN receipt.
4. DIAGNOSIS SIGNALS
* Check MPL for the failed AS2 exchange and capture MessageGuid, timestamp, sender, receiver, and error text.
* Compare AS2 IDs, MIC algorithm, certificate chain, and MDN settings with the partner profile.
* Verify that the active CPI certificate matches the partner trust configuration.
* Preserve runtime evidence: Use MPL evidence: 2026-03-12T17:52:56.903 | MessageGuid AGmy_XjJqg48DvTTceN0HNUs4aLp | Interface IR20_IF03_Fetch_data_from_Google_Sheets_via_Open_Connectors | Sender n/a | Receiver n/a | Error: HTTP operation failed : {"requestId":"69b2fd79e4b0343f264930ef","message":"Invalid Organization or User secret provided"} status code : 401.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_AS2_MDN_INVALID and AS2 | MDN | VALIDATION | MDN_INVALID during search and triage.
5. RESOLUTION
* Align AS2 IDs, MIC algorithm, certificate, and MDN settings with the partner profile.
* Import or replace the correct certificate in CPI Security Material.
* Redeploy the iFlow and replay one controlled AS2 message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_AS2_MDN_INVALID and AS2 | MDN | VALIDATION | MDN_INVALID do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Use synchronous MDN temporarily only if the partner profile supports it.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_AS2_MDN_INVALID_P1_v1.md
* Cross-reference object_name: CPI_AS2_MDN_INVALID
* Cross-reference taxonomy: AS2 | MDN | VALIDATION | MDN_INVALID
* Source KEDB ID: KEDB-P1-0065
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
