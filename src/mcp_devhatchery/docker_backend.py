from __future__ import annotations

# NOTE: Simplified interface stub to keep tests lightweight; real impl can use docker SDK.
from typing import Iterable, Optional, Any, Iterator, Tuple

class DockerBackend:
    def attach_or_spawn(self, owner: str) -> dict: ...  # existing
    def list(self, kind: str, owner: str) -> Iterable[dict]: ...  # existing

    # New: exec with streaming
    def exec_stream(self, container_id: str, cmd: list[str] | str, *, stdin: bytes | None = None, timeout: Optional[float] = None) -> Tuple[int, Iterator[Tuple[str, bytes]]]:
        """Execute a command in the container and stream output.

        Returns (exit_code, iterator of (stream, chunk)) where stream in {"stdout","stderr"}.
        Default implementation raises; real backend provides it.
        """
        raise NotImplementedError
