# SAP CPI Message Mapping - Datatype conversion failed

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_MAPPING\_TYPE\_CAST"
priority: "P2"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P2-0080
RUNBOOK TITLE
SAP CPI Message Mapping - Datatype conversion failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI Message Mapping - Datatype conversion failed.
* Use this runbook only for object\_name CPI\_MAPPING\_TYPE\_CAST and taxonomy MAPPING | CONVERSION | TYPE\_CAST | INVALID\_FORMAT.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: Message Mapping fails because a source string cannot be converted to the required numeric, date, or target datatype.
* Priority: P2.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: Message Mapping.
* Protocol family: XML/JSON Mapping.
* Error pattern: MAPPING | CONVERSION | TYPE\_CAST | INVALID\_FORMAT.
* System type: CPI.
* Source KEDB ID(s): KEDB-P2-0080.
* Source KEDB artifact: KB\_RCMO\_CPI\_MAPPING\_TYPE\_CAST\_P2\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI Message Mapping - Datatype conversion failed.
* Normalized object\_name: CPI\_MAPPING\_TYPE\_CAST.
* Normalized taxonomy: MAPPING | CONVERSION | TYPE\_CAST | INVALID\_FORMAT.
* Sample 1: 2026-04-07T20:38:06.196 | MessageGuid AGnVay6AcrleALzuH4lKBNGRvdnj | Interface IR12\_IF03\_MM\_CategoryFlat\_to\_CategoryFlat\_Nested\_Conditional\_FilterByStatusCode | Sender n/a | Receiver n/a | Error: An internal server error occured: Referenced Message Mapping artifact MM\_CategoryFlat\_to\_CategoryFlat\_Nested\_Conditional\_FilterByStatusCode is not available
* Sample 2: 2026-04-07T20:35:11.898 | MessageGuid AGnVan\_l9TDnZT1wVGVPl\_qV8Ren | Interface IR12\_IF03\_MM\_CategoryFlat\_to\_CategoryFlat\_Conditional\_CreateIF\_FilterByStatusCode | Sender n/a | Receiver n/a | Error: An internal server error occured: Referenced Message Mapping artifact MM\_CategoryFlat\_to\_CategoryFlat\_FilterByStatusCode\_If\_Else is not available
5. ERROR SIGNATURE
* Title: SAP CPI Message Mapping - Datatype conversion failed.
* Short symptom: Message Mapping fails because a source string cannot be converted to the required numeric, date, or target datatype.
* Normalized object name: CPI\_MAPPING\_TYPE\_CAST.
* Normalized taxonomy: MAPPING | CONVERSION | TYPE\_CAST | INVALID\_FORMAT.
6. KNOWN ROOT CAUSES
* Source payload contains invalid numeric or date format.
* Mapping function expects a different datatype than the source value.
* Referenced mapping artifact or conversion logic is outdated.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check mapping trace and capture the source field, value, and target type.
* Validate numeric and date formats against the interface contract.
* Confirm that mapping artifacts and UDFs are deployed in the expected version.
* Compare the failing execution with the last successful MPL execution for CPI\_MAPPING\_TYPE\_CAST.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Normalize source numeric and date formats before mapping.
* Add Groovy, XSLT, or mapping conversion logic for approved formats.
* Redeploy the corrected mapping and replay one controlled message.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_MAPPING\_TYPE\_CAST is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_MAPPING\_TYPE\_CAST and MAPPING | CONVERSION | TYPE\_CAST | INVALID\_FORMAT do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

