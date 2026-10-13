# SAP CPI SOAP Receiver - SOAP fault from target system
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SOAP_FAULT"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0089
KEDB TITLE
SAP CPI SOAP Receiver - SOAP fault from target system
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* SOAP receiver returns a fault because the request payload, namespace, schema, or backend business validation fails.
* Canonical retrieval phrase: SAP CPI SOAP Receiver - SOAP fault from target system.
* Normalized object_name: CPI_SOAP_FAULT.
2. ERROR PATTERN
* SOAP | RECEIVER | FAULT | TARGET_SYSTEM
3. ROOT CAUSE
* SOAP request schema does not match the receiver contract.
* Namespaces or mapping content are wrong.
* Target system business validation rejects the request.
4. DIAGNOSIS SIGNALS
* Check MPL SOAP fault detail and preserve exact fault code and fault string.
* Validate outbound SOAP envelope against the receiver WSDL/schema.
* Compare namespaces and mapped values with the receiver contract.
* Preserve runtime evidence: Receiver returns SOAP Fault to CPI.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SOAP_FAULT and SOAP | RECEIVER | FAULT | TARGET_SYSTEM during search and triage.
5. RESOLUTION
* Correct namespaces and payload structure in the SOAP request mapping.
* Fix business data rejected by the target system.
* Retest with one representative SOAP message after receiver confirmation.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SOAP_FAULT and SOAP | RECEIVER | FAULT | TARGET_SYSTEM do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Hold affected messages and avoid automatic retry until the SOAP fault cause is corrected.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SOAP_FAULT_P1_v1.md
* Cross-reference object_name: CPI_SOAP_FAULT
* Cross-reference taxonomy: SOAP | RECEIVER | FAULT | TARGET_SYSTEM
* Source KEDB ID: KEDB-P1-0089
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
