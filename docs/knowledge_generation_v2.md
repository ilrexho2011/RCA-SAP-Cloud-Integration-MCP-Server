# Knowledge Generation v2

This package extends the original five MCP tools with five knowledge-oriented tools:

1. `generate_interface_catalogs`
2. `generate_kedb_documents`
3. `generate_runbook_documents`
4. `update_kedb_documents`
5. `update_runbook_documents`

## Why version is mandatory
Each of the five tools requires an explicit `version` argument. This enforces operator control over generated knowledge artifacts such as `v1`, `v2`, or `v3`.

## Output conventions
- Interface catalogs are emitted as `DOC_<CUSTOMER>_<SAP_SID>_<OBJECT>_<VERSION>.md`
- KEDB documents are emitted as `KB_<CUSTOMER>_<SAP_SID>_<OBJECT>_<PRIORITY>_<VERSION>.md`
- Runbooks are emitted as `RB_<CUSTOMER>_<SAP_SID>_<OBJECT>_<PRIORITY>_<VERSION>.md`

## Output directories
By default, the service writes to:
- `./exports/knowledge/interface_catalogs/<version>/`
- `./exports/knowledge/kedb/<version>/`
- `./exports/knowledge/runbooks/<version>/`
- `./exports/knowledge/kedb_updated/<version>/`
- `./exports/knowledge/runbooks_updated/<version>/`

Each directory is also zipped automatically.
