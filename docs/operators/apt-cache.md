# APT cache warm-up smoke test

To see the benefit of APT cache persistence, run twice inside a runner:

```bash
apt-get update
apt-get install -y ripgrep
```

On the second run with `APT_CACHE_PERSIST=true`, downloads should largely hit the cache and complete faster.
