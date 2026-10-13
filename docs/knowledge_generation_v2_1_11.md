# Knowledge Generation v2.1.11

## Purpose

This patch hardens KEDB and Runbook generation for tenants where direct entity reads on `IntegrationDesigntimeArtifacts` return `501 Not Implemented`.

## Key fixes

- Reuse package-scoped iFlow list items during scenario derivation.
- Avoid tenant-wide rediscovery when the user already selected a package.
- Cache unsupported entity-read capability after the first `501` response.
- Cache package and package-iFlow lists in the SAP client for the lifetime of the process.
- Apply safe fallback sections during KEDB and Runbook rendering when OpenAI refinement omits expected keys.

## Operational note

For long runs in MCP Inspector, set `Maximum Total Timeout` to the same value as `Request Timeout`.
