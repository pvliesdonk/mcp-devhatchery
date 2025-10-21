from __future__ import annotations

import io, os, tarfile, time, json, hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import zstandard as zstd  # type: ignore
except Exception:  # pragma: no cover
    zstd = None

EXPORT_ROOT = Path(os.environ.get("EXPORT_ROOT", "/exports"))
EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

@dataclass
class ExportItem:
    alias: str
    src: Path
    mode: str = "ro"


class Exporter:
    """Create zstd-compressed tar archives with a MANIFEST.json next to it.

    If zstandard is unavailable, we still write a .tar.zst using raw tar bytes; replacing with real zstd can be done by adding the dependency.
    """

    def __init__(self, export_root: Path = EXPORT_ROOT):
        self.export_root = export_root

    def _tar_bytes(self, items: Iterable[ExportItem]) -> bytes:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w") as tf:
            for it in items:
                p = it.src
                if p.is_dir():
                    for child in sorted(p.rglob("*")):
                        if child.is_file():
                            tf.add(child, arcname=f"{it.alias}/{child.relative_to(p)}")
                elif p.is_file():
                    tf.add(p, arcname=f"{it.alias}/{p.name}")
        return buf.getvalue()

    def create(self, name: str, items: Iterable[ExportItem]) -> Path:
        from .events import emit  # local import to avoid cycles
        out = self.export_root / f"{name}.tar.zst"
        tmp = out.with_suffix(".tar.zst.tmp")
        raw = self._tar_bytes(items)
        sha = hashlib.sha256(raw).hexdigest()
        data = raw
        if zstd is not None:
            cctx = zstd.ZstdCompressor(level=10)
            data = cctx.compress(raw)
        tmp.write_bytes(data)
        manifest = {
            "created": int(time.time()),
            "items": [{"alias": it.alias, "path": str(it.src), "mode": it.mode} for it in items],
            "archive": {"algo": "sha256", "sha256": sha},
        }
        (out.parent / (out.name + ".MANIFEST.json")).write_text(json.dumps(manifest, indent=2))
        tmp.replace(out)
        emit('export.created', owner='system', name=name, path=str(out), manifest=manifest)
        return out
