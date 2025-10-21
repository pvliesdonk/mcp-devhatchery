# Release Flow

1. PRs target develop and are squash-merged with Conventional Commit titles.
2. Promotion PR develop → main must use a Merge commit (not squash).
3. Add label promote to the promotion PR.
4. The promotion guard checks there is at least one feat|fix since the last tag on main.
5. release-please watches main and opens a Release PR automatically.
6. Auto-merge Release PR; back-merge.yml pulls main → develop.

For docs/chore-only promotions: if there is intentionally no feat|fix, add a footer to the promotion PR body to force a bump: Release-As: vX.Y.Z (use sparingly).

One-off RC releases: we do not automate prereleases. For a one-off -rc1, create/merge a PR to main with the desired changes, then create a pre-release tag manually via GitHub Releases UI or CLI. Example gh CLI: gh release create v0.2.0-rc1 --prerelease --title v0.2.0-rc1 --notes 'Release candidate for 0.2.0'.
