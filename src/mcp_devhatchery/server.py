from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import json, asyncio
from typing import AsyncIterator

from .auth import BearerAuthMiddleware
from .prepull import ensure_image_prepulled
from .events import BUS, Event
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(BearerAuthMiddleware)

    @app.on_event('startup')
    async def _startup():
        await ensure_image_prepulled()

    @app.get('/health')
    async def health(request: Request):
        # Report minimal auth-mode info expected by tests
        owner = getattr(getattr(request, 'state', None), 'owner', None)
        return {
            'status': 'ok',
            'auth_mode': settings.auth_mode,
            'owner': getattr(owner, 'owner', None),
        }

    @app.get('/events')
    async def events(request: Request):
        """Server-Sent Events: streams events from the in-memory EventBus.
        """
        queue: asyncio.Queue[Event] = asyncio.Queue()

        def sub(evt: Event):
            try:
                queue.put_nowait(evt)
            except Exception:
                pass

        BUS.subscribe(sub)

        async def gen() -> AsyncIterator[bytes]:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    evt = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    yield b':\n\n'
                    continue
                data = json.dumps({
                    'type': evt.type,
                    'owner': evt.owner,
                    'ts': evt.ts,
                    'data': evt.data,
                }).encode()
                yield b'data: ' + data + b'\n\n'
        return StreamingResponse(gen(), media_type='text/event-stream')

    return app


# Backward-compat export for uvicorn entrypoints
app = create_app()
