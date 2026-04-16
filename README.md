# RCA-SAP-Cloud-Integration-MCP-Server

Remote MCP server with Python that connects to the SAP Cloud Integration APIs and exposes different tools

## Features in v1.0

- Catalog packages
- Catalog iFlows
- Analyze iFlow
- Generate DOCX documentation
- Score iFlow quality

## Run locally (The first Terminal / Powershell)

```bash
cp .env.example .env
uv sync
uv run python -m app.main
```

## Connect with MCP Inspector (The second Terminal / Powershell)

```bash
npx -y @modelcontextprotocol/inspector
```

## Endpoint to be called

```bash
http://localhost:8000/mcp
```
