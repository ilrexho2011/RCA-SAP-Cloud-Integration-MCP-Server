# SAP CPI JDBC Adapter - Database connection refused
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_JDBC_CONNECT"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0075
KEDB TITLE
SAP CPI JDBC Adapter - Database connection refused
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* JDBC connection cannot be opened because the database host, port, driver, Cloud Connector, or credentials are unavailable or wrong.
* Canonical retrieval phrase: SAP CPI JDBC Adapter - Database connection refused.
* Normalized object_name: CPI_JDBC_CONNECT.
2. ERROR PATTERN
* JDBC | CONNECTIVITY | CONNECTION_REFUSED | DB_PORT
3. ROOT CAUSE
* Database host or port is unreachable from CPI.
* JDBC driver, URL, or connection parameters are wrong.
* Cloud Connector, VPN, or database listener is unavailable.
4. DIAGNOSIS SIGNALS
* Check MPL for JDBC connection error and capture host, port, and MessageGuid.
* Verify Cloud Connector or network route to the database host.
* Validate JDBC URL, driver, credential alias, and database listener status.
* Preserve runtime evidence: Check MPL API evidence for connection failure timestamps and MessageGuid.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_JDBC_CONNECT and JDBC | CONNECTIVITY | CONNECTION_REFUSED | DB_PORT during search and triage.
5. RESOLUTION
* Correct JDBC URL, host, port, driver, and credential alias.
* Restore Cloud Connector, VPN, or database listener availability.
* Redeploy and test one controlled JDBC operation.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_JDBC_CONNECT and JDBC | CONNECTIVITY | CONNECTION_REFUSED | DB_PORT do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Switch to the approved backup database route only after database owner confirmation.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_JDBC_CONNECT_P1_v1.md
* Cross-reference object_name: CPI_JDBC_CONNECT
* Cross-reference taxonomy: JDBC | CONNECTIVITY | CONNECTION_REFUSED | DB_PORT
* Source KEDB ID: KEDB-P1-0075
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
