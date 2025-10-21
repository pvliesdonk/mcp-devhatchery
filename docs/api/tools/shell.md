# Tool: shell

## exec(container_id, cmd: string[], cwd?, stdin?, timeout_s?) -> stream + {exit_code}
Streams stdout/stderr chunks; returns exit code on completion.

Errors use structured shape with `code`, `message`, `hint?`, `details?`.
