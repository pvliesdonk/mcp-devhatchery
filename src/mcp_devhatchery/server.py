from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import settings
from .auth import BearerAuthMiddleware
from .prepull import prepull_images
import asyncio


# NOTE: This file still avoids implementing MCP mechanics.
# Adds auth middleware and kicks off a background prepull task.


def create_app() -> FastAPI:
    app = FastAPI(title="mcp-devhatchery", version="0.0.0")
    app.add_middleware(BearerAuthMiddleware)

    @app.on_event('startup')
    async def _startup():
        # fire-and-forget prepull
        asyncio.create_task(prepull_images())

    @app.get('/health')
    def health():
        return JSONResponse({
            'status': 'ok',
            'default_image': settings.default_image,
            'export_root': settings.export_root,
            'auth_mode': settings.auth_mode,
        })

    return app
