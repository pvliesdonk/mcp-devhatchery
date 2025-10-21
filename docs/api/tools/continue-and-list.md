# Tools: list + continue + reattach (M1)

**Status:** Implemented (M1) — PR Fixes #17.

## Endpoints
- `containers.list(owner)` → `[{id,image,state,labels}]`
- `volumes.list(owner)` → `[{name,driver,labels}]`
- `snapshots.list(owner)` → discovered from `EXPORT_ROOT` (`*.tar.zst` + `MANIFEST.json`)
- `containers.reattach(owner)` → container id or null
- `continue(owner)` → `{container_id, continued: boolean}`

Notes:
- Backed by `DockerBackend` when available; resilient to API naming.
- Owner scoping via labels is expected in backend.
