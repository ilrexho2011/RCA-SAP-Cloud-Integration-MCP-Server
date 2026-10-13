# Common Design Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "COMMON_DESIGN_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-033

DOC TITLE
Common Design Patterns

1. PURPOSE
- Design patterns help you build integration flows that are easier to understand, test, operate, and troubleshoot.
- Patterns encode proven choices: how you route, mediate payloads, manage asynchronous behavior, and handle errors consistently.

2. SCOPE
- Primary source scope: Common Design Patterns and closely related SAP Help pages.
- Chunking hint: pattern intent; typical flow shape; failure categories; evidence to capture.
- Preferred retrieval anchors: common design patterns, pattern intent, typical flow shape, failure categories, patterns.

3. KEY TERMS
- Pattern intent
- Typical flow shape
- Failure categories
- Evidence to capture
- Fix verification

4. CORE EXPLANATION
- Request-reply patterns: orchestrate a call and then validate/transform the reply into the expected downstream model.
- Asynchronous processing: decouple execution with polling/queuing-style behaviors so you can manage retries and failure visibility.
- Polling and batch-style integration: handle file or message availability using robust lifecycle and idempotency expectations.
- Content mediation: standardize payload shapes using transformation and mapping boundaries so downstream steps are stable.
- Error handling patterns: centralize exception mapping, retry/fallback logic, and standardized error payloads.

5. OPERATIONAL RELEVANCE
- Selecting patterns without matching the runtime behavior (sync vs async mismatch).
- Ignoring idempotency and replay behavior in polling/batch scenarios.
- Using generic error handling that hides which pattern boundary failed.
- Changing only one side of a mediation boundary without updating downstream assumptions.
- Representative question forms:
- What is the intended use of common design patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for common design patterns?
- What evidence and search anchors should be stored for common design patterns, pattern intent, typical flow shape?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-033
- Related runbooks: RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, RB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related KEDB: KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, KB_RCMO_CPI_INTEGRATION_STATE_CONFLICT_409_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode, IR16_IF01_Northwind_Orders_via_OrderID_in_Payload_using_Variable
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
