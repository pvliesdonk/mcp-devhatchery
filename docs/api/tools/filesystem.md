# Tool: filesystem

## read(container_id, path, offset?, length?) -> bytes
## write(container_id, path, bytes, mode?) -> {size}
## stat(container_id, path) -> {type, size, mtime}
## listdir(container_id, path) -> [Dirent]
## rm(container_id, path, recursive?) -> {}
## mkdir(container_id, path, parents?) -> {}

Paths default to Roots; absolute paths allowed with explicit intent.
