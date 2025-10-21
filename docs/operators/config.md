# Configuration

Environment variables (see `.env.example`). Key ones:

- `AUTH_MODE`: none|bearer|oidc
- `TOKENS_JSON`: array of {id, token} for bearer
- `OIDC_ISSUER`, `OIDC_AUDIENCE`, `REQUIRE_JWT`
- `DEFAULT_IMAGE` (default `ubuntu:24.04`), `PREPULL_IMAGES`
- `WARM_POOL_MAP` (per-image warm containers)
- `PERSISTENT_BY_DEFAULT`, `APT_CACHE_PERSIST`
- `EXPORT_ROOT` (control-plane path)
- `ENABLE_HOST_BIND_MOUNTS`, `ALLOWED_ROOTS_JSON` (alias/path/default_mode)
- Limits: `MAX_CPU`, `MAX_MEM_MB`, `MAX_CONTAINERS_PER_OWNER`

All resources are labeled with `owner`, `workspace`, `image`, `created_at`.
