import json
from mcp_devhatchery.warm_pool import WarmPoolManager
from mcp_devhatchery.snapshots import label_snapshot, read_snapshot_labels
from mcp_devhatchery.exports import Exporter, ExportItem

class DummyBackend:
    def __init__(self):
        self.spawned = []
        self.labeled = {}
    def spawn(self, image: str, labels=None, volumes=None):
        cid = f'c{len(self.spawned)+1}'
        self.spawned.append({'id': cid, 'image': image, 'labels': labels or {}, 'volumes': volumes or []})
        return {'id': cid}
    def label_container(self, cid, labels):
        self.labeled[cid] = labels


def test_warm_pool_checkout_and_replenish(monkeypatch):
    monkeypatch.setenv('WARM_POOL_MAP', json.dumps({'ubuntu:24.04': 1}))
    monkeypatch.setenv('APT_CACHE_PERSIST', 'true')
    wp = WarmPoolManager(backend=DummyBackend())
    # Fill initially
    wp.replenish(owner='u1')
    assert len(wp._by_image.get('ubuntu:24.04', [])) == 1
    # Checkout consumes one and triggers replenish
    cid = wp.checkout(owner='u1', image='ubuntu:24.04')
    assert cid is not None


def test_snapshot_labels_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv('EXPORT_ROOT', str(tmp_path))
    ex = Exporter(export_root=tmp_path)
    (tmp_path / 'a.txt').write_text('x')
    out = ex.create('snap1', [ExportItem(alias='root', src=tmp_path)])
    p = label_snapshot('snap1', {'owner': 'u1', 'image': 'ubuntu:24.04'})
    assert p.exists()
    labels = read_snapshot_labels('snap1')
    assert labels['owner'] == 'u1'
