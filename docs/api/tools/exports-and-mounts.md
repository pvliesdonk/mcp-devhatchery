# Exports & Mount Broker

## Exports (control-plane)
Create a compressed archive (`.tar.zst`) with a `MANIFEST.json` alongside it under `EXPORT_ROOT` (default `/exports`).

**Manifest schema**
```json
{
  "created": 1730000000,
  "items": [{ "alias": "root", "path": "/work", "mode": "ro" }],
  "archive": { "algo": "sha256", "sha256": "..." }
}
```

## Mount Broker
Map human-readable aliases to real host paths with a default read-only policy. Runner binds these under `/export/<alias>` as read-only unless explicitly set to `rw`.
