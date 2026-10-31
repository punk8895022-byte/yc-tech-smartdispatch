import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import create_app


@pytest.fixture
def client(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        monkeypatch.setenv("XY_ALLOW_DEMO_API", "1")
        monkeypatch.setenv("XY_DEMO_CUSTOMER_TOKEN", "customer-abcdefghijklmnopqrstuvwxyz")
        monkeypatch.setenv("XY_DEMO_CONTRACTOR_TOKEN", "contractor-abcdefghijklmnopqrstuvwxyz")
        monkeypatch.setenv("XY_DEMO_REVIEWER_TOKEN", "reviewer-abcdefghijklmnopqrstuvwxyz")
        monkeypatch.setenv("XY_DEMO_DB_PATH", str(Path(d) / "isolated.sqlite"))
        yield TestClient(create_app())


def headers(role):
    return {"Authorization": f"Bearer {role}-abcdefghijklmnopqrstuvwxyz"}


def test_full_flow_and_access_controls(client):
    job = {"category": "network", "region": "台南市", "description": "三間分店需要整合商用網路及 Wi-Fi AP 管理。"}
    assert client.post("/requests", json=job).status_code == 401
    assert client.post("/requests", headers=headers("contractor"), json=job).status_code == 403
    created = client.post("/requests", headers=headers("customer"), json=job)
    assert created.status_code == 201
    rid = created.json()["id"]
    quote = {"request_id": rid, "price_ntd": 28000, "scope": "含 3 個 Wi-Fi AP 安裝與基本設定，不含拉線。"}
    assert client.get("/requests", headers=headers("contractor")).json() == []
    assert client.post("/quotes", headers=headers("contractor"), json=quote).status_code == 409
    assert client.post(f"/requests/{rid}/moderate", headers=headers("customer"), json={"decision":"APPROVED"}).status_code == 403
    assert client.post(f"/requests/{rid}/moderate", headers=headers("reviewer"), json={"decision":"APPROVED"}).status_code == 200
    assert len(client.get("/requests", headers=headers("contractor")).json()) == 1
    q = client.post("/quotes", headers=headers("contractor"), json=quote)
    assert q.status_code == 201
    qid = q.json()["id"]
    assert client.get(f"/requests/{rid}/quotes", headers=headers("contractor")).status_code == 403
    assert len(client.get(f"/requests/{rid}/quotes", headers=headers("customer")).json()) == 1
    assert client.post(f"/quotes/{qid}/select", headers=headers("customer")).status_code == 200
    assert client.post(f"/quotes/{qid}/select", headers=headers("customer")).status_code == 409
    assert client.get("/health").json()["payments_enabled"] is False


def test_reject_and_invalid_inputs(client):
    p = {"category": "cctv", "region": "台南", "description": "測試用監視器現場汰換案件，先不包含金流。"}
    r = client.post("/requests",headers=headers("customer"),json=p).json()["id"]
    assert client.post(f"/requests/{r}/moderate",headers=headers("reviewer"),json={"decision":"REJECTED"}).status_code == 200
    assert client.post("/quotes",headers=headers("contractor"),json={"request_id":r,"price_ntd":5,"scope":"標準監控設備安裝項目"}).status_code == 409
    assert client.post("/quotes",headers=headers("contractor"),json={"request_id":r,"price_ntd":-1,"scope":"標準監控設備安裝項目"}).status_code == 422


def test_locked_without_explicit_demo_flags(monkeypatch):
    monkeypatch.delenv("XY_ALLOW_DEMO_API", raising=False)
    with pytest.raises(RuntimeError, match="locked"):
        create_app()


def test_ui_and_role_scoped_read_endpoints(client):
    """UI comes from same app; only authorized roles can read their own view."""
    page = client.get('/demo')
    assert page.status_code == 200
    assert 'YC Tech Match' in page.text
    assert client.get('/ui/app.js').status_code == 200
    assert client.get('/ui/styles.css').status_code == 200
    assert 'payments_enabled' not in page.text
    assert client.get('/my/requests').status_code == 401
    assert client.get('/my/requests',headers=headers('contractor')).status_code == 403
    assert client.get('/review/requests',headers=headers('customer')).status_code == 403
    new = client.post('/requests',headers=headers('customer'),json={
        'category':'access','region':'台南市','description':'虛構門市的門禁整合測試需求，不需要真實付款。'})
    assert new.status_code == 201
    rid = new.json()['id']
    mine = client.get('/my/requests',headers=headers('customer')).json()
    assert any(j['id'] == rid and j['state']=='PENDING' for j in mine)
    pending = client.get('/review/requests',headers=headers('reviewer')).json()
    assert any(j['id'] == rid for j in pending


def test_database_persists_after_restarting_app(client):
    """Persistence is SQLite, not localStorage. Never store real user data."""
    created = client.post('/requests',headers=headers('customer'),json={
        'category':'network','region':'台南市','description':'重建本機 API 後也能看到的匿名案件資料。'})
    assert created.status_code == 201
    new_client = TestClient(create_app())
    after = new_client.get('/my/requests',headers=headers('customer')).json()
    assert any(r['id']==created.json()['id'] for r in after)
