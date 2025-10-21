<!--
The PR title will become the squash commit message — make it a Conventional Commit.
Examples:
- feat(warm-pool): add per-image warm pool with APT cache
- fix(server): include auth_mode in /health response
- docs(oidc): add M2 design scaffold
-->

### Summary
- ...

### Type
- [ ] feat
- [ ] fix
- [ ] docs
- [ ] chore
- [ ] refactor
- [ ] test
- [ ] ci
- [ ] build

### Scope
`<module or area, e.g. warm-pool | snapshots | server>`

### Notes
- Squash-merge into **develop** required.
- Promotion **develop → main** must use **Merge commit** (not squash) to keep per-feature commits for release-please.
