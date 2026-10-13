# Licensed Capabilities and Features

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "LICENSED_CAPABILITIES_AND_FEATURES"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-010

DOC TITLE
Licensed Capabilities and Features

1. PURPOSE
- Not every capability is simply “there by default”; practical availability depends on the licensed scope and the tenant context in which Cloud Integration is consumed.
- This topic matters because design assumptions, rollout planning, and operational expectations can fail when teams confuse documented platform features with licensed entitlement.

2. SCOPE
- Primary source scope: Licensed Capabilities and Features and closely related SAP Help pages.
- Chunking hint: documented capability; licensed entitlement; tenant enablement; project usage.
- Preferred retrieval anchors: licensed capabilities and features, documented capability, licensed entitlement, tenant enablement, licensed.

3. KEY TERMS
- Documented capability
- Licensed entitlement
- Tenant enablement
- Project usage

4. CORE EXPLANATION
- In Cloud Integration projects, feature understanding is not enough on its own. A team may design a solution assuming a specific runtime, connector, operational feature, or surrounding service is available, but the real project boundary is often determined by licensing and tenant setup. That is why this topic belongs early in the corpus: it reduces avoidable rework and unrealistic design assumptions.
- Capabilities are documented broadly: SAP Help usually describes what the product area can do from a functional perspective.
- Licensed scope narrows usage: What your team can adopt in a real tenant depends on the subscribed landscape and contractual scope.
- Enabled features shape implementation: Even when something is theoretically part of a capability family, rollout readiness still depends on tenant activation, environment, and lifecycle stage.
- Architecture decisions should reflect entitlement reality: Avoid designing dependencies on features that the target subscription or tenant model does not actually support.

5. OPERATIONAL RELEVANCE
- Confusing product marketing breadth with the exact features available to a specific customer tenant.
- Assuming that if a feature appears in SAP Help, it is automatically licensed and ready for immediate project use.
- Building architecture decisions around trial observations without validating productive subscription scope.
- Letting licensing questions surface late, after interface design or build work has already started. How to use this in the corpus
- Representative question forms:
- What is the intended use of licensed capabilities and features in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for licensed capabilities and features?
- What evidence and search anchors should be stored for licensed capabilities and features, documented capability, licensed entitlement?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-010
- Related runbooks: RB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, RB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, RB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P3_v1.md, RB_RCMO_CPI_SAP_XI_ACK_DELAY_WARNING_P3_v1.md
- Related KEDB: KB_RCMO_CPI_HTTP_AUTHORIZATION_FORBIDDEN_403_P1_v1.md, KB_RCMO_CPI_SAP_XI_CHANNEL_CONFIGURATION_ERROR_P1_v1.md, KB_RCMO_CPI_MPL_OBSERVABILITY_ERROR_DETAILS_MISSING_P3_v1.md, KB_RCMO_CPI_SAP_XI_ACK_DELAY_WARNING_P3_v1.md
- Related catalog objects: IR01_IF06_Test_SMS_Message, IR16_IF01_Northwind_Orders_via_OrderID_in_Payload_using_Variable
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
