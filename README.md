
# RCA-SAP-Cloud-Integration-MCP-Server

Remote MCP server with Python that connects to the SAP Cloud Integration APIs and exposes different tools

<img width="1662" height="931" alt="image" src="https://github.com/user-attachments/assets/0bc2f310-7929-49d7-89ca-f8d81e37045f" />

## Features in v 1.0

- Catalog packages
- Catalog iFlows
- Analyze iFlow
- Knowledge generation (.md)
- Generate DOCX documentation
- Evaluate Docs Compliance
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
