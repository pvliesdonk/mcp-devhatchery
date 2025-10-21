import base64
import subprocess
from mcp_devhatchery.tools import tool_shell_exec


def test_shell_exec_stub_streams(tmp_path):
    res = tool_shell_exec(command="printf 'hi'")
    assert res['exit_code'] == 0
    assert base64.b64decode(res['stdout_b64']).startswith(b'hi')
