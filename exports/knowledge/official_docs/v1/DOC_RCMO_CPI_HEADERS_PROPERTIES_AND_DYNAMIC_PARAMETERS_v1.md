# Headers, Exchange Properties, and Dynamic Parameters

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "HEADERS_PROPERTIES_AND_DYNAMIC_PARAMETERS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-048

DOC TITLE
Headers, Exchange Properties, and Dynamic Parameters

1. PURPOSE
- Headers, exchange properties, and dynamic parameters form the hidden control plane of many integration flows.
- They influence routing, authentication, endpoint behavior, pagination, and downstream interpretation without always changing the visible payload.

2. SCOPE
- Primary source scope: Headers, Exchange Properties, and Dynamic Parameters and closely related SAP Help pages.
- Chunking hint: identify controlling runtime value; locate where it is written/read; confirm scope and lifetime.
- Preferred retrieval anchors: headers, exchange properties, and dynamic parameters, identify controlling runtime value, locate where it is written/read, confirm scope and lifetime, headers.

3. KEY TERMS
- Identify controlling
- runtime value
- Locate where it is
- written/read
- Confirm scope and
- lifetime

4. CORE EXPLANATION
- SAP Help offers dedicated documentation both for framework-provided headers/properties and for dynamic parameterization. That is operationally important because a large class of incidents is caused by invisible context: not the business payload itself, but the runtime state attached to it.
- Visibility gap: runtime context may drive behavior even when the payload looks unchanged.
- Scope matters: some values are meant for internal processing, others are part of transport semantics.
- Dynamic parameters increase flexibility, but they also increase ambiguity if governance is weak.
- Control values should be documented like interfaces, not treated as incidental implementation details.

5. OPERATIONAL RELEVANCE
- Changing context values without documenting who relies on them later.
- Using similar header/property names for different purposes and creating ambiguity.
- Treating a dynamic parameter as stable although its source value is volatile.
- Ignoring runtime context comparison when payload comparison shows no obvious difference.
- Representative question forms:
- What is the intended use of headers, exchange properties, and dynamic parameters in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for headers, exchange properties, and dynamic parameters?
- What evidence and search anchors should be stored for headers, exchange properties, and dynamic parameters, identify controlling runtime value, locate where it is written/read?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-048
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHENTICATION_UNAUTHORIZED_401_P1_v1.md, KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/headers-and-exchange-properties-provided-by-integration-framework, https://help.sap.com/docs/integration-suite/sap-integration-suite/read-and-modify-message-header-message-body-and-exchange-properties, https://help.sap.com/docs/integration-suite/sap-integration-suite/dynamically-configure-integration-flow-parameters, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/externalize-parameters-of-integration-flow
