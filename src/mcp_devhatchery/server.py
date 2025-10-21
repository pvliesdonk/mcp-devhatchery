from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import settings

# NOTE: This file intentionally avoids implementing MCP mechanics yet.
# It provides a health endpoint and placeholders where the Streamable-HTTP MCP
# server will be mounted in subsequent branches.


def create_app() -> FastAPI:
    app = FastAPI(title="mcp-devhatchery", version="0.0.0")

    @app.get('/health')
    def health():
        return JSONResponse({
            'status': 'ok',
            'default_image': settings.default_image,
            'export_root': settings.export_root,
        })

    # TODO(m1): Mount MCP Streamable-HTTP server here (FastMCP 2 integration).
    # TODO(m1): Add SSE endpoint (if separate) for readiness/event streaming.

    return app
