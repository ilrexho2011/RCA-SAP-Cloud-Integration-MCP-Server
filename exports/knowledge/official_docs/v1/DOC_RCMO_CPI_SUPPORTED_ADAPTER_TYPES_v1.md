# Supported Adapter Types - Overview

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "SUPPORTED_ADAPTER_TYPES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-008

DOC TITLE
Supported Adapter Types - Overview

1. PURPOSE
- Adapter selection usually follows the interface style: HTTP-based, file-based, service-based, SAP-specific, or internal pattern.
- The same business scenario can often be solved in multiple ways, but the adapter determines many downstream choices.

2. SCOPE
- Primary source scope: Supported Adapter Types - Overview and closely related SAP Help pages.
- Chunking hint: supported adapter types - overview; supported; types.
- Preferred retrieval anchors: supported adapter types - overview, supported, types.

3. KEY TERMS
- Supported Adapter
- Types - Overview
- Supported
- Types

4. CORE EXPLANATION
- HTTP | SOAP | OData | SFTP | SAP
- HTTP or HTTPS: practical for API-style integration and lightweight service exposure.
- SOAP: common in service contracts where WSDL-style interface definitions are relevant.
- OData: useful when integration is centered on resource or entity operations.
- SFTP or SSH-based file transfer: common in batch, polling, and file-exchange scenarios.

5. OPERATIONAL RELEVANCE
- Treating this overview as a substitute for adapter-specific configuration docs.
- Assuming all adapters behave the same operationally.
- Ignoring target-side constraints when selecting the protocol.
- Representative question forms:
- What is the intended use of this overview in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for this overview?
- What evidence and search anchors should be stored for supported adapter types - overview, supported, types?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-008
- Related runbooks: RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_ODATA_SERVICE_NOT_FOUND_404_P2_v1.md, RB_RCMO_CPI_SFTP_FILE_PATH_NOT_FOUND_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_ODATA_SERVICE_NOT_FOUND_404_P2_v1.md, KB_RCMO_CPI_SFTP_FILE_PATH_NOT_FOUND_P2_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration, https://help.sap.com/docs/integration-suite/sap-integration-suite/capabilities, https://help.sap.com/doc/978cdb2059244c10b55a8bd916484a63/CLOUD/en-US/b97b0ec26c871014bc6ce3c22a1e81b1.html, https://help.sap.com/docs/integration-suite/sap-integration-suite/what-is-sap-integration-suite
