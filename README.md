# RCA-SAP-Cloud-Integration-MCP-Server
Remote MCP server with Python that connects to the SAP Cloud Integration APIs and exposes different tools

## Features in v0.1
- Catalog packages
- Catalog iFlows
- Analyze iFlow
- Generate DOCX documentation
- Score iFlow quality

## Run locally
```bash
cp .env.example .env
uv sync
uv run python -m app.main
