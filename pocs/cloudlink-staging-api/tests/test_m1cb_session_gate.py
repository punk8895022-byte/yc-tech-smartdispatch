"""M1c-B evidence: synthetic local-only session lifecycle and metadata-only audit."""
import os
import re
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app import create_app
from test_workflow import client, headers


def gate(client, monkeypatch, ttl=600):
    monkeypatch.setenv("XY_STAGING_SESSIONS", "1")
    monkeypatch.setenv("XY_STAGING_SESSION_TTL", str(ttl))
    return TestClient(create_app())


def exchange(c, role="customer"):
    r = c.post("/staging/session", headers=headers(role))
    assert r.status_code == 200, r.text
    assert r.headers["cache-control"] == "no-store"
    assert r.json()["expires_in"] > 0
    assert len(r.json()["access_token"]) >= 40
    return r.json()["access_token"]


def bearer(token):
    return {"Authorization": "Bearer " + token}


def test_issue_valid_expire_revoke_and_legacy_bootstrap_rejection(client, monkeypatch):
    c = gate(client, monkeypatch)
    token = exchange(c)
    job = {"category": "network", "region": "台南市",
           "description": "合成的公司 Wi-Fi 安全測試案件，僅供隔離驗證。"}
    assert c.post("/requests", headers=headers("customer"), json=job).status_code == 401
    assert c.post("/requests", headers=bearer(token), json=job).status_code == 201
    assert c.get("/my/requests", headers=bearer(token)).status_code == 200
    assert c.get("/staging/audit", headers=bearer(token)).status_code == 403
    assert c.post("/staging/session/revoke", headers=bearer(token)).json() == {"revoked": True}
    assert c.get("/my/requests", headers=bearer(token)).status_code == 401
    assert c.post("/staging/session/revoke", headers=bearer(token)).status_code == 401
    assert c.get("/my/requests", headers={"Authorization": "Bearer forged"}).status_code == 401


def test_expiration_and_restart_persistence(client, monkeypatch):
    c = gate(client, monkeypatch, ttl=5)
    token = exchange(c)
    assert TestClient(create_app()).get("/my/requests", headers=bearer(token)).status_code == 200
    import staging_sessions
    base = staging_sessions.time.time()
    monkeypatch.setattr(staging_sessions.time, "time", lambda: base + 7)
    assert c.get("/my/requests", headers=bearer(token)).status_code == 401


def test_audit_metadata_no_tokens_no_body_and_reviewer_only(client, monkeypatch):
    c = gate(client, monkeypatch)
    customer = exchange(c)
    reviewer = exchange(c, "reviewer")
    marker = "SENSITIVE-SYNTHETIC-STRING-DO-NOT-PERSIST-IN-AUDIT"
    p = c.post("/requests", headers=bearer(customer), json={
        "category": "cctv", "region": "台南市",
        "description": marker + "，這是合成的監視器修繕需求，不是客戶資料。"})
    assert p.status_code == 201, p.text
    id_ = p.json()["id"]
    assert c.post("/requests/" + id_ + "/moderate", headers=bearer(customer),
                  json={"decision": "APPROVED"}).status_code == 403
    assert c.post("/requests/" + id_ + "/moderate", headers=bearer(reviewer),
                  json={"decision": "APPROVED"}).status_code == 200
    data = c.get("/staging/audit", headers=bearer(reviewer)).json()
    assert len(data) >= 4
    assert any(r["status"] == 403 and r["route"] == "/requests/{request_id}/moderate" for r in data)
    assert all(set(item) == {"created_at", "actor", "method", "route", "status"} for item in data)
    audit = str(data)
    assert marker not in audit and id_ not in audit
    assert customer not in audit and reviewer not in audit
    with sqlite3.connect(os.environ["XY_DEMO_DB_PATH"]) as db:
        rows = db.execute("SELECT token_hash FROM staging_sessions").fetchall()
        assert rows and all(re.fullmatch("[a-f0-9]{64}", r[0]) for r in rows)
        assert customer not in repr(rows) and reviewer not in repr(rows)


def test_gate_disabled_and_fail_closed_configuration(client, monkeypatch):
    monkeypatch.delenv("XY_STAGING_SESSIONS", raising=False)
    assert TestClient(create_app()).post("/staging/session", headers=headers("customer")).status_code == 404
    assert TestClient(create_app()).get("/my/requests", headers=headers("customer")).status_code == 200
    monkeypatch.setenv("XY_STAGING_SESSIONS", "1")
    for ttl in ("0", "901", "invalid"):
        monkeypatch.setenv("XY_STAGING_SESSION_TTL", ttl)
        with pytest.raises(RuntimeError, match="Invalid isolated staging session"):
            create_app()


def test_reviewer_cannot_read_other_actor_business_data(client, monkeypatch):
    c = gate(client, monkeypatch)
    rev = exchange(c, "reviewer")
    assert c.get("/my/requests", headers=bearer(rev)).status_code == 403
    assert c.get("/my/quotes", headers=bearer(rev)).status_code == 403
    assert isinstance(c.get("/staging/audit", headers=bearer(rev)).json(), list)
