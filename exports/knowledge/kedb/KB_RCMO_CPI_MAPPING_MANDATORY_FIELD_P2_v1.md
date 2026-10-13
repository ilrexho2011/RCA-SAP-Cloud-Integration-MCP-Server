# SAP CPI Message Mapping - Mandatory target field missing
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_MAPPING_MANDATORY_FIELD"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0079
KEDB TITLE
SAP CPI Message Mapping - Mandatory target field missing
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Message Mapping cannot create a mandatory target field because the required source value is missing or empty.
* Canonical retrieval phrase: SAP CPI Message Mapping - Mandatory target field missing.
* Normalized object_name: CPI_MAPPING_MANDATORY_FIELD.
2. ERROR PATTERN
* MAPPING | VALIDATION | MANDATORY_FIELD | MISSING
3. ROOT CAUSE
* Source payload lacks a mandatory field.
* Mapping rule does not define an approved default value.
* Invalid records are not routed to an exception path.
4. DIAGNOSIS SIGNALS
* Check mapping trace and identify the missing source field.
* Compare the failing payload with the target schema mandatory fields.
* Confirm whether a business-approved default is allowed.
* Preserve runtime evidence: Review evidence: 2026-04-07T20:38:06.196 | MessageGuid AGnVay6AcrleALzuH4lKBNGRvdnj | Interface IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode | Sender n/a | Receiver n/a | Error: An internal server error occured: Referenced Message Mapping artifact MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode is not available.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_MAPPING_MANDATORY_FIELD and MAPPING | VALIDATION | MANDATORY_FIELD | MISSING during search and triage.
5. RESOLUTION
* Add validation for the mandatory source field before mapping.
* Set a business-approved default only when the interface contract allows it.
* Route invalid records to an exception path with the missing field name.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_MAPPING_MANDATORY_FIELD and MAPPING | VALIDATION | MANDATORY_FIELD | MISSING do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Hold invalid records and request corrected source data from the sender.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_MAPPING_MANDATORY_FIELD_P2_v1.md
* Cross-reference object_name: CPI_MAPPING_MANDATORY_FIELD
* Cross-reference taxonomy: MAPPING | VALIDATION | MANDATORY_FIELD | MISSING
* Source KEDB ID: KEDB-P2-0079
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
