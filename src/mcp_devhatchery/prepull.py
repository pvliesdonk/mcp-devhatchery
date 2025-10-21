'''
Image pre-pull helper and ensure helper used by server startup.
'''
from __future__ import annotations

import asyncio, json
from typing import List
try:
    import docker  # type: ignore
except Exception:  # pragma: no cover
    docker = None
from .config import settings

async def prepull_images() -> None:
    client = docker.from_env() if docker else None
    try:
        imgs: List[str] = json.loads(settings.prepull_images)
    except Exception:
        imgs = [settings.default_image]
    for img in imgs:
        try:
            if client:
                await asyncio.to_thread(client.images.pull, img)
        except Exception:
            pass
    if client:
        client.close()

async def ensure_image_prepulled() -> None:
    # fire-and-forget pre-pull at startup
    try:
        await prepull_images()
    except Exception:
        pass
