# SAP CPI HTTPS Adapter - SSL handshake failure

environment: "demo"
customer\_id: "RCMO"
system\_id: "CPI-RCMO"
sap\_sid: "CPI"
artifact\_type: "runbook"
object\_name: "CPI\_SSL\_HANDSHAKE"
priority: "P1"
interface\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_id: "IFLOW\_CUSTOMER\_SYNC"
integration\_flow\_name: "IFLOW\_CUSTOMER\_SYNC"
package\_name: "Multiple packages"
review\_cycle: "monthly"
version: "v1"
RUNBOOK ID
RB-P1-0091
RUNBOOK TITLE
SAP CPI HTTPS Adapter - SSL handshake failure
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1

1. PURPOSE
* Triage, diagnose, recover, and validate one canonical SAP CPI issue: SAP CPI HTTPS Adapter - SSL handshake failure.
* Use this runbook only for object\_name CPI\_SSL\_HANDSHAKE and taxonomy TLS | SSL\_HANDSHAKE | CERTIFICATE | TRUST\_FAILURE.
2. BUSINESS CONTEXT
* Business process: Scenario-dependent SAP CPI integration processing.
* Primary reference interface: IFLOW\_CUSTOMER\_SYNC.
* Impact: TLS session cannot be established because certificate chain, trust, hostname, or protocol settings are invalid.
* Priority: P1.
3. TECHNICAL LANDSCAPE
* Package: Multiple packages.
* Integration flow ID: IFLOW\_CUSTOMER\_SYNC.
* Integration flow name: IFLOW\_CUSTOMER\_SYNC.
* Processing component: HTTPS/HTTP Adapter.
* Protocol family: TLS/HTTPS.
* Error pattern: TLS | SSL\_HANDSHAKE | CERTIFICATE | TRUST\_FAILURE.
* System type: CPI.
* Source KEDB ID(s): KEDB-P1-0091.
* Source KEDB artifact: KB\_RCMO\_CPI\_SSL\_HANDSHAKE\_P1\_v1.md.
4. MONITORING AND MPL EVIDENCE
* Query-facing signature: SAP CPI HTTPS Adapter - SSL handshake failure.
* Normalized object\_name: CPI\_SSL\_HANDSHAKE.
* Normalized taxonomy: TLS | SSL\_HANDSHAKE | CERTIFICATE | TRUST\_FAILURE.
* Sample 1: Provide MessageGuid, time window, failing step if known, error text, configuration delta, and replay outcome.
5. ERROR SIGNATURE
* Title: SAP CPI HTTPS Adapter - SSL handshake failure.
* Short symptom: TLS session cannot be established because certificate chain, trust, hostname, or protocol settings are invalid.
* Normalized object name: CPI\_SSL\_HANDSHAKE.
* Normalized taxonomy: TLS | SSL\_HANDSHAKE | CERTIFICATE | TRUST\_FAILURE.
6. KNOWN ROOT CAUSES
* Receiver certificate is expired or missing from CPI trust store.
* Certificate chain is incomplete.
* TLS protocol or hostname verification does not match receiver configuration.
7. PREREQUISITES FOR INVESTIGATION
* Access SAP CPI Monitor, MPL, trace, and deployed artifact view.
* Access package Multiple packages and interface IFLOW\_CUSTOMER\_SYNC.
* Capture the exact MessageGuid, timestamp, error text, adapter, sender, receiver, and recent configuration delta.
* Obtain one representative failing payload or reproducible test message when available.
8. DIAGNOSIS STEPS
* Check MPL for SSLHandshakeException and certificate error details.
* Inspect receiver certificate validity, issuer, SAN, and full chain.
* Verify CPI Security Material, trust store, and TLS protocol compatibility.
* Compare the failing execution with the last successful MPL execution for CPI\_SSL\_HANDSHAKE.
9. RECOVERY STEPS
* Contain the incident and preserve evidence before changing runtime configuration.
* Import the full trusted certificate chain into CPI Security Material.
* Renew expired receiver certificates.
* Align TLS protocol and hostname settings between CPI and receiver.
* Rollback: restore the last known stable configuration if validation fails.
* Rollback: stop replay and keep affected messages quarantined while the same signature persists.
10. ESCALATION CRITERIA
* Support owner: IntegrationTeam.
* Service owner: RCMO Integration Service Owner.
* Escalation group: RCMO-CPI-L2.
* Escalate when CPI\_SSL\_HANDSHAKE is reproducible, business-visible, recurrent, or cannot be stabilized through normal operational handling.
* Provide evidence: MessageGuid, time window, exact error text, adapter, endpoint or configuration delta, and replay outcome.
11. POST-FIX VALIDATION
* Verify MPL status COMPLETED for one controlled representative message.
* Confirm that CPI\_SSL\_HANDSHAKE and TLS | SSL\_HANDSHAKE | CERTIFICATE | TRUST\_FAILURE do not reappear in the immediate monitoring window.
* Confirm downstream acknowledgement or receiver-side processing success.
* Reprocess backlog only after controlled validation succeeds.
* Retry pattern: avoid blind mass replay; use sequenced replay with MPL observation.

