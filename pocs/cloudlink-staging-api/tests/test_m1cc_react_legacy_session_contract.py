"""M1c-C regression: actual legacy React's expected API contract.
Synthetic accounts/SQLite only; no real users and no financial operations.
"""
from fastapi.testclient import TestClient

from app import create_app
from test_workflow import client, headers


def _bearer(token: str):
    return {"Authorization": "Bearer " + token}


def _short(c: TestClient, role: str):
    response = c.post("/staging/session", headers=headers(role))
    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    body = response.json()
    assert 5 <= body["expires_in"] <= 900
    return body["access_token"]


def test_original_cloudlink_expected_exchange_legacy_post_revoke(client, monkeypatch):
    # The React form now requires this deliberately opt-in mode.
    monkeypatch.setenv("XY_STAGING_SESSIONS", "1")
    c = TestClient(create_app())
    customer = _short(c, "customer")
    payload = {"categoryId": "net", "region": "台南市",
               "description": "虛構多分店 Wi-Fi 設備升級、交換器配置與交付文件。"}
    # The old long-lived bootstrap credential must not reach the business API.
    assert c.post("/legacy/requests", headers=headers("customer"),
                  json=payload).status_code == 401
    created = c.post("/legacy/requests", headers=_bearer(customer), json=payload)
    assert created.status_code == 201, created.text
    assert created.json()["state"] == "PENDING"
    rid = created.json()["id"]
    assert c.get("/my/requests", headers=_bearer(customer)).json()[0]["id"] == rid
    assert c.post("/staging/session/revoke", headers=_bearer(customer)).json() == {"revoked": True}
    assert c.get("/my/requests", headers=_bearer(customer)).status_code == 401
    # Simulated flow can continue only with separately issued role-bound sessions.
    reviewer = _short(c, "reviewer")
    assert c.post(f"/requests/{rid}/moderate", headers=_bearer(reviewer),
                  json={"decision": "APPROVED"}).status_code == 200
    contractor = _short(c, "contractor")
    quote = c.post("/quotes", headers=_bearer(contractor),
                   json={"request_id": rid, "price_ntd": 42000,
                         "scope": "虛構 Wi-Fi 交換器佈署、連線測試及設備清冊。"})
    assert quote.status_code == 201, quote.text
    renewed_customer = _short(c, "customer")
    assert c.post(f"/quotes/{quote.json()['id']}/select",
                  headers=_bearer(renewed_customer)).status_code == 200
    assert c.get("/health").json()["payments_enabled"] is False


def test_legacy_form_fails_closed_when_session_not_enabled(client):
    assert client.post("/staging/session", headers=headers("customer")).status_code == 404
    assert client.get("/health").json()["payments_enabled"] is False


def test_wrong_role_and_unsupported_legacy_category_with_short_session(client, monkeypatch):
    monkeypatch.setenv("XY_STAGING_SESSIONS", "1")
    c = TestClient(create_app())
    contractor = _short(c, "contractor")
    customer = _short(c, "customer")
    payload = {"categoryId": "net", "region": "台南市",
               "description": "此為虛構的多據點網路規劃，無個資與付款。"}
    assert c.post("/legacy/requests", headers=_bearer(contractor),
                  json=payload).status_code == 403
    payload["categoryId"] = "unapproved"
    assert c.post("/legacy/requests", headers=_bearer(customer),
                  json=payload).status_code == 422
