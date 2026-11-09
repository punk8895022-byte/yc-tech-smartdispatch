from test_workflow import client, headers

def test_legacy_category_to_canonical_and_visibility(client):
    job = {"categoryId":"net","region":"台南市",
           "description":"三間虛構門市需要 Wi-Fi AP 安裝、商用網路佈線規劃。"}
    assert client.post("/legacy/requests", json=job).status_code == 401
    assert client.post("/legacy/requests",json=job,headers=headers("contractor")).status_code == 403
    response=client.post("/legacy/requests",json=job,headers=headers("customer"))
    assert response.status_code == 201
    rid=response.json()["id"]
    assert client.get("/requests",headers=headers("contractor")).json() == []
    own=client.get("/my/requests",headers=headers("customer")).json()
    assert own[0]["category"] == "network"
    assert own[0]["id"] == rid
    assert client.post(f"/requests/{rid}/moderate",json={"decision":"APPROVED"},headers=headers("reviewer")).status_code == 200
    assert client.get("/requests",headers=headers("contractor")).json()[0]["id"] == rid
    assert client.get("/legacy-staging").status_code == 200
    assert client.get("/ui/legacy.js").status_code == 200

def test_unsupported_categories_cannot_be_misclassified(client):
    for category in ("weak","info","pc","__proto__"):
        response=client.post("/legacy/requests",json={
            "categoryId":category,"region":"台南市",
            "description":"這是虛構設備維護案件，不能自動對應類別。"
        },headers=headers("customer"))
        assert response.status_code == 422

def test_noncustomer_cannot_read_customer_jobs(client):
    assert client.get("/my/requests",headers=headers("contractor")).status_code == 403
    assert client.get("/my/requests").status_code == 401

def test_demo_html_has_only_local_nonpayment_bridge(client):
    html=client.get("/legacy-staging").text
    assert "legacy.js" in html
    assert "/ui/styles.css" in html
    assert client.get("/health").json()["payments_enabled"] is False
