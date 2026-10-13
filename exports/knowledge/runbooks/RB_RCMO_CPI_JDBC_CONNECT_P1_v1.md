# SAP CPI JDBC Adapter - Database connection refused

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_JDBC\_CONNECT"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0075
RUNBOOK TITLE
SAP CPI JDBC Adapter - Database connection refused
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI JDBC Adapter - Database connection refused.
* Use this runbook only for object\_name CPI\_JDBC\_CONNECT and taxonomy JDBC | CONNECTIVITY | CONNECTION\_REFUSED | DB\_PORT.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: JDBC connection cannot be opened because the database host, port, driver, Cloud Connector, or credentials are unavailable or wrong.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: JDBC Receiver Adapter.
* Protocol family: JDBC.
* Error pattern: JDBC | CONNECTIVITY | CONNECTION\_REFUSED | DB\_PORT.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0075.
* Source KEDB artifact: KB\_RCMO\_CPI\_JDBC\_CONNECT\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI JDBC Adapter - Database connection refused.
* Normalized object\_name: CPI\_JDBC\_CONNECT.
* Normalized taxonomy: JDBC | CONNECTIVITY | CONNECTION\_REFUSED | DB\_PORT.
* Sample 1 | 2026-04-06T22:30:49.957 | MessageGuid AGnUNBnbavGGocjWdJVbvCyhuISG | Interface IR\_IF034\_SFTP\_Passthrough\_Sample\_Source\_to\_Target | Sender n/a | Receiver n/a
* Sample 2: Evidence required | MessageGuid, time window, failing step if known, error text, configuration delta, replay outcome
5. ERROR SIGNATURE
* Title: SAP CPI JDBC Adapter - Database connection refused.
* Short symptom: JDBC connection cannot be opened because the database host, port, driver, Cloud Connector, or credentials are unavailable or wrong.
* Normalized object name: CPI\_JDBC\_CONNECT.
* Normalized taxonomy: JDBC | CONNECTIVITY | CONNECTION\_REFUSED | DB\_PORT.
6. KNOWN ROOT CAUSES
* Database host or port is unreachable from CPI.
* JDBC driver, URL, or connection parameters are wrong.
* Cloud Connector, VPN, or database listener is unavailable.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for JDBC connection error and capture host, port, and MessageGuid.
* Verify Cloud Connector or network route to the database host.
* Validate JDBC URL, driver, credential alias, and database listener status.
* Compare the failing execution with the last successful MPL execution for CPI\_JDBC\_CONNECT.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Correct JDBC URL, host, port, driver, and credential alias.
* Restore Cloud Connector, VPN, or database listener availability.
* Redeploy and test one controlled JDBC operation.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_JDBC\_CONNECT is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_JDBC\_CONNECT and JDBC | CONNECTIVITY | CONNECTION\_REFUSED | DB\_PORT do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

