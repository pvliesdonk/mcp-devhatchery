# Tools: shell.exec and fs.*

**Status:** M1 — Build (tracked in #15)

## shell.exec
Run a command with streamed logs.

**Input**
- `command`: `string | string[]` — if string, runs via `/bin/sh -lc`.
- `stdin_b64?`: base64-encoded bytes for stdin.
- `timeout_sec?`: soft timeout.
- `workdir?`: working directory.
- `env?`: object of extra env vars.

**Output**
- `exit_code`: number.
- `stdout_b64`: base64 bytes.
- `stderr_b64`: base64 bytes.

**Streaming**
- Server emits log events for stdout/stderr chunks as they arrive.

## fs.*
All paths are resolved against `WORK_ROOT` (default `/work`) unless an absolute path within `ALLOWED_ROOTS`.

### fs.stat(path) -> {exists,is_dir,is_file,size,mode,mtime,path}
### fs.listdir(path) -> Array<{name,is_dir,size}>
### fs.read(path, max_bytes?, b64=true) -> {path,data_b64|data,size}
### fs.write(path, data_b64?|text?, mode="644") -> {path,size}
### fs.rm(path, recursive=false) -> {path,removed}
### fs.mkdir(path, parents=true, exist_ok=true, mode="755") -> {path,exists}

**Security**
- Roots enforcement prevents escaping to host paths; absolute paths must be under an allowed root.

**Notes**
- Runners start as root; user switching arrives in later milestones.
