import json, asyncio, importlib
from starlette.testclient import TestClient


def test_health_requires_bearer_token(monkeypatch):
    monkeypatch.setenv('AUTH_MODE', 'bearer')
    monkeypatch.setenv('TOKENS_JSON', json.dumps([{ 'id': 'peter', 'token': 'secret' }]))
    server = importlib.import_module('mcp_devhatchery.server')
    app = server.create_app()
    client = TestClient(app)

    r = client.get('/health')
    assert r.status_code == 401

    r = client.get('/health', headers={ 'Authorization': 'Bearer secret' })
    assert r.status_code == 200
    assert r.json()['auth_mode'] == 'bearer'


class DummyImages:
    def __init__(self):
        self.pulled = []
    def pull(self, img):
        self.pulled.append(img)

class DummyDocker:
    def __init__(self):
        self.images = DummyImages()
    def close(self):
        pass


async def _run_prepull_with(monkeypatch, imgs):
    monkeypatch.setenv('PREPULL_IMAGES', json.dumps(imgs))
    import mcp_devhatchery.prepull as p
    import docker
    monkeypatch.setattr(docker, 'from_env', lambda: DummyDocker())
    await p.prepull_images()


def test_prepull_invokes_pull(monkeypatch):
    imgs = ['ubuntu:24.04', 'node:22-bookworm']
    asyncio.run(_run_prepull_with(monkeypatch, imgs))
