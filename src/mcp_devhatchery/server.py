'''
Minimal FastAPI app used as a host for the MCP Streamable-HTTP server.

M1 provides:
- /health endpoint (smoke)
- Bearer auth middleware
- Startup hook launching image pre-pull task

Future PRs will mount the MCP routes and SSE/event streaming.
'''
from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import settings
from .auth import BearerAuthMiddleware
from .prepull import prepull_images
import asyncio


def create_app() -> FastAPI:
    '''Create and configure the FastAPI application instance.

    Returns:
        FastAPI: a configured app with auth + startup hooks.
    '''
    app = FastAPI(title='mcp-devhatchery', version='0.0.0')
    app.add_middleware(BearerAuthMiddleware)

    @app.on_event('startup')
    async def _startup():
        # Fire-and-forget pre-pull. Failures are non-fatal.
        asyncio.create_task(prepull_images())

    @app.get('/health')
    def health():
        '''Simple health probe used by CI and container orchestrators.
        Returns static config so we can sanity-check env parsing.
        '''
        return JSONResponse({
            'status': 'ok',
            'default_image': settings.default_image,
            'export_root': settings.export_root,
            'auth_mode': settings.auth_mode,
        })

    return app
