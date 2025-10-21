from mcp_devhatchery.exports import Exporter, ExportItem


def test_exporter_creates_artifacts(tmp_path):
    (tmp_path / 'a.txt').write_text('x')
    ex = Exporter(export_root=tmp_path)
    out = ex.create('t1', [ExportItem(alias='root', src=tmp_path)])
    assert out.exists()
    mf = tmp_path / (out.name + '.MANIFEST.json')
    assert mf.exists()
