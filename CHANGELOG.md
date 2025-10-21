# Changelog

All notable changes to this project will be documented in this file.

## 0.1.0 — 2025-10-21

### Features
- Server skeleton with FastAPI app, `/health`, uvicorn entrypoint.
- Bearer auth middleware and OwnerContext.
- Docker backend: `attach_or_spawn`, `list`, `stop/remove`, `snapshot_to_image`.
- Tools: streamed `shell.exec`; `fs.read/write/stat/listdir/rm/mkdir` with Roots enforcement.
- Exports: control‑plane tar.zst + MANIFEST; Mount Broker for `/export` (RO by default).
- List/continue and reattach flows (owner‑scoped).
- Events: `spawn.ready`, `container.*`, `export.*`; `/events` SSE endpoint.

### CI
- Ruff, Pyright, and pytest workflows (tests non‑blocking).
- Release automation wiring (release‑please + artifacts on GitHub Releases).

### Docs
- Design docs for M1, API docs for tools/events, and operator KB.
