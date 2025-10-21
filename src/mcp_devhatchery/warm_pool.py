from __future__ import annotations

import asyncio, json, threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .config import settings
from .events import emit

try:
    from .docker_backend import DockerBackend  # type: ignore
except Exception:  # pragma: no cover
    DockerBackend = object  # type: ignore

@dataclass
class WarmItem:
    container_id: str
    image: str
    labels: Dict[str, str] = field(default_factory=dict)

class WarmPoolManager:
    """Maintain a per-image pool of ready containers.

    Contract with DockerBackend (best-effort, stub-friendly):
    - If backend has `spawn(image: str, labels: dict | None = None, volumes: list | None = None)` use it.
    - Else fall back to `attach_or_spawn(owner)` and treat result as a fresh container.

    Containers are labeled with `mcp.owner` when checked out.
    """

    def __init__(self, backend: Optional[DockerBackend] = None):
        self.backend = backend or DockerBackend()
        self._lock = threading.Lock()
        self._by_image: Dict[str, List[WarmItem]] = {}

    # ---- APT cache helpers ----------------------------------------------
    def _apt_cache_volumes(self, owner: str) -> Optional[list]:
        if not settings.apt_cache_persist:
            return None
        # Use a deterministic per-owner volume name to avoid sharing caches across owners.
        vol_name = f"apt-cache-{owner}"
        # Shape is backend-defined; we pass through a common dict for docker SDK adapters.
        return [{
            'type': 'volume',
            'source': vol_name,
            'target': '/var/cache/apt',
            'read_only': False,
            'labels': {'mcp.owner': owner, 'mcp.kind': 'apt-cache'}
        }]

    # ---- core ------------------------------------------------------------
    def _spawn_one(self, image: str, for_owner: str) -> Optional[WarmItem]:
        labels = {'mcp.kind': 'warm', 'mcp.image': image}
        vols = self._apt_cache_volumes(for_owner)
        b = self.backend
        try:
            if hasattr(b, 'spawn'):
                res = getattr(b, 'spawn')(image=image, labels=labels, volumes=vols)
            else:
                # Fallback: attach_or_spawn path (labels/vols may be ignored by stub).
                res = getattr(b, 'attach_or_spawn')(owner=for_owner)
            cid = str(res.get('id') or res.get('container_id') or res.get('Id') or '')
            if not cid:
                return None
            return WarmItem(container_id=cid, image=image, labels=labels)
        except Exception:
            return None

    def _pool(self, image: str) -> List[WarmItem]:
        with self._lock:
            return list(self._by_image.get(image, []))

    def _set_pool(self, image: str, items: List[WarmItem]):
        with self._lock:
            self._by_image[image] = items

    def replenish(self, owner: str) -> None:
        """Ensure configured pool sizes per image.
        WARM_POOL_MAP is JSON like {"ubuntu:24.04": 1, "node:22-bookworm": 2}.
        """
        try:
            cfg: Dict[str, int] = json.loads(settings.warm_pool_map)
        except Exception:
            cfg = {settings.default_image: 1}
        for image, target in cfg.items():
            items = self._pool(image)
            missing = max(0, int(target) - len(items))
            made: List[WarmItem] = []
            for _ in range(missing):
                it = self._spawn_one(image, for_owner=owner)
                if it:
                    made.append(it)
            if made:
                self._set_pool(image, items + made)
                emit('warm.replenished', owner=owner, image=image, count=len(made))

    def checkout(self, owner: str, image: Optional[str] = None) -> Optional[str]:
        """Checkout a ready container from the pool (or None).
        Labels the container with the owner when possible.
        """
        img = image or settings.default_image
        items = self._pool(img)
        if not items:
            return None
        item = items.pop(0)
        self._set_pool(img, items)
        emit('warm.checkout', owner=owner, image=img, container_id=item.container_id)
        # Best-effort owner labeling if backend supports it.
        try:
            if hasattr(self.backend, 'label_container'):
                getattr(self.backend, 'label_container')(item.container_id, {'mcp.owner': owner})
        except Exception:
            pass
        # Trigger background replenish without blocking.
        asyncio.get_event_loop().call_soon_threadsafe(lambda: self.replenish(owner))
        return item.container_id
