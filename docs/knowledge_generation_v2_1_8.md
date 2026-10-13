# Knowledge and compliance generation v2.1.8

This release hardens the ingestion-policy compliance layer with a more professional KEDB/Runbook assessment package.

## What changed

1. `assess_ingestion_policy_compliance` now generates a professional Word report that mirrors the enterprise compliance example more closely.
2. The report includes:
   - overall compliance score table
   - inventory and composite score table
   - primary-ingestion compliance matrix
   - BM25 supplemental assessment matrix
   - quantitative indicator table
   - five chart outputs matching the assessment structure
3. The tool now also generates a dedicated remediation text package based on the packaged strict-ingestion remediation example.
4. MCP clients receive an on-screen markdown summary with the main compliance table and chart paths.
5. The packaged additional reference materials were refreshed for the compliance examples.
