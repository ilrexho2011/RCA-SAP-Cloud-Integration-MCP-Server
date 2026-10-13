# Cloud Integration Runtime

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "CLOUD_INTEGRATION_RUNTIME"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-016

DOC TITLE
Cloud Integration Runtime

1. PURPOSE
- Runtime is where integration flows actually execute, where messages are processed, tracked, retried, and diagnosed.
- A correct mental model connects design-time artifacts to runtime behavior: what gets executed, where evidence is stored, and how failures are represented.

2. SCOPE
- Primary source scope: Cloud Integration Runtime and closely related SAP Help pages.
- Chunking hint: build-time artifact; runtime execution; message processing; monitoring visibility.
- Preferred retrieval anchors: cloud integration runtime, build-time artifact, runtime execution, message processing, runtime.

3. KEY TERMS
- Build-time artifact
- Runtime execution
- Message processing
- Monitoring visibility
- Failure evidence
- Support actions

4. CORE EXPLANATION
- In practice, runtime is the bridge between your integration flow design and what operations observe. When something happens (success or failure), the runtime provides the traceability surface: message states, processing timelines, log/trace artifacts, and the operational signals needed for triage. Therefore, runtime understanding affects how teams troubleshoot, how they confirm fixes, and how they validate deployments.
- Execution context: Which runtime component executes the flow and how requests are handled in sequence or parallelism.
- Message states: How the platform records processing stages so you can interpret “where it stopped”.
- Evidence and observability: What traces/logs/monitoring entries are available for investigation.
- Retry and failure behavior: How transient issues are represented and what patterns you should expect during recovery.

5. OPERATIONAL RELEVANCE
- Assuming that design-time correctness guarantees runtime correctness without verifying runtime observability and failure patterns.
- Misreading monitoring states and drawing conclusions without checking trace or supporting evidence.
- Treating every failure as a mapping problem instead of considering retry behavior, execution context, and runtime lifecycle effects.
- Using the wrong environment assumptions when interpreting runtime evidence (Cloud Foundry vs Neo context).
- Representative question forms:
- What is the intended use of cloud integration runtime in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for cloud integration runtime?
- What evidence and search anchors should be stored for cloud integration runtime, build-time artifact, runtime execution?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-016
- Related runbooks: RB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, RB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, RB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md
- Related KEDB: KB_RCMO_CPI_NETWORK_DNS_HOST_RESOLUTION_FAILED_P1_v1.md, KB_RCMO_CPI_DB_DATA_DUPLICATE_KEY_DETECTED_P1_v1.md, KB_RCMO_CPI_DB_CONNECTIVITY_JDBC_CONNECTION_FAILED_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md
- Related catalog objects: IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP, IR11_IF08_Exercise03_Reusable_Message_Mapping_Artifacts_and_Error_Handling_1, IR27_IF03_Dynamic_Process_Football_OData_Scores
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/sap-cloud-integration
