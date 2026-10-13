# Overview of Integration Flow Editor

environment: "demo"
customer_id: "RCMO"
system_id: "CPI-RCMO"
sap_sid: "CPI"
artifact_type: "documentation"
object_name: "OVERVIEW_OF_INTEGRATION_FLOW_EDITOR"
priority: "P3"
interface_id: "N/A"
integration_flow_id: "N/A"
integration_flow_name: "N/A"
package_name: "SAP Help Derivative Docs"
review_cycle: "monthly"

DOC ID
SAP-CI-038

DOC TITLE
Overview of Integration Flow Editor

1. PURPOSE
- The integration flow editor is the design cockpit where structure, routing, transformation, and adapter configuration come together.
- Its value for RAG is not UI description alone, but faster localization of where a configuration error probably lives.

2. SCOPE
- Primary source scope: Overview of Integration Flow Editor and closely related SAP Help pages.
- Chunking hint: palette; drop shape; configure properties; link resources.
- Preferred retrieval anchors: overview of integration flow editor, palette, drop shape, configure properties, overview of flow editor.

3. KEY TERMS
- Palette
- Drop shape
- Configure properties
- Link resources
- Validate flow
- readability
- Deploy and inspect
- runtime result Why th…

4. CORE EXPLANATION
- and inspect runtime result SAP Help frames the editor as the environment for efficient iFlow development. In a knowledge base, that makes it valuable as a “where to look” guide: when a route, script, mapping, or resource reference fails, support needs a mental map of where that configuration typically resides in the editor.
- Canvas structure: sequence, subprocesses, and branching logic define control flow before any payload detail is inspected.
- Shape-level configuration: a large share of defects come from one shape whose properties were incomplete or inconsistent.
- Resource linkage: scripts, mappings, and supporting artifacts may exist, but not be wired correctly into the flow step.
- Editor readability matters operationally: unclear naming and structure slow incident diagnosis later.

5. OPERATIONAL RELEVANCE
- Investigating a runtime symptom without first identifying the relevant design shape.
- Assuming the resource is broken when the actual issue is missing linkage from the editor step.
- Using unclear names for branches or local processes, which weakens support evidence.
- Treating editor layout as cosmetic instead of operationally important for triage speed.
- Representative question forms:
- What is the intended use of this overview in SAP Cloud Integration?
- Which prerequisites or restrictions should be retained for this overview?
- What evidence and search anchors should be stored for overview of integration flow editor, palette, drop shape?

6. RELATED ARTIFACTS
- Source doc ID: SAP-CI-038
- Related runbooks: RB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, RB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, RB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, RB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md
- Related KEDB: KB_RCMO_CPI_SCRIPT_GROOVY_NULL_REFERENCE_DETECTED_P1_v1.md, KB_RCMO_CPI_RUNTIME_RESOURCE_NOT_FOUND_404_P1_v1.md, KB_RCMO_CPI_MAPPING_SOURCE_MANDATORY_VALUE_MISSING_P2_v1.md, KB_RCMO_CPI_MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED_P2_v1.md
- Related catalog objects: IR01_IF00_Global_Variables, IR01_IF13_Fetching_Failed_Iflow_Error_Messages_Text_AI4BIZ_MVP, IR12_IF03_MM_CategoryFlat_to_CategoryFlat_Conditional_IF_FilterByStatusCode
- Source URL: https://help.sap.com/docs/cloud-integration/sap-cloud-integration/overview-of-integration-flow-editor, https://help.sap.com/docs/cloud-integration/sap-cloud-integration/configure-integration-flow-components
