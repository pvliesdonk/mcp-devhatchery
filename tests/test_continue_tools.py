import types
from mcp_devhatchery.continue_tools import ContinueService

class FakeBackend:
    def __init__(self, containers):
        self._containers = containers
    def list(self, kind: str, owner: str):
        if kind=="containers":
            return self._containers
        return []
    def attach_or_spawn(self, owner: str):
        return { 'id': 'spawned-123' }


def test_reattach_when_running():
    b = FakeBackend([{ 'id':'abc', 'image':'ubuntu', 'state':'running', 'labels':{'owner':'u1'}}])
    svc = ContinueService(backend=b)
    assert svc.reattach('u1') == 'abc'


def test_continue_or_spawn_spawns_when_none():
    b = FakeBackend([])
    svc = ContinueService(backend=b)
    out = svc.continue_or_spawn('u1')
    assert out['continued'] is False and out['container_id']
