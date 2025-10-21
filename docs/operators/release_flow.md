# Release Flow (semantic-release)

1. PRs target **develop** and are **squash-merged** with Conventional Commit (CC) titles.
2. Promotion PR **develop → main** must use a **Merge commit** (not squash) and include the `promote` label.
3. On push to **main**, **python-semantic-release**:
   - Calculates the next SemVer from CC history since the last tag,
   - Updates `CHANGELOG.md`,
   - Creates a git tag (`v{version}`) and a GitHub Release,
   - Builds and attaches `dist/*.whl` and `dist/*.tar.gz`.
4. **Back-merge** `main → develop` keeps branches aligned (`CHANGELOG.md` and release commit).
5. One-off RCs remain **manual**, e.g.:

```bash
# create a pre-release tag manually when needed
gh release create v0.2.0-rc1 --prerelease --title v0.2.0-rc1 --notes 'Release candidate for 0.2.0'
```

### Edge cases
- If no `feat`/`fix` since last tag, add a tiny `fix:` change. As a last resort, add a `Release-As: vX.Y.Z` footer on the promotion PR description.
- Keep the **Conventional Commit PR title** linter and **promotion guard**; they remain unchanged.
