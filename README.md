# mcp-devhatchery

Streamable-HTTP **MCP** server that spawns per-user dev containers and exposes **shell + filesystem** to MCP clients.
Built with **FastMCP 2** and **uv** (planned), packaged as a Docker container.

> Status: **Design / Plan stage** — no runtime code yet. This repo currently hosts requirements, architecture, plans, and operator docs per our engineering contract (v2.2.0).

## What it does (scope)
- Control-plane container (this server) can **spawn** ephemeral **runner** containers from any image (policy configurable).
- Inside runners: **unrestricted shell** (root or `dev` user with passwordless sudo), persistent workspace at `/work` by default, or transient `tmpfs`.
- **Two export paths**:
  1) Control-plane export root (`/exports`) → `tar.zst|tar.gz|tar|dir`, atomic writes + manifest.
  2) Runner **publish mount** via **Mount Broker** → host bind mount at `/export` (RO default; alias-specific RW).
- **Startup**: pre-pull images; **per-image warm pool** (configurable map; default only for `DEFAULT_IMAGE`); async spawn + readiness events.
- **Auth ladder**: none → **Bearer tokens** → **OIDC/OAuth 2.1 (Authelia, Auth Code + PKCE)**.

## Contract
ACK CONTRACT v2.2.0. Base branch: `develop`. PRs → `develop`, squash merges, conventional commit titles.

## Quick links
- docs/design/requirements.md
- docs/design/architecture.md
- docs/plan/high_level_plan.md
- docs/design/milestones/M1.md

