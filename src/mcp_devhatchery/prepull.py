'''
Image pre-pull helper.

On startup, we pre-pull DEFAULT_IMAGE and any images listed in PREPULL_IMAGES.
This is a best-effort optimization; failures are swallowed to avoid blocking boot.
'''
from __future__ import annotations

import asyncio
from typing import List
import json
import docker
from .config import settings


async def prepull_images() -> None:
    '''
    Pull images listed in settings.prepull_images (JSON array) asynchronously.

    Uses asyncio.to_thread to run blocking Docker SDK calls without stalling the loop.
    '''
    client = docker.from_env()
    try:
        imgs: List[str] = json.loads(settings.prepull_images)
    except Exception:
        imgs = [settings.default_image]
    for img in imgs:
        try:
            await asyncio.to_thread(client.images.pull, img)
        except Exception:
            # Best-effort: structured logging will land with observability work.
            pass
    client.close()
