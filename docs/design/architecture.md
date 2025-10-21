# Architecture — mcp-devhatchery

## Components
- **Control-plane server**: FastMCP 2, Streamable-HTTP endpoint. Talks to Docker Engine API. Exposes Tools + Resources, supports Roots.
- **Runner containers**: per-request/user containers providing unrestricted shell; `/work` persistent volume; optional `/export` publish mount.

## Key flows
1. **attach_or_spawn** → create/find container for (owner, workspace, image) → stream `ready` when attachable.
2. **shell.exec** → stream stdout/stderr; return exit code.
3. **fs.* operations** → operate inside container FS; `/work` is durable storage.
4. **exports.write** (control-plane) → tar.zst/dir to `EXPORT_ROOT` with atomic rename and manifest.
5. **mounts.request** (runner publish) → alias-based, realpath-verified bind mount at `/export`.
6. **snapshot_to_image** → `docker commit` + snapshot labels; `snapshots.list`.
7. **resources** → expose `/work` files (and optional `/export` subtrees) as MCP Resources; resource templates allow on-demand URIs.
8. **roots** → honor client-declared Roots; constrain listing/templating and default working sets to those URIs.

## Roots (MCP)
- On connect, if the client declares Roots, the server narrows default workspaces to those URIs.
- Supported forms: `file://` for `/work` subtrees, `file://` for control-plane `EXPORT_ROOT` (read-only), and custom `devhatchery://workspace/{owner}/{workspace}` for discovery.
- Tools respect Roots for default path resolution and listing; out-of-root operations require explicit absolute paths.

## Resources
- **Direct resources**: recent files in `/work` (e.g., `/work/README.md`, key configs) exposed with metadata (mime, size, lastModified).
- **Resource templates**: `file:///work/{path}` and `file:///export/{path}` with globs; clients can materialize URIs and call `resources/read`.
- Binary + text supported; large files stream-chunked with size caps.

## Security posture
- Non-privileged containers; `cap-drop=ALL`, `no-new-privileges`.
- Bind mounts via **Mount Broker**: allowed roots, RO default, RW explicit, realpath checks.
- Owner from Bearer/OIDC labels every container/volume/image.
- Audit logs for lifecycle, mounts, exports, and shell metadata (not contents).

## Defaults
- Base image: **ubuntu:24.04** (LTS).
