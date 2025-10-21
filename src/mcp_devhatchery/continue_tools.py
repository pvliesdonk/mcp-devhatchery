from __future__ import annotations

import os, time, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    from .docker_backend import DockerBackend  # type: ignore
except Exception:  # pragma: no cover
    DockerBackend = object  # fallback for type hints

from .exports import EXPORT_ROOT
from .events import emit

@dataclass
class ContainerDesc:
    id: str
    image: str
    state: str
    labels: dict[str, str]


class ContinueService:
    """Owner-scoped list/continue/reattach utilities.

    Uses DockerBackend when available. Methods are resilient to API shape by probing common names.
    """

    def __init__(self, backend: Optional[DockerBackend] = None):
        self.backend = backend or DockerBackend()

    # ---- helpers ----------------------------------------------------------
    def _list_containers_backend(self, owner: str) -> list[dict]:
        b = self.backend
        if hasattr(b, 'list_containers'):
            return list(getattr(b, 'list_containers')(owner=owner))
        if hasattr(b, 'list'):
            return list(getattr(b, 'list')(kind='containers', owner=owner))
        return []

    def _list_volumes_backend(self, owner: str) -> list[dict]:
        b = self.backend
        if hasattr(b, 'list_volumes'):
            return list(getattr(b, 'list_volumes')(owner=owner))
        if hasattr(b, 'list'):
            return list(getattr(b, 'list')(kind='volumes', owner=owner))
        return []

    def _attach_or_spawn(self, owner: str) -> dict[str, Any]:
        b = self.backend
        if hasattr(b, 'attach_or_spawn'):
            return getattr(b, 'attach_or_spawn')(owner=owner)
        raise RuntimeError('DockerBackend.attach_or_spawn unavailable')

    # ---- public API ------------------------------------------------------
    def containers_list(self, owner: str) -> list[ContainerDesc]:
        items = self._list_containers_backend(owner)
        out: list[ContainerDesc] = []
        for it in items:
            out.append(ContainerDesc(
                id=str(it.get('id') or it.get('Id') or it.get('container_id', '')),
                image=str(it.get('image') or it.get('Image', '')),
                state=str(it.get('state') or it.get('State') or it.get('status') or ''),
                labels=dict(it.get('labels') or it.get('Labels') or {}),
            ))
        return out

    def volumes_list(self, owner: str) -> list[dict]:
        return self._list_volumes_backend(owner)

    def snapshots_list(self, owner: str) -> list[dict]:
        out: list[dict] = []
        if not EXPORT_ROOT.exists():
            return out
        for mf in sorted(EXPORT_ROOT.glob('*.tar.zst.MANIFEST.json')):
            try:
                data = json.loads(mf.read_text())
            except Exception:
                continue
            name = mf.name.replace('.tar.zst.MANIFEST.json', '')
            out.append({
                'name': name,
                'manifest': data,
                'archive': str(EXPORT_ROOT / f'{name}.tar.zst'),
            })
        return out

    def reattach(self, owner: str) -> Optional[str]:
        for c in self.containers_list(owner):
            if (c.state or '').lower().startswith('running'):
                emit('container.attached', owner, container_id=c.id)
                return c.id
        return None

    def continue_or_spawn(self, owner: str) -> dict[str, Any]:
        existing = self.reattach(owner)
        if existing:
            return { 'container_id': existing, 'continued': True }
        res = self._attach_or_spawn(owner)
        cid = str(res.get('id') or res.get('container_id') or '')
        emit('spawn.ready', owner, container_id=cid)
        return { 'container_id': cid, 'continued': False }
