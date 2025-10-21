# Releasing

We use **release-please** to manage version bumps and changelogs. Flow per contract: releases via release-please; back-merge main → develop.

## Quickstart
1. Ensure develop is green and ready.
2. Merge develop → main via a Release PR created by release-please.
3. When the Release PR merges, a GitHub Release + tag is created.
4. The `build-artifacts` workflow attaches wheels/sdists to the release.
5. Back-merge main → develop.

## Manual trigger
You can run the `release-please` workflow via **Run workflow** to refresh/open a Release PR.

## Notes
- No secrets in CI. PyPI publish omitted by design.
- Version bump performed in `pyproject.toml` by release-please.
