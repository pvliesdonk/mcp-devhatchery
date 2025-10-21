from mcp_devhatchery.mount_broker import MountBroker


def test_mount_broker_register_and_resolve(tmp_path):
    b = MountBroker()
    b.register('data', tmp_path)
    m = b.resolve('data')
    assert m.alias == 'data'
    assert m.real.exists()
