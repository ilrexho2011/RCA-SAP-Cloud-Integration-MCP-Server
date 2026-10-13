# Process Direct and Internal Patterns

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "PROCESS_DIRECT_INTERNAL_PATTERNS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-026

DOC TITLE
Process Direct and Internal Patterns

1. PURPOSE
- Process Direct patterns enable modular internal communication between integration artifacts in the same runtime context.
- Instead of repeating logic, teams design reusable “internal entry points” and call them from flows, improving maintainability and governance.

2. SCOPE
- Primary source scope: Process Direct and Internal Patterns and closely related SAP Help pages.
- Chunking hint: modularization goal; internal entry point; call pattern; payload/context passing.
- Preferred retrieval anchors: process direct and internal patterns, modularization goal, internal entry point, call pattern, process.

3. KEY TERMS
- Modularization goal
- internal entry point
- call pattern
- payload/context
- passing
- error strategy
- deploy & trace

4. CORE EXPLANATION
- Internal patterns are architectural choices that help teams structure integration content as a maintainable system. They address repeated transformations, repeated validation logic, and the need for consistent error handling and operational visibility across multiple flows.
- Reuse: centralize shared logic so changes happen once.
- Separation of concerns: keep orchestration flows cleaner and push business logic into dedicated internal components.
- Governance: standardize how internal calls are traced and how errors are surfaced.
- When multiple integration flows need the same processing step set (mapping/validation/transformation blocks).

5. OPERATIONAL RELEVANCE
- Over-splitting logic into internal calls, creating deep call chains that are hard to reason about.
- Passing incompatible payload shapes between internal components.
- Inconsistent error propagation rules, leading to confusing incident categorization.
- Updating internal shared logic without verifying all dependent flows.
- Representative question forms:
- What is the intended use of process direct and internal patterns in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for process direct and internal patterns?
- What evidence and search anchors should be stored for process direct and internal patterns, modularization goal, internal entry point?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-026
- Related runbooks: RB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, RB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P2_v1.md
- Related KEDB: KB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P1_v1.md, KB_RCMO_CPI_DOWNSTREAM_SERVER_INTERNAL_ERROR_500_P2_v1.md
- Related catalog objects: IR01_IF07_Test_Email_with_OAuth2_Code, IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP, IR06_IF04_SFTP_Poll_Enrich_Multiple_File_and_Delete, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
