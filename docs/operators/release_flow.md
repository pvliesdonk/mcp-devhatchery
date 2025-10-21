# Release Flow

1. PRs target `develop` and are **squash-merged** with Conventional Commit titles.
2. Promotion PR `develop → main` must use a **Merge commit** (not squash).
3. `release-please` watches `main` and opens a Release PR automatically.
4. Auto-merge Release PR; `back-merge.yml` pulls `main` → `develop`.

## Why no squash on promotion?
Squashing the promotion collapses all `feat|fix` into a `chore:` and release-please won’t bump. Merge commit preserves per-feature commits.
