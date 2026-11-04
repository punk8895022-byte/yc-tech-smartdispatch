"""Real 127.0.0.1 socket smoke test, synthetic credentials & SQLite only."""
import os, subprocess, sys, tempfile, secrets, time
from pathlib import Path
import httpx
root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as d:
    tokens={r:secrets.token_urlsafe(32) for r in ("customer","reviewer","contractor")}
    env={**os.environ,"XY_ALLOW_DEMO_API":"1","XY_DEMO_DB_PATH":str(Path(d)/"demo.sqlite"),
         **{f"XY_DEMO_{r.upper()}_TOKEN":v for r,v in tokens.items()}}
    proc=subprocess.Popen([sys.executable,"-m","uvicorn","app:create_app","--factory",
                           "--host","127.0.0.1","--port","18765"],cwd=root,env=env,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        with httpx.Client(base_url="http://127.0.0.1:18765",timeout=1.5) as c:
            for _ in range(25):
                try: h=c.get("/health");break
                except httpx.ConnectError:time.sleep(.1)
            else:raise RuntimeError("loopback server did not start")
            assert h.status_code==200
            hdr=lambda role:{"Authorization":"Bearer "+tokens[role]}
            q=c.post("/legacy/requests",headers=hdr("customer"),
              json={"categoryId":"net","region":"台南市","description":"虛構的三間門市進行 WiFi AP 網路整合。"})
            assert q.status_code==201,q.text
            jid=q.json()["id"]
            assert c.post(f"/requests/{jid}/moderate",headers=hdr("reviewer"),
                          json={"decision":"APPROVED"}).status_code==200
            quote=c.post("/quotes",headers=hdr("contractor"),
              json={"request_id":jid,"price_ntd":20000,"scope":"三台 AP 安裝與網路規劃，不含真實施工。"})
            assert quote.status_code==201,quote.text
            assert c.post(f"/quotes/{quote.json()['id']}/select",
                          headers=hdr("customer")).status_code==200
            assert c.get("/my/requests",headers=hdr("customer")).json()[0]["state"]=="SELECTED"
            assert c.get("/legacy-react").status_code==404
            print("LOOPBACK_HTTP_PASS; React page gated off by default")
    finally:
        proc.terminate()
        try:proc.communicate(timeout=4)
        except subprocess.TimeoutExpired:proc.kill()
