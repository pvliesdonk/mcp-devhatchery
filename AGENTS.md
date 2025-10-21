# AGENTS.md — AI Agent Instructions (repo-wide)

## Contract Link & Scope
- Authoritative contract: [docs/design/ENGINEERING_CONTRACT.md](docs/design/ENGINEERING_CONTRACT.md)
- Base branch: `develop`; PRs target `develop`; releases via release-please on `main`.

## Planning Sources
- Requirements/design live in `docs/design/`; knowledge base in `docs/kb/`.
- Keep `docs/design/requirements.md`, `architecture.md`, ADRs current before coding.

## Plan & Build Gate
- Build work requires a referenced Plan issue (`Fixes #ID` / `Refs #ID`) unless the PR carries `plan-exempt`.
- Pre-build PRs focus on docs/planning/ops. Update the Plan issue when scope or acceptance criteria change.

## Branching, PRs & Labels
- Branch naming: `feat|fix|docs|chore|refactor|test/<slug>`.
- Rebase on `origin/develop`; squash-merge after approval.
- Apply `from-ai`, `needs-review`, plus scope labels (`docs`, `chore`, etc.).

## CI & Tooling
- Early CI: ruff (lint/format), pyright (type), pytest (tests).
- Docs: MkDocs build later in M1; publish via Pages on `main`.

## Security & Secrets
- Never commit secrets; use `.env.example`.
- Redact tokens in logs/PRs; coordinate for rotation if needed.

## Session Modes (SCM-A/B/C)
- Detect mode once per session; confirm capabilities if unclear.
- SCM-A may branch/push/PR (merge with approval); SCM-B provides diffs; SCM-C is advise-only.
