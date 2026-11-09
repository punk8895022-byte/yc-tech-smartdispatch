from test_workflow import client

def test_original_react_route_off_by_default(client, monkeypatch):
    monkeypatch.delenv("XY_ALLOW_LEGACY_REACT", raising=False)
    assert client.get("/legacy-react").status_code == 404

def test_original_react_route_requires_explicit_local_index(client, monkeypatch, tmp_path):
    monkeypatch.setenv("XY_ALLOW_LEGACY_REACT", "1")
    monkeypatch.delenv("XY_CLOUDLINK_LEGACY_HTML_PATH", raising=False)
    assert client.get("/legacy-react").status_code == 404
    index = tmp_path / "index.html"
    index.write_text("<!doctype html><title>LOCAL_REACT_TEST_ONLY</title>",encoding="utf-8")
    monkeypatch.setenv("XY_CLOUDLINK_LEGACY_HTML_PATH",str(index))
    response=client.get("/legacy-react")
    assert response.status_code == 200
    assert "LOCAL_REACT_TEST_ONLY" in response.text
    assert response.headers["cache-control"] == "no-store"

def test_original_react_route_rejects_unexpected_filename(client, monkeypatch, tmp_path):
    fake = tmp_path / "admin.html"
    fake.write_text("<!doctype html><title>NOT_ALLOW</title>")
    monkeypatch.setenv("XY_ALLOW_LEGACY_REACT","1")
    monkeypatch.setenv("XY_CLOUDLINK_LEGACY_HTML_PATH",str(fake))
    assert client.get("/legacy-react").status_code == 404
