# Tool: snapshots

## list(owner?) -> [Image]
List images labeled as devhatchery snapshots.

## snapshot_to_image(container_id, new_image_tag)
Create a labeled snapshot for fast cold-starts. Volume data is not included (use exports).
