from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from .exports import EXPORT_ROOT

LABEL_SUFFIX = '.LABELS.json'

def label_snapshot(name: str, labels: Dict[str, Any]) -> Path:
    p = EXPORT_ROOT / f'{name}{LABEL_SUFFIX}'
    p.write_text(json.dumps(labels, indent=2))
    return p

def read_snapshot_labels(name: str) -> Dict[str, Any]:
    p = EXPORT_ROOT / f'{name}{LABEL_SUFFIX}'
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}
