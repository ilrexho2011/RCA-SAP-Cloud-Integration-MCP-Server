# RCA-SAP-Cloud-Integration-MCP-Server
Remote MCP server with Python that connects to the SAP Cloud Integration APIs and exposes different tools

## Features in v0.1
- Catalog packages
- Catalog iFlows
- Analyze iFlow
- Generate DOCX documentation
- Score iFlow quality

## Run locally (Terminal / Powershell)
```bash
cp .env.example .env
uv sync
uv run python -m app.main
```
## Connect with MCP Inspector (Terminal / Powershell)
```bash
npx -y @modelcontextprotocol/inspector
```
## Endpoint
```bash
http://localhost:8000/mcp
```
