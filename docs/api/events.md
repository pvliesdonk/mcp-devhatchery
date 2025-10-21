# Event Streams

Events are streamed over the MCP transport (Streamable-HTTP).

## Container lifecycle
- `container.started` {container_id, image, workspace}
- `container.ready` {container_id}
- `container.stopped` {container_id, reason}

## Export lifecycle
- `export.started` {workspace, destination}
- `export.completed` {workspace, destination, bytes, sha256}

## Readiness
- `spawn.ready` includes attach URL or token for the session.
