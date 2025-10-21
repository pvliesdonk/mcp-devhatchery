from unittest import mock
from mcp_devhatchery.docker_backend import DockerBackend, _slugify


def test_slugify_basic():
    assert _slugify('Hello World') == 'hello-world'
    assert _slugify('A'*80).startswith('a')
    assert len(_slugify('A'*80)) <= 63


def test_volume_and_container_names():
    b = DockerBackend()
    assert b.volume_name('Owner X', 'My WS').startswith('devhatchery_ws_owner-x_my-ws')
    n = b.container_name('Owner X', 'My WS')
    assert n.startswith('devhatchery_ct_owner-x_my-ws_')
    assert len(n.split('_')[-1]) == 5


class DummyImage:
    def __init__(self, tags=None, short_id='sha:123'):
        self.tags = tags or []
        self.short_id = short_id

class DummyContainer:
    def __init__(self, id='cid', name='cname', image=None, labels=None, status='running'):
        self.id = id
        self.name = name
        self.image = image or DummyImage(['ubuntu:24.04'])
        self.labels = labels or {}
        self.status = status
        self.attrs = {'Created': 'now'}

class DummyContainers:
    def __init__(self, items):
        self._items = items
    def list(self, all=False, filters=None):
        return self._items
    def get(self, cid):
        return DummyContainer(id=cid)

class DummyVolumes:
    def __init__(self):
        self._created = {}
    def get(self, name):
        raise Exception('NotFound')
    def create(self, name, labels=None):
        self._created[name] = True
        class V: pass
        v = V(); v.name = name; return v

class DummyAPI:
    def create_host_config(self, **kw):
        return kw
    def create_container(self, **kw):
        return {'Id': 'newcid'}
    def start(self, container):
        return None
    def commit(self, container, repository, tag):
        return {'Id': 'imgid'}

class DummyClient:
    def __init__(self, items=None):
        self.containers = DummyContainers(items or [])
        self.volumes = DummyVolumes()
        self.api = DummyAPI()


@mock.patch('mcp_devhatchery.docker_backend.docker')
def test_attach_or_spawn_creates_when_missing(mock_docker):
    mock_docker.from_env.return_value = DummyClient(items=[])
    b = DockerBackend()
    out = b.attach_or_spawn('peter', 'ws', 'ubuntu:24.04')
    assert out['status'] == 'starting'
    assert out['container_id'] == 'newcid'


@mock.patch('mcp_devhatchery.docker_backend.docker')
def test_list_containers_shapes(mock_docker):
    items = [DummyContainer()]
    mock_docker.from_env.return_value = DummyClient(items=items)
    b = DockerBackend()
    rows = b.list_containers()
    assert isinstance(rows, list) and rows
    assert 'id' in rows[0] and 'image' in rows[0]


@mock.patch('mcp_devhatchery.docker_backend.docker')
def test_snapshot_to_image(mock_docker):
    mock_docker.from_env.return_value = DummyClient(items=[])
    b = DockerBackend()
    imgid = b.snapshot_to_image('cid', 'repo:tag')
    assert imgid == 'imgid'
