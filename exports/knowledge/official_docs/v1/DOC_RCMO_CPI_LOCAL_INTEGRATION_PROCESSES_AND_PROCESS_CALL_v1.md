# Local Integration Processes and Process Call

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "LOCAL_INTEGRATION_PROCESSES_AND_PROCESS_CALL"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-043

DOC TITLE
Local Integration Processes and Process Call

1. PURPOSE
- A local integration process is a contained subprocess used to decompose a complex integration flow into smaller parts.
- Process Call is the handoff mechanism from the main process to that contained logic; ProcessDirect extends the idea across dependent flows.

2. SCOPE
- Primary source scope: Local Integration Processes and Process Call and closely related SAP Help pages.
- Chunking hint: main flow decides task; call local process or dependent flow; execute contained logic; return result or escalate exception why this topic matters in daily work.
- Preferred retrieval anchors: local integration processes and process call, main flow decides task, call local process or dependent flow, execute contained logic, local processes and process call.

3. KEY TERMS
- Main flow decides task
- Call local process or
- dependent flow
- Execute contained
- logic
- Return result or
- escalate exception W…

4. CORE EXPLANATION
- result or escalate exception SAP Help positions the local integration process as a container for a separate subprocess and ProcessDirect as a fast direct communication path between flows. In operational terms, this is where modularity meets dependency management: when a consumer is missing, inactive, or handling errors poorly, the issue may sit at the process boundary rather than in business logic itself.
- Modularity improves readability and reuse, but it introduces explicit call boundaries that must be observable.
- A local process and a dependent flow are not the same operationally, even if they solve similar decomposition goals.
- Exception semantics across process boundaries should be designed, not assumed.
- Consumer availability and activation state become first-class support checks in ProcessDirect-heavy designs.

5. OPERATIONAL RELEVANCE
- Treating a process call boundary like an invisible implementation detail.
- Not documenting which flow owns the callee responsibility.
- Allowing exceptions to propagate across dependent flows without deliberate handling strategy.
- Assuming modularity automatically improves supportability without explicit evidence points.
- Representative question forms:
- What is the intended use of local integration processes and process call in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for local integration processes and process call?
- What evidence and search anchors should be stored for local integration processes and process call, main flow decides task, call local process or dependent flow?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-043
- Related runbooks: RB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, RB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, RB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, RB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related KEDB: KB_RCMO_CPI_CPI_PROCESSDIRECT_CONSUMER_MISSING_P1_v1.md, KB_RCMO_CPI_FLOW_SPLITTER_PATH_RESOLUTION_FAILED_P2_v1.md, KB_RCMO_CPI_FLOW_GATHER_CORRELATION_INCOMPLETE_P2_v1.md, KB_RCMO_CPI_FLOW_ROUTER_CONDITION_NO_MATCH_P3_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/define-local-integration-process, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/handle-exceptions-in-dependent-integration-flows, https://help.sap.com/docs/integration-suite/sap-integration-suite/processdirect-adapter
