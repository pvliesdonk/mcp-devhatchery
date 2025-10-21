# Requirements — mcp-devhatchery

Status: Accepted.

## User stories
- As an MCP client, I can **spawn** a dev container and get **shell** and **filesystem** access inside it.
- As a user, I can **persist** my work in `/work` (named volume) or opt into a **transient tmpfs**.
- As a user, I can **export** work either to a control-plane export root or directly to a host path mounted as `/export` in my runner.
- As an operator, I can configure **auth** (none → bearer → OIDC), **image prepull**, **warm pool**, **limits**, and **allowed bind roots**.
- As a user, I can **list** my containers, volumes, and snapshots, then **reattach** by `workspace_key`.
- As a client, I want the server to honor **MCP Roots** so I can declare the relevant workspaces and export locations.
- As a client, I want **files also available as MCP Resources** (selected or templated) so I can pull specific content into model context without running tools.
- As security, I want **no allow-list inside the runner** but strict host isolation with alias-based bind mounts (RO by default).

## Defaults
- **Default base image:** `ubuntu:24.04` (LTS), providing a general-purpose dev base.

## Non-functional requirements
- Transport: Streamable-HTTP MCP with async readiness events.
- Concurrency: >= 10 concurrent sessions with streamed exec.
- Observability: structured audit logs; lifecycle events for containers, volumes, exports.
- Reproducibility: base image + optional snapshot; persistent volume for `/work`.
- Documentation: operators, API, security, clients; decision logs (ADRs).

## Milestones
- **M1 — Hatch and Work**: bearer auth, spawn/attach, shell/fs, list/continue, exports (both paths), async spawn + prepull, docs & smoke tests.
- **M1.1 — Startup comfort**: per-image warm pool (config map), apt cache volume, snapshot-to-image + snapshot listing.
- **M2 — OIDC**: OAuth 2.1 (Auth Code + PKCE) with Authelia; claim→policy mapping (optional).
- **M3 — Extras (optional)**: quotas/GC; S3/MinIO exporter; registry publish.
