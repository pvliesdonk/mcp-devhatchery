# Tool: mounts (Mount Broker)

## request([{alias, subpath, target, mode?}]) -> {mounted: true}
- Validates alias against `ALLOWED_ROOTS_JSON`, enforces realpath under allowed root.
- `mode`: `ro` (default) or `rw` when policy allows.
