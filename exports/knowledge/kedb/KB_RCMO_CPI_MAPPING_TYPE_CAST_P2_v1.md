# SAP CPI Message Mapping - Datatype conversion failed
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_MAPPING_TYPE_CAST"
priority: "P2"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P2-0080
KEDB TITLE
SAP CPI Message Mapping - Datatype conversion failed
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P2
VERSION
v1
1. SYMPTOM
* Message Mapping fails because a source string cannot be converted to the required numeric, date, or target datatype.
* Canonical retrieval phrase: SAP CPI Message Mapping - Datatype conversion failed.
* Normalized object_name: CPI_MAPPING_TYPE_CAST.
2. ERROR PATTERN
* MAPPING | CONVERSION | TYPE_CAST | INVALID_FORMAT
3. ROOT CAUSE
* Source payload contains invalid numeric or date format.
* Mapping function expects a different datatype than the source value.
* Referenced mapping artifact or conversion logic is outdated.
4. DIAGNOSIS SIGNALS
* Check mapping trace and capture the source field, value, and target type.
* Validate numeric and date formats against the interface contract.
* Confirm that mapping artifacts and UDFs are deployed in the expected version.
* Preserve runtime evidence: Correlate MessageGuid AGnVay6AcrleALzuH4lKBNGRvdnj to Interface IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Nested_Conditional_FilterByStatusCode.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_MAPPING_TYPE_CAST and MAPPING | CONVERSION | TYPE_CAST | INVALID_FORMAT during search and triage.
5. RESOLUTION
* Normalize source numeric and date formats before mapping.
* Add Groovy, XSLT, or mapping conversion logic for approved formats.
* Redeploy the corrected mapping and replay one controlled message.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_MAPPING_TYPE_CAST and MAPPING | CONVERSION | TYPE_CAST | INVALID_FORMAT do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Route records with invalid formats to an exception branch for data correction.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_MAPPING_TYPE_CAST_P2_v1.md
* Cross-reference object_name: CPI_MAPPING_TYPE_CAST
* Cross-reference taxonomy: MAPPING | CONVERSION | TYPE_CAST | INVALID_FORMAT
* Source KEDB ID: KEDB-P2-0080
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
