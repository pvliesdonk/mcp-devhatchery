# Operator Notes — Warm Pool

## Config
- Example: set WARM_POOL_MAP to {'ubuntu:24.04': 2}
- APT cache persistence: APT_CACHE_PERSIST=true

## Observability
- Events: warm.replenished, warm.checkout

## Tradeoffs
- Slight idle resource use in exchange for faster cold-start.
