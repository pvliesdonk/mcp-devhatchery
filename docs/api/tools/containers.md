# Tool: containers

## list(owner?) -> [Container]
List running containers (owner-scoped by default).

## attach_or_spawn(workspace, image, profile="full"|"user", cpu?, mem_mb?, network?, persistent=true, warm_ok=true) -> {container_id, status}
- Returns immediately with status: starting|ready.
- Emits `container.ready` when attachable.

## stop(container_id) / remove(container_id)
Idempotent lifecycle control.

## snapshot_to_image(container_id, new_image_tag)
Create a snapshot image (labels mark as snapshot).

### JSON Shapes
```json
{
  "Container": {
    "id": "string",
    "image": "string",
    "workspace": "string",
    "owner": "string",
    "created_at": "RFC3339"
  }
}
```
