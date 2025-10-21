# Events (M1)

## SSE endpoint
`GET /events` — Content-Type: `text/event-stream`. Each line is `data: <json>`, blank line delimited.

Example:
```bash
curl -N -H 'Authorization: Bearer <token>' http://localhost:8080/events
```

Emitted:
- `spawn.ready` (on first start via continue/spawn)
- `container.attached` (when reattaching)
- `export.created` (Exporter.create)
