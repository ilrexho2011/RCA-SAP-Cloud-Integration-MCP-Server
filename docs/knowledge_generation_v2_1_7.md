# Knowledge generation and compliance assessment v2.1.7

This update introduces two main hardening themes:

1. KEDB and Runbook generation/update now align with the newer reference templates more closely.
2. A new MCP tool named `assess_ingestion_policy_compliance` evaluates the generated corpus under `exports/knowledge`.

## New knowledge-assessment tool

The new tool scans these generated document families:

- `kedb`
- `runbooks`
- `interface_catalogs`
- `official_docs`

It measures structural, quantitative, and qualitative retrieval-oriented indicators and exports:

- TXT report
- PDF report
- JSON metrics
- PNG charts

## Policy basis

The tool uses these packaged assets:

- `resources/policies/AI4BIZ_Knowledge_Ingestion_Guide.txt`
- `resources/policies/BM25_Runbook_Authoring_Guideline.txt`

Supplementary uploaded examples can be stored under:

- `resources/reference_materials/additional_samples/`

## Operational note

The compliance tool is read-only with respect to the knowledge corpus. It analyzes the generated outputs and writes a separate assessment package under `exports/compliance/<version>/`.
