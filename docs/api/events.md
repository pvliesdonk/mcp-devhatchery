# Events (M1)

Envelope:
```json
{ "type": "spawn.ready|container.*|export.*", "owner": "string", "ts": 1730000000, "data": {} }
```

Emitted:
- `spawn.ready` (on first start via continue/spawn)
- `container.attached` (when reattaching)
- `export.created` (Exporter.create)

In M2+, more granular container.* events will be wired to the DockerBackend exec lifecycle.
