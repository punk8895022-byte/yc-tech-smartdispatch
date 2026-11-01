"""M1c: real loopback TCP/HTTP smoke with two synthetic customers & contractors."""
import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx

root = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as tmp:
    extra = [
        {"id": name, "role": role, "token": secrets.token_urlsafe(32)}
        for role in ("customer", "contractor") for name in ("alpha", "bravo")
    ]
    base = {r: secrets.token_urlsafe(32) for r in ("customer", "contractor", "reviewer")}
    env = {**os.environ, "XY_ALLOW_DEMO_API": "1", "XY_DEMO_DB_PATH": str(Path(tmp) / "db.sqlite"),
           "XY_DEMO_ACTORS_JSON": json.dumps(extra),
           **{f"XY_DEMO_{r.upper()}_TOKEN": t for r, t in base.items()}}
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:create_app", "--factory", "--host",
                             "127.0.0.1", "--port", str(port)], cwd=root, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=3) as c:
            for _ in range(40):
                try:
                    if c.get("/health").status_code == 200: break
                except httpx.RequestError: time.sleep(.1)
            else: raise RuntimeError("Loopback server failed startup")
            h = lambda role, name: {"Authorization": "Bearer " + next(x["token"] for x in extra if x["role"] == role and x["id"] == name)}
            job = lambda name: c.post("/requests", headers=h("customer", name), json={
                "category": "network", "region": "台南市", "description": "這是完全虛構的網路 AP 驗收需求，不含客戶個資。"})
            a, b = job("alpha"), job("bravo")
            assert a.status_code == b.status_code == 201, (a.text, b.text)
            aid, bid = a.json()["id"], b.json()["id"]
            assert [x["id"] for x in c.get("/my/requests", headers=h("customer", "alpha")).json()] == [aid]
            assert [x["id"] for x in c.get("/my/requests", headers=h("customer", "bravo")).json()] == [bid]
            assert c.post(f"/requests/{aid}/moderate", headers={"Authorization": "Bearer " + base["reviewer"]},
                          json={"decision":"APPROVED"}).status_code == 200
            q = c.post("/quotes", headers=h("contractor", "alpha"), json={
                "request_id": aid, "price_ntd": 18000, "scope": "這是虛構的網路施工報價，不代表有效成交。"})
            assert q.status_code == 201, q.text
            qid = q.json()["id"]
            assert [x["id"] for x in c.get("/my/quotes", headers=h("contractor", "alpha")).json()] == [qid]
            assert c.get("/my/quotes", headers=h("contractor", "bravo")).json() == []
            assert c.get(f"/requests/{aid}/quotes", headers=h("customer", "bravo")).status_code == 404
            assert c.post(f"/quotes/{qid}/select", headers=h("customer", "bravo")).status_code == 404
            assert c.post(f"/quotes/{qid}/select", headers=h("customer", "alpha")).status_code == 200
            assert c.get("/health").json()["payments_enabled"] is False
            print("M1C_LOOPBACK_SOCKET_PASS customer_A/B request separation, contractor_A/B quote separation, cross-account 404")
    finally:
        proc.terminate()
        try: proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate(timeout=2)
