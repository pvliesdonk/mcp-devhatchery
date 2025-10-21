# Exports

Two options:

1) **Control-plane export root** (`EXPORT_ROOT`):
   - `exports.write(workspace, destination, format)` → tar.zst/tar.gz/tar/dir
   - Atomic writes (`.tmp` then rename), `MANIFEST.json` with SHA-256

2) **Runner publish mount** via Mount Broker:
   - Broker attaches host path at `/export` (RO default; per-alias RW)
   - UID/GID mapping via `profile=user` or explicit `host_uid/gid`

Use control-plane for reproducible snapshots; runner mount for fast, large artifacts.
