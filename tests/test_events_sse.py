from fastapi.testclient import TestClient
from mcp_devhatchery.server import app
from mcp_devhatchery.events import emit


def test_sse_streams_one_event():
    client = TestClient(app)
    with client.stream('GET', '/events') as r:
        emit('test.stream', 'u1', x=1)
        chunk = next(r.iter_lines())
        assert chunk.startswith('data: ')
