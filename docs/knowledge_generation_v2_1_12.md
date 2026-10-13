# Knowledge generation v2.1.12

- Stops package-scoped KEDB/Runbook generation from calling global package discovery just to resolve package names.
- Fills fallback metadata from the actual scenario context when interface catalog matching is unavailable.
- Removes escaped underscore artifacts from generated KEDB and Runbook markdown output.
- Changes MCP tool defaults so an unchecked `use_mpl` toggle behaves as disabled in Inspector-driven runs.
