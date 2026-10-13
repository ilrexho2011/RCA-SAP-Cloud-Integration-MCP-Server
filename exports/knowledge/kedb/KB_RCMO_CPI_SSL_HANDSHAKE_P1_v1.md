# SAP CPI HTTPS Adapter - SSL handshake failure
environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "kedb"
object_name: "CPI_SSL_HANDSHAKE"
priority: "P1"
interface_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_id: "IFLOW_CUSTOMER_SYNC"
integration_flow_name: "IFLOW_CUSTOMER_SYNC"
package_name: "Multiple packages"
review_cycle: "monthly"
version: "v1"
KEDB ID
KEDB-P1-0091
KEDB TITLE
SAP CPI HTTPS Adapter - SSL handshake failure
CUSTOMER
RCMO
SYSTEM
CPI
PRIORITY
P1
VERSION
v1
1. SYMPTOM
* TLS session cannot be established because certificate chain, trust, hostname, or protocol settings are invalid.
* Canonical retrieval phrase: SAP CPI HTTPS Adapter - SSL handshake failure.
* Normalized object_name: CPI_SSL_HANDSHAKE.
2. ERROR PATTERN
* TLS | SSL_HANDSHAKE | CERTIFICATE | TRUST_FAILURE
3. ROOT CAUSE
* Receiver certificate is expired or missing from CPI trust store.
* Certificate chain is incomplete.
* TLS protocol or hostname verification does not match receiver configuration.
4. DIAGNOSIS SIGNALS
* Check MPL for SSLHandshakeException and certificate error details.
* Inspect receiver certificate validity, issuer, SAN, and full chain.
* Verify CPI Security Material, trust store, and TLS protocol compatibility.
* Preserve runtime evidence when available: MessageGuid, CorrelationId, HTTP status, adapter, sender, receiver, and error text.
* Capture evidence fields: MessageGuid, CorrelationId, adapter, sender, receiver, HTTP status if relevant, and exact error text.
* Match the canonical terms CPI_SSL_HANDSHAKE and TLS | SSL_HANDSHAKE | CERTIFICATE | TRUST_FAILURE during search and triage.
5. RESOLUTION
* Import the full trusted certificate chain into CPI Security Material.
* Renew expired receiver certificates.
* Align TLS protocol and hostname settings between CPI and receiver.
6. VALIDATION
* Verify MPL status COMPLETED for the representative message after remediation.
* Confirm that CPI_SSL_HANDSHAKE and TLS | SSL_HANDSHAKE | CERTIFICATE | TRUST_FAILURE do not reappear in the post-fix monitoring window.
* Confirm business processing with interface IFLOW_CUSTOMER_SYNC.
7. WORKAROUND
* Use the approved trusted reverse proxy only as a temporary containment path.
8. RELATED ARTIFACTS
* Primary runbook: RB_RCMO_CPI_SSL_HANDSHAKE_P1_v1.md
* Cross-reference object_name: CPI_SSL_HANDSHAKE
* Cross-reference taxonomy: TLS | SSL_HANDSHAKE | CERTIFICATE | TRUST_FAILURE
* Source KEDB ID: KEDB-P1-0091
* Owner: IntegrationTeam
* Notes: Remediated for AI4BIZ ingestion policy and BM25 retrieval alignment without changing field names or section order.
