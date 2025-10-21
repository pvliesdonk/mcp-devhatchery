from mcp_devhatchery.events import BUS, emit, Event
from mcp_devhatchery.continue_tools import ContinueService

class FakeBackend:
    def __init__(self, to_spawn=True):
        self.to_spawn = to_spawn
    def list(self, kind: str, owner: str):
        return []
    def attach_or_spawn(self, owner: str):
        return { 'id': 'c1' }


def test_event_bus_publish_and_subscribe():
    seen = []
    def sub(evt: Event):
        seen.append(evt)
    BUS.subscribe(sub)
    emit('test.evt', 'u1', x=1)
    assert any(e.type=='test.evt' and e.owner=='u1' for e in seen)


def test_continue_emits_spawn_ready_when_spawning():
    svc = ContinueService(backend=FakeBackend())
    seen = []
    BUS.subscribe(lambda e: seen.append(e))
    svc.continue_or_spawn('uX')
    assert any(e.type=='spawn.ready' for e in seen)
