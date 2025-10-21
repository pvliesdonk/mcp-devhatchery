# Clients: Connect

Example mcpjungle seed:

```json
{
  "name": "mcp-devhatchery",
  "transport": "http",
  "description": "Spawn-on-demand dev containers; shell + filesystem + exports.",
  "url": "http://localhost:8080/servers/devhatchery",
  "env": { "MCP_PROTOCOL_VERSION": "2025-03-26" },
  "headers": { "Authorization": "Bearer <token>" }
}
```

Roots example:

```json
{
  "roots": [
    "file:///work",
    "file:///export"
  ]
}
```
