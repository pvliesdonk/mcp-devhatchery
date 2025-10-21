# High-Level Plan & Milestones

> Contract alignment: base branch `develop`; PRs → `develop` (squash), Conventional Commit titles; branch naming `feat|fix|docs|chore|refactor|test/<slug>`; early CI (lint/format + byte-compile/smoke); no secrets; use `.env.example`; labels: `from-ai`, `needs-review`, `docs`, `chore`.

## M1 — Hatch and Work
- Bearer auth; owner-scoped resources
- Spawn/attach with persistent volumes (+ transient flag)
- Shell + filesystem tools; streaming IO
- List (containers/volumes/snapshots) + reattach
- Exports: control-plane tar.zst and runner publish mount
- Async spawn + pre-pull
- Operator/API docs; smoke tests
- **Docs site**: add **MkDocs** at end of M1; publish site (e.g., GitHub Pages) and keep updated after every milestone
- **CI bootstrap**: ruff (lint/format), pyright (type), minimal smoke job (no runtime code until approved)

## M1.1 — Startup comfort
- Per-image warm pool (configurable map; default only for DEFAULT_IMAGE)
- APT cache persistent volume
- Snapshot to image (`docker commit`) + snapshot listing

## M2 — OIDC
- OAuth 2.1 Auth Code + PKCE via Authelia
- Token validation, audience/issuer checks
- Claim→policy mapping (optional)

## M3 — Extras (optional)
- Quotas + GC for volumes/exports
- S3/MinIO exporter
- Registry publish
