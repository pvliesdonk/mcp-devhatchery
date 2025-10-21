# High-Level Plan & Milestones

## M1 — Hatch and Work
- Bearer auth; owner-scoped resources
- Spawn/attach with persistent volumes (+ transient flag)
- Shell + filesystem tools; streaming IO
- List (containers/volumes/snapshots) + reattach
- Exports: control-plane tar.zst and runner publish mount
- Async spawn + pre-pull
- Operator/API docs; smoke tests

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
