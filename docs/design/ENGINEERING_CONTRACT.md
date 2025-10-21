# ENGINEERING_CONTRACT.md (capsule) — v2.2.0

This repository follows the **AI × Peter Engineering Contract v2.2.0**.
The canonical source is maintained at `pvliesdonk/ai_engineer_contract`.

## Key Points
- Base branch is `develop`. `main` is release-only; we cut releases from `develop → main` via release PRs.
- Feature branches: `feat|fix|docs|chore|refactor|test/<slug>`; squash-merge PRs into `develop`.
- PR quality: Conventional Commit titles, small focused diffs, with Summary/Why/Changes/Validation/Risk & Rollback.
- Early CI: **ruff** (lint/format), **pyright** (type), **pytest** (smoke).
- Keep `docs/design` and `docs/kb` in sync with changes; update ADRs.
- SCM modes: A/B/C with explicit confirmation for privileged ops.

> For the full contract text and updates, see the upstream repository.
