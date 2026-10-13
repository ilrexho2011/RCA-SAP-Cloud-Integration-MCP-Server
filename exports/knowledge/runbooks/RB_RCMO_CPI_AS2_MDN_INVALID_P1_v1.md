# SAP CPI AS2 MDN\_INVALID - AS2 MDN validation failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_AS2\_MDN\_INVALID"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0065
RUNBOOK TITLE
SAP CPI AS2 MDN\_INVALID - AS2 MDN validation failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI AS2 MDN\_INVALID - AS2 MDN validation failed.
* Use this runbook only for object\_name CPI\_AS2\_MDN\_INVALID and taxonomy AS2 | MDN | VALIDATION | MDN\_INVALID.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: AS2 MDN receipt validation fails because the signature, MIC, AS2 ID, or certificate does not match the partner profile.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: AS2 Adapter.
* Protocol family: AS2.
* Error pattern: AS2 | MDN | VALIDATION | MDN\_INVALID.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0065.
* Source KEDB artifact: KB\_RCMO\_CPI\_AS2\_MDN\_INVALID\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI AS2 MDN\_INVALID - AS2 MDN validation failed.
* Normalized object\_name: CPI\_AS2\_MDN\_INVALID.
* Normalized taxonomy: AS2 | MDN | VALIDATION | MDN\_INVALID.
* Sample 1: 2026-03-12T17:52:56.903 | MessageGuid AGmy\_XjJqg48DvTTceN0HNUs4aLp | Interface IR20\_IF03\_Fetch\_data\_from\_Google\_Sheets\_via\_Open\_Connectors | Sender n/a | Receiver n/a | Error: HTTP operation failed : {"requestId":"69b2fd79e4b0343f264930ef","message":"Invalid Organization or User secret provided"} status code : 401.
* Sample 2: Provide evidence: MessageGuid | time window | failing step if known | error text | configuration delta | replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI AS2 MDN\_INVALID - AS2 MDN validation failed.
* Short symptom: AS2 MDN receipt validation fails because the signature, MIC, AS2 ID, or certificate does not match the partner profile.
* Normalized object name: CPI\_AS2\_MDN\_INVALID.
* Normalized taxonomy: AS2 | MDN | VALIDATION | MDN\_INVALID.
6. KNOWN ROOT CAUSES
* Certificate mismatch between CPI Security Material and partner profile.
* AS2 ID, MIC algorithm, or MDN mode differs from partner agreement.
* Partner sends an invalid or unsigned MDN receipt.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for the failed AS2 exchange and capture MessageGuid, timestamp, sender, receiver, and error text.
* Compare AS2 IDs, MIC algorithm, certificate chain, and MDN settings with the partner profile.
* Verify that the active CPI certificate matches the partner trust configuration.
* Compare the failing execution with the last successful MPL execution for CPI\_AS2\_MDN\_INVALID.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Align AS2 IDs, MIC algorithm, certificate, and MDN settings with the partner profile.
* Import or replace the correct certificate in CPI Security Material.
* Redeploy the iFlow and replay one controlled AS2 message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_AS2\_MDN\_INVALID is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_AS2\_MDN\_INVALID and AS2 | MDN | VALIDATION | MDN\_INVALID do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

