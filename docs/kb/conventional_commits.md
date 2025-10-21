# Conventional Commits (house rules)

- We **squash** PRs into `develop`. The **PR title** becomes the commit message.
- Title must follow: `type(scope): summary`
  - Types: feat, fix, docs, chore, refactor, test, ci, build, perf, revert.
  - Scope is optional but recommended (e.g., `warm-pool`, `snapshots`, `server`).
  - Summary in **imperative** form, lowercase.

## Examples
- `feat(warm-pool): add per-image warm pool with APT cache`
- `fix(server): include auth_mode in /health response`
- `docs(oidc): add M2 design scaffold`

## Why
Release Please reads commit messages on `main` to decide versions. We keep per-feature commits by merging the promotion PR (`develop → main`) **without squashing**.
