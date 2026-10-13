# Sender and Receiver Adapters

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SENDER_RECEIVER_ADAPTERS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-007

DOC TITLE
Sender and Receiver Adapters

1. PURPOSE
- Sender adapters define inbound communication into the flow.
- Receiver adapters define outbound delivery to the target.

2. SCOPE
- Primary source scope: Sender and Receiver Adapters and closely related SAP Help pages.
- Chunking hint: source; sender adapter; flow logic; receiver adapter.
- Preferred retrieval anchors: sender and receiver adapters, source, sender adapter, flow logic, sender.

3. KEY TERMS
- Source
- Sender Adapter
- Flow Logic
- Receiver Adapter
- Target

4. CORE EXPLANATION
- Use the sender side to define how a message is accepted: trigger style, address or endpoint, protocol expectations, and security model.
- Sender configuration should be precise enough to avoid over-collecting data or exposing overly broad entry points.
- Use the receiver side to define where the processed message goes and under which protocol or authentication rules.
- Receiver configuration should align with the target interface contract and expected response pattern.
- Protocol fit: does the adapter match the interface contract?

5. OPERATIONAL RELEVANCE
- Choosing an adapter only because it is familiar.
- Using broad file or message selectors that collect unintended inputs.
- Treating adapter configuration as isolated from security and monitoring.
- Representative question forms:
- What is the intended use of sender and receiver adapters in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for sender and receiver adapters?
- What evidence and search anchors should be stored for sender and receiver adapters, source, sender adapter?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-007
- Related runbooks: RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, RB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_HTTP_AVAILABILITY_REQUEST_TIMEOUT_TIMEOUT_P1_v1.md, KB_RCMO_CPI_SECURITY_TLS_HANDSHAKE_FAILURE_P1_v1.md, KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration, https://help.sap.com/docs/integration-suite/sap-integration-suite/capabilities, https://help.sap.com/doc/978cdb2059244c10b55a8bd916484a63/CLOUD/en-US/b97b0ec26c871014bc6ce3c22a1e81b1.html, https://help.sap.com/docs/integration-suite/sap-integration-suite/what-is-sap-integration-suite
