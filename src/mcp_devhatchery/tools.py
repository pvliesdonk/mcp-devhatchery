from __future__ import annotations

import base64, subprocess, threading, queue, shlex
from typing import Optional, Callable, Iterator, Tuple

from .continue_tools import ContinueService
from .docker_backend import DockerBackend

StreamCb = Optional[Callable[[str, bytes], None]]


def tool_shell_exec(command: str | list[str], *, owner: Optional[str] = None, stdin_b64: str | None = None, timeout_sec: float | None = None, workdir: str | None = None, env: dict | None = None, stream_cb: StreamCb = None) -> dict:
    """Execute a command inside the per-owner runner and stream output.

    Returns {exit_code, stdout_b64, stderr_b64}.
    """
    # Resolve/ensure runner
    svc = ContinueService()
    cont = svc.continue_or_spawn(owner or 'system')
    cid = cont['container_id']

    backend = DockerBackend()
    stdin = base64.b64decode(stdin_b64) if stdin_b64 else None

    # If backend doesn't implement exec_stream yet, fall back to control-plane /bin/sh
    if not hasattr(backend, 'exec_stream'):
        raise RuntimeError('DockerBackend.exec_stream unavailable')

    exit_code, it = backend.exec_stream(cid, command, stdin=stdin, timeout=timeout_sec)
    out_buf: list[bytes] = []
    err_buf: list[bytes] = []
    for stream, chunk in it:
        if stream == 'stdout':
            out_buf.append(chunk)
        else:
            err_buf.append(chunk)
        if stream_cb:
            stream_cb(stream, chunk)
    return {
        'exit_code': exit_code,
        'stdout_b64': base64.b64encode(b''.join(out_buf)).decode(),
        'stderr_b64': base64.b64encode(b''.join(err_buf)).decode(),
    }
