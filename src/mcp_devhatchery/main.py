from __future__ import annotations

import uvicorn
from .server import create_app


def run() -> None:
    app = create_app()
    # TODO: make host/port configurable via env
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    run()
