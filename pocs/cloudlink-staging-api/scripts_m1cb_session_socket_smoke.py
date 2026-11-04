"""M1c-B real 127.0.0.1 HTTP check; synthetic credentials only; no paid services."""
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
with tempfile.TemporaryDirectory() as temporary:
    keys = {role: secrets.token_urlsafe(32) for role in ("customer", "contractor", "reviewer")}
    env = {**os.environ, "XY_ALLOW_DEMO_API": "1", "XY_STAGING_SESSIONS": "1",
           "XY_STAGING_SESSION_TTL": "20", "XY_DEMO_DB_PATH": str(Path(temporary) / "synthetic.sqlite"),
           **{f"XY_DEMO_{role.upper()}_TOKEN": value for role, value in keys.items()}}
    with socket.socket() as sk:
        sk.bind(("127.0.0.1", 0))
        port = sk.getsockname()[1]
    cmd = [sys.executable, "-m", "uvicorn", "app:create_app", "--factory",
           "--host", "127.0.0.1", "--port", str(port)]
    process = subprocess.Popen(cmd, cwd=root, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=2) as client:
            for _ in range(40):
                try:
                    if client.get("/health").status_code == 200: break
                except httpx.RequestError:
                    time.sleep(.1)
            else: raise RuntimeError("Isolated loopback server did not become available")
            bootstrap = lambda role: {"Authorization": "Bearer " + keys[role]}
            sessions = {}
            for role in keys:
                rsp = client.post("/staging/session", headers=bootstrap(role))
                assert rsp.status_code == 200, rsp.text
                assert rsp.headers["cache-control"] == "no-store"
                sessions[role] = rsp.json()["access_token"]
            auth = lambda role: {"Authorization": "Bearer " + sessions[role]}
            data = {"category": "network", "region": "台南市",
                    "description": "完全虛構的商家網路維護驗收資料，不能用於實際報價。"}
            assert client.post("/requests", headers=bootstrap("customer"), json=data).status_code == 401
            r = client.post("/requests", headers=auth("customer"), json=data)
            assert r.status_code == 201, r.text
            rid = r.json()["id"]
            assert client.post(f"/requests/{rid}/moderate", headers=auth("customer"),
                               json={"decision": "APPROVED"}).status_code == 403
            assert client.post(f"/requests/{rid}/moderate", headers=auth("reviewer"),
                               json={"decision": "APPROVED"}).status_code == 200
            assert client.get("/staging/audit", headers=auth("customer")).status_code == 403
            events = client.get("/staging/audit", headers=auth("reviewer")).json()
            assert any(e["status"] == 403 for e in events)
            assert all("token" not in str(e).lower() and rid not in str(e) for e in events)
            assert client.post("/staging/session/revoke", headers=auth("customer")).status_code == 200
            assert client.get("/my/requests", headers=auth("customer")).status_code == 401
            assert client.get("/health").json()["payments_enabled"] is False
            print("M1CB_REAL_SOCKET_PASS: issue, role denial, redacted audit, immediate revocation")
    finally:
        process.terminate()
        try: process.communicate(timeout=4)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=2)
