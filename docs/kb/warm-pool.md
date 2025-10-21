# Warm Pool (M1.1)

- `WARM_POOL_MAP` JSON maps image→desired count.
- Checkout emits `warm.checkout` and triggers async replenish.
- Enable APT cache persistence via `APT_CACHE_PERSIST=true` (per-owner volume mounted at /var/cache/apt).
