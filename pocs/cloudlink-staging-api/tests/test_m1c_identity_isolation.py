"""M1c-A staging-only cross-account and quote ownership regression checks."""
import json

import pytest
from fastapi.testclient import TestClient

from app import create_app
from test_workflow import client, headers

EXTRA = [
    {"id":"alpha", "role":"customer", "token":"customer-alpha-stage-abcdefghijklmnop"},
    {"id":"bravo", "role":"customer", "token":"customer-bravo-stage-abcdefghijklmnop"},
    {"id":"alpha", "role":"contractor", "token":"contractor-alpha-stage-abcdefghijklmnop"},
    {"id":"bravo", "role":"contractor", "token":"contractor-bravo-stage-abcdefghijklmnop"},
]

def auth(role, name):
    return {"Authorization":"Bearer " + next(i["token"] for i in EXTRA if i["role"]==role and i["id"]==name)}

def stage(client, monkeypatch):
    monkeypatch.setenv("XY_DEMO_ACTORS_JSON", json.dumps(EXTRA))
    return TestClient(create_app())

def post_job(c, name):
    p={"category":"network", "region":"台南市", "description":"本案為虛構商家匿名資料，測試跨帳號隔離。"}
    response=c.post("/requests",headers=auth("customer",name),json=p)
    assert response.status_code==201,response.text
    return response.json()["id"]

def test_customer_ownership_and_no_cross_account_quotes(client,monkeypatch):
    c=stage(client,monkeypatch)
    job_a,job_b=post_job(c,"alpha"),post_job(c,"bravo")
    a=c.get("/my/requests",headers=auth("customer","alpha"))
    b=c.get("/my/requests",headers=auth("customer","bravo"))
    assert {x["id"] for x in a.json()}=={job_a}
    assert {x["id"] for x in b.json()}=={job_b}
    assert c.get("/requests",headers=auth("customer","alpha")).status_code==403
    for job in (job_a,job_b):
        assert c.post(f"/requests/{job}/moderate",headers=headers("reviewer"),json={"decision":"APPROVED"}).status_code==200
    qa=c.post("/quotes",headers=auth("contractor","alpha"),
        json={"request_id":job_a,"price_ntd":42000,"scope":"這是經核准的網路 AP 測試報價，非正式合約。"})
    qb=c.post("/quotes",headers=auth("contractor","bravo"),
        json={"request_id":job_b,"price_ntd":36000,"scope":"這是經核准的不同商家測試報價，非正式合約。"})
    assert qa.status_code==201,qa.text
    assert qb.status_code==201,qb.text
    qa_id,qb_id=qa.json()["id"],qb.json()["id"]
    assert c.get(f"/requests/{job_b}/quotes",headers=auth("customer","alpha")).status_code==404
    assert c.post(f"/quotes/{qb_id}/select",headers=auth("customer","alpha")).status_code==404
    assert [x["id"] for x in c.get(f"/requests/{job_a}/quotes",headers=auth("customer","alpha")).json()]==[qa_id]
    assert [x["id"] for x in c.get("/my/quotes",headers=auth("contractor","alpha")).json()]==[qa_id]
    assert [x["id"] for x in c.get("/my/quotes",headers=auth("contractor","bravo")).json()]==[qb_id]
    assert c.get("/my/quotes",headers=auth("customer","alpha")).status_code==403
    assert c.post(f"/quotes/{qa_id}/select",headers=auth("customer","alpha")).status_code==200
    assert c.post(f"/quotes/{qa_id}/select",headers=auth("customer","alpha")).status_code==409
    assert c.get("/my/requests",headers=auth("customer","bravo")).json()[0]["state"]=="APPROVED"

@pytest.mark.parametrize("actors",[
    [{"id":"alpha","role":"customer","token":"customer-abcdefghijklmnopqrstuvwxyz"}],
    [{"id":"not valid","role":"customer","token":"abcdefghijklmnopqrstuvwxyz-abcd"}],
    [{"id":"alpha","role":"reviewer","token":"abcdefghijklmnopqrstuvwxyz-abcd"}],
    [{"id":"alpha","role":"contractor","token":"short"}],
    [{"id":"alpha","role":"customer","token":"abcdefghijklmnopqrstuvwxyz-abcd"},
     {"id":"alpha","role":"customer","token":"not-the-same-but-still-long-enough"}],
])
def test_invalid_synthetic_actor_configuration_rejected(client,monkeypatch,actors):
    monkeypatch.setenv("XY_DEMO_ACTORS_JSON",json.dumps(actors))
    with pytest.raises(RuntimeError,match="Invalid XY_DEMO_ACTORS_JSON"):
        create_app()

def test_default_demo_mode_does_not_impersonate_extra_actors(client,monkeypatch):
    monkeypatch.delenv("XY_DEMO_ACTORS_JSON",raising=False)
    c=TestClient(create_app())
    assert c.get("/my/requests",headers=auth("customer","alpha")).status_code==401
    assert c.get("/my/quotes",headers=headers("contractor")).status_code==200
