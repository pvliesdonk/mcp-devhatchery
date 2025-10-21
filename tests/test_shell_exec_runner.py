import base64
from mcp_devhatchery.tools import tool_shell_exec

class FakeBackend:
    def __init__(self):
        pass
    def exec_stream(self, container_id, cmd, *, stdin=None, timeout=None):
        def gen():
            yield ('stdout', b'hi')
            yield ('stderr', b'')
        return 0, gen()

# Monkeypatch DockerBackend in tools to our fake
import mcp_devhatchery.tools as T
T.DockerBackend = FakeBackend


def test_shell_exec_runs_in_runner(monkeypatch):
    # Also stub ContinueService to avoid docker dependency
    class FakeSvc:
        def continue_or_spawn(self, owner):
            return {'container_id': 'abc', 'continued': True}
    T.ContinueService = FakeSvc

    res = tool_shell_exec(["/bin/echo", "hi"], owner="u1")
    assert res['exit_code'] == 0
    assert base64.b64decode(res['stdout_b64']) == b'hi'
