# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1](https://github.com/pvliesdonk/mcp-devhatchery/compare/v0.1.0...v0.1.1) (2025-10-21)


### Bug Fixes

* trigger release for M1.1 ([#48](https://github.com/pvliesdonk/mcp-devhatchery/issues/48)) ([24680d6](https://github.com/pvliesdonk/mcp-devhatchery/commit/24680d6ae41603d82a0433d9c57998353a7ad271))

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
