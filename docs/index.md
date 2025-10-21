# mcp-devhatchery

Streamable-HTTP MCP server that hatches per-user dev containers with unrestricted shells, persistent workspaces, and dual export paths. Built on FastMCP 2 + uv.

- Default image: **ubuntu:24.04**
- Persistence: named volume at `/work` (transient tmpfs optional)
- Exports: control-plane `EXPORT_ROOT` (tar.zst/dir) and runner publish mount (`/export`)
- Auth ladder: none → Bearer → OIDC/PKCE (Authelia)
- Roots respected; files exposed as **Resources** (with templates)

Start at **Design → Requirements** for scope and constraints.
