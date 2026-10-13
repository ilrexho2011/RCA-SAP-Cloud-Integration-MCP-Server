# Knowledge Generation v2.1.3 Production Hardening

## Scope
This version hardens the tenant-wide knowledge generation layer with four additions:

1. MPL runtime enrichment
2. Interactive version elicitation
3. ZIP input handling for update tools
4. Combined knowledge-output package export

## MPL semantic coverage
The service `app/services/mpl_semantic_coverage_service.py` collects failed-message evidence from:
- live SAP CPI Message Processing Logs through the SAP client
- optional local JSON MPL corpora through `MPL_LOCAL_JSON_DIR`

The runtime signatures are merged into generated KEDB and Runbooks to improve:
- error-family precision
- example error text coverage
- MessageGuid evidence preservation
- last-seen and occurrence metadata

## Interactive version selection
If a knowledge-generation tool is called without `version`, the tool attempts MCP form-mode elicitation.
If the client does not support elicitation, the caller must pass the version explicitly.

## ZIP input handling
The following tools now accept ZIP paths directly:
- `update_kedb_documents(source_zip_path=...)`
- `update_runbook_documents(source_zip_path=...)`
- `generate_knowledge_output_bundle(kedb_zip_path=..., runbook_zip_path=...)`

ZIP files are extracted to `KNOWLEDGE_STAGING_DIR`.

## Combined bundle export
`generate_knowledge_output_bundle` creates a consolidated folder and ZIP archive that can contain:
- interface catalogs
- generated KEDB
- generated Runbooks
- updated KEDB corpus
- updated Runbook corpus
- manifest JSON


## Interface catalog post-processing layer
The service `app/services/interface_catalog_formatter.py` is applied after interface catalog markdown is generated.
It normalizes indentation, converts numbered-section bullets to `*`, preserves the approved section order, and removes noisy generation lines that are not part of the reference format.
