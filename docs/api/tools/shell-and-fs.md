# Tools: shell.exec and fs.*

## shell.exec (Runner)
Executes inside the **per-owner runner** container.

Input: `{ command: string|string[], stdin_b64?, timeout_sec?, workdir?, env?, owner? }`
Output: `{ exit_code, stdout_b64, stderr_b64 }`

Notes:
- Uses `ContinueService.continue_or_spawn(owner)` then `DockerBackend.exec_stream`.
- Streams stdout/stderr; events may be emitted via EventBus (M2 will add exec.* events).

## fs.*
(unchanged)
