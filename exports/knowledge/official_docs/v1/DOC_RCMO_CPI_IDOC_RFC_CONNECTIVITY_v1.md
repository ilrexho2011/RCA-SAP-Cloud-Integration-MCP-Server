# IDoc and RFC Connectivity - Overview

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "IDOC_RFC_CONNECTIVITY"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-025

DOC TITLE
IDoc and RFC Connectivity - Overview

1. PURPOSE
- This overview explains how Cloud Integration teams think about SAP backend connectivity when using IDoc and RFC patterns.
- The key design decisions are: which interface family (IDoc vs RFC), what endpoints/landscape assumptions apply, and how security materials and connectivity details are prepared.

2. SCOPE
- Primary source scope: IDoc and RFC Connectivity - Overview and closely related SAP Help pages.
- Chunking hint: sap connectivity choice (idoc/rfc); backend system context; auth & credentials; message contract.
- Preferred retrieval anchors: idoc and rfc connectivity - overview, sap connectivity choice (idoc/rfc), backend system context, auth & credentials, idoc.

3. KEY TERMS
- SAP connectivity
- choice (IDoc/RFC)
- Backend system
- context
- Auth & credentials
- Message contract
- Deploy
- Verify with evidence

4. CORE EXPLANATION
- IDoc (Intermediate Document) patterns are commonly used for structured message exchange between SAP systems where business documents are exchanged with clear semantic structures.
- Message structure: business documents mapped into IDoc segments and control records.
- Processing patterns: inbound/outbound handling aligned with SAP workflow and exchange configuration.
- Troubleshooting focus: contract alignment, partner settings, and evidence at the point of IDoc processing.
- RFC (Remote Function Call) patterns are used for invoking or integrating with SAP backend function interfaces, often where a service-like call model is suitable.

5. OPERATIONAL RELEVANCE
- Focusing only on integration flow logic while ignoring backend partner/function contract expectations.
- Treating connectivity/auth symptoms as generic runtime failures without evidence classification.
- Mixing environment context assumptions, leading to incorrect triage routing.
- Leaving runbooks without SAP connectivity gates, causing repeated first-failure investigations.
- Representative question forms:
- What is the intended use of this overview in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for this overview?
- What evidence and search anchors should be stored for idoc and rfc connectivity - overview, sap connectivity choice (idoc/rfc), backend system context?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-025
- Related runbooks: RB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, RB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, RB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md
- Related KEDB: KB_RCMO_CPI_SOAP_CONTRACT_FAULT_RAISED_P1_v1.md, KB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, KB_RCMO_CPI_SAP_IDOC_POSTING_CONFIGURATION_ERROR_P1_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
