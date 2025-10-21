from __future__ import annotations

import asyncio
from typing import List
import json
import docker
from .config import settings

async def prepull_images() -> None:
    client = docker.from_env()
    try:
        imgs: List[str] = json.loads(settings.prepull_images)
    except Exception:
        imgs = [settings.default_image]
    for img in imgs:
        try:
            # pull synchronously in a thread to avoid blocking loop
            await asyncio.to_thread(client.images.pull, img)
        except Exception:
            # best-effort: log later when we add logging
            pass
    client.close()
