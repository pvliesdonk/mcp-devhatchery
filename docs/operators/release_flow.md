# Release Flow

1. PRs target develop and are squash-merged with Conventional Commit titles.
2. Promotion PR develop -> main must use a Merge commit (not squash).
3. Add label promote to the promotion PR.
4. release-please watches main and opens a Release PR automatically.
5. Auto-merge Release PR; back-merge.yml pulls main -> develop.

For docs/chore-only promotions: if there is intentionally no feat|fix, add a footer to the promotion PR body to force a bump: Release-As: vX.Y.Z (use sparingly).

One-off RC releases: create/merge a PR to main with the desired changes, then create a pre-release tag manually via GitHub Releases UI or CLI, e.g.:

```bash
gh release create v0.2.0-rc1 --prerelease --title v0.2.0-rc1 --notes 'Release candidate for 0.2.0'
```
