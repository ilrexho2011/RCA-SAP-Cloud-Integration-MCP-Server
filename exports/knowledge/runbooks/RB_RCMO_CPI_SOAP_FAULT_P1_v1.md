# SAP CPI SOAP Receiver - SOAP fault from target system

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SOAP\_FAULT"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0089
RUNBOOK TITLE
SAP CPI SOAP Receiver - SOAP fault from target system
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI SOAP Receiver - SOAP fault from target system.
* Use this runbook only for object\_name CPI\_SOAP\_FAULT and taxonomy SOAP | RECEIVER | FAULT | TARGET\_SYSTEM.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: SOAP receiver returns a fault because the request payload, namespace, schema, or backend business validation fails.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: SOAP Receiver Adapter.
* Protocol family: SOAP.
* Error pattern: SOAP | RECEIVER | FAULT | TARGET\_SYSTEM.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0089.
* Source KEDB artifact: KB\_RCMO\_CPI\_SOAP\_FAULT\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI SOAP Receiver - SOAP fault from target system.
* Normalized object\_name: CPI\_SOAP\_FAULT.
* Normalized taxonomy: SOAP | RECEIVER | FAULT | TARGET\_SYSTEM.
* Sample 1: Impact | SOAP Fault returned by target system.
* Sample 1 | No directly matching MPL example available in the provided export.
5. ERROR SIGNATURE
* Title: SAP CPI SOAP Receiver - SOAP fault from target system.
* Short symptom: SOAP receiver returns a fault because the request payload, namespace, schema, or backend business validation fails.
* Normalized object name: CPI\_SOAP\_FAULT.
* Normalized taxonomy: SOAP | RECEIVER | FAULT | TARGET\_SYSTEM.
6. KNOWN ROOT CAUSES
* SOAP request schema does not match the receiver contract.
* Namespaces or mapping content are wrong.
* Target system business validation rejects the request.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL SOAP fault detail and preserve exact fault code and fault string.
* Validate outbound SOAP envelope against the receiver WSDL/schema.
* Compare namespaces and mapped values with the receiver contract.
* Compare the failing execution with the last successful MPL execution for CPI\_SOAP\_FAULT.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct namespaces and payload structure in the SOAP request mapping.
* Fix business data rejected by the target system.
* Retest with one representative SOAP message after receiver confirmation.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SOAP\_FAULT is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SOAP\_FAULT and SOAP | RECEIVER | FAULT | TARGET\_SYSTEM do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

