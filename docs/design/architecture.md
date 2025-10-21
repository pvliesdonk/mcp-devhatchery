# Architecture — mcp-devhatchery

## Components
- **Control-plane server** (this project): FastMCP 2, Streamable-HTTP endpoint. Talks to Docker Engine API. Exposes MCP tools.
- **Runner containers**: per-request/user containers providing unrestricted shell; `/work` persistent volume; optional `/export` publish mount.

## Key flows
1. **attach_or_spawn** → create/find container for (owner, workspace, image) → stream `ready` when attachable.
2. **shell.exec** → stream stdout/stderr; return exit code.
3. **fs.* operations** → operate inside container FS; `/work` is durable storage.
4. **exports.write** (control-plane) → tar.zst/dir to `EXPORT_ROOT` with atomic rename and manifest.
5. **mounts.request** (runner publish) → alias-based, realpath-verified bind mount at `/export`.
6. **snapshot_to_image** → `docker commit` + snapshot labels; `snapshots.list`.

## Security posture
- Non-privileged containers; `cap-drop=ALL`, `no-new-privileges`.
- Bind mounts guarded by **Mount Broker**: allowed roots, RO default, RW explicit.
- Owner from Bearer/OIDC labels every container/volume/image.
- Audit logs for lifecycle, mounts, exports, and shell metadata.
