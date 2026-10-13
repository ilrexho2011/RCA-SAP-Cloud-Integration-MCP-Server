# Knowledge Generation v2.1.6

- KEDB generation now considers `AI4BIZ_Enterprise_Error_Catalog_CPI.json`.
- New KEDB IDs start after the highest ID already found in existing KEDB markdown and enterprise catalog entries.
- New Runbooks are generated from the same filtered scenario set used for newly generated KEDBs.
- Filenames and cross-references avoid duplicated system prefixes such as `CPI_CPI_...`.
- Updated KEDB output normalizes `Updated at:` to the current date and normalizes the SAP Help note text.
- Bundled fallbacks are included for inventory ZIP, enterprise error catalog, ingestion-policy texts, and local MPL JSON corpora.
- OpenAI refinement remains optional and now includes ingestion-policy context.
