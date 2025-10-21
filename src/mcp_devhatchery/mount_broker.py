from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

DEFAULT_POLICY = "ro"

@dataclass
class Mount:
    alias: str
    real: Path
    mode: str = DEFAULT_POLICY


class MountBroker:
    """Alias→realpath mapping with default RO policy.
    Runner will bind these under /export/<alias>.
    """
    def __init__(self):
        self._map: Dict[str, Mount] = {}

    def register(self, alias: str, real: str | Path, *, mode: str = DEFAULT_POLICY) -> None:
        self._map[alias] = Mount(alias, Path(real).resolve(), mode)

    def resolve(self, alias: str) -> Mount:
        return self._map[alias]

    def list(self) -> list[Mount]:
        return list(self._map.values())
