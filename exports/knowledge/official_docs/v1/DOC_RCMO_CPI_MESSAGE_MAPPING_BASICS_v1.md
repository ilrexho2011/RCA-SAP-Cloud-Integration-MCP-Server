# Message Mapping Basics

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "MESSAGE_MAPPING_BASICS"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-045

DOC TITLE
Message Mapping Basics

1. PURPOSE
- Message Mapping is the main graphical transformation mechanism for aligning source and target message structures.
- It becomes operationally important whenever source values are missing, data types do not align, or the target contract is stricter than expected.

2. SCOPE
- Primary source scope: Message Mapping Basics and closely related SAP Help pages.
- Chunking hint: read source and target structures; map required fields; apply standard/custom functions; test representative payload.
- Preferred retrieval anchors: message mapping basics, read source and target structures, map required fields, apply standard/custom functions.

3. KEY TERMS
- Read source and target
- structures
- Map required fields
- Apply standard/custom
- functions
- Test representative
- payload
- Deploy with clear
- assumptions Why thi…

4. CORE EXPLANATION
- SAP Help frames message mapping as the place to handle mappings and mapping functions. In support work, mapping is where business payload reality meets target contract strictness. Many defects that surface as HTTP 400, OData bad request, or receiver validation errors were actually introduced earlier in mapping design.
- Source-target contract alignment is the real core of mapping, not only line-to-line field connection.
- Mandatory values and datatype conversion need explicit treatment, not optimistic assumptions.
- Custom functions increase flexibility but can also reduce transparency if overused.
- A mapping issue often surfaces downstream and must be traced back to transformation logic.

5. OPERATIONAL RELEVANCE
- Treating mapping like a purely technical field-connection exercise and ignoring business rules.
- Letting custom functions hide simple logic that should stay visible and testable.
- Testing only the happy-path payload and not edge cases like missing or malformed values.
- Classifying receiver rejections as transport failures instead of contract-transformation failures.
- Representative question forms:
- What is the intended use of message mapping basics in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for message mapping basics?
- What evidence and search anchors should be stored for message mapping basics, read source and target structures, map required fields?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-045
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, RB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, RB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_PAYLOAD_XML_PARSE_FAILURE_P1_v1.md, KB_RCMO_CPI_SCRIPT_GROOVY_TEST_EXCEPTION_RAISED_P1_v1.md, KB_RCMO_CPI_ODATA_PAYLOAD_BAD_REQUEST_400_P2_v1.md
- Related catalog objects: IR16_IF01_Northwind_Orders_via_OrderID_in_Payload_using_Variable
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/message-mapping-guidelines-basics, https://help.sap.com/docs/integration-suite/sap-integration-suite/creating-message-mapping-as-flow-step, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/creating-custom-mapping, https://help.sap.com/docs/integration-suite/sap-integration-suite/defining-standard-message-mapping
