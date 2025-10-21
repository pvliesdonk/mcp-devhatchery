# ADR-0001: Transport & Runtime

**Status:** Proposed

- **Decision:** Use Streamable-HTTP transport per MCP spec, **FastMCP 2** for server framework, and **uv** for package/runtime management.
- **Consequences:** Minimal protocol boilerplate; easy streaming; fast reproducible envs.
- **Alternatives:** SSE-only transport; raw ASGI without framework; pip/venv.
