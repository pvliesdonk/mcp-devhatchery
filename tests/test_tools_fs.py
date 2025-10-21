import os, base64
from pathlib import Path
import pytest

from mcp_devhatchery.tools import _norm_path, fs_write, fs_read, fs_stat, fs_listdir, fs_rm, fs_mkdir, RootsViolation


@pytest.fixture(autouse=True)
def _tmp_work_root(monkeypatch, tmp_path):
    monkeypatch.setenv("WORK_ROOT", str(tmp_path))
    monkeypatch.delenv("ALLOWED_ROOTS", raising=False)
    yield


def test_norm_path_enforces_root(tmp_path):
    base = tmp_path
    p = _norm_path("hello.txt")
    assert str(p).startswith(str(base))
    # escape attempt
    with pytest.raises(RootsViolation):
        _ = _norm_path("/etc/passwd")


def test_fs_write_and_read_text(tmp_path):
    res = fs_write("dir/hello.txt", text="hello")
    assert res["size"] == 5
    out = fs_read("dir/hello.txt", b64=False)
    assert out["data"] == "hello"


def test_fs_stat_and_listdir(tmp_path):
    fs_mkdir("d1")
    fs_write("d1/a.txt", text="a")
    st = fs_stat("d1/a.txt")
    assert st["is_file"] and st["size"] == 1
    listing = fs_listdir("d1")
    assert any(x["name"] == "a.txt" for x in listing)


def test_fs_rm_recursive(tmp_path):
    fs_write("d2/a.txt", text="bye")
    fs_mkdir("d2/sub")
    fs_write("d2/sub/b.txt", text="x")
    fs_rm("d2", recursive=True)
    assert not (Path(os.environ.get("WORK_ROOT", str(tmp_path))) / "d2").exists()
