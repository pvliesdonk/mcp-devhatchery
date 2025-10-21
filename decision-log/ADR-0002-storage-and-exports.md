# ADR-0002: Storage & Export Strategy

**Status:** Proposed

- **Decision:** Persistent named volumes at `/work` (default) with optional transient tmpfs; **two export paths**: control-plane EXPORT_ROOT (tar.zst/dir, atomic writes + MANIFEST) and runner publish mount via Mount Broker (`/export`).
- **Consequences:** Safety by default; speed when needed; provenance via manifests.
- **Alternatives:** Host bind mounts only; copy-only exports; blob store only.
