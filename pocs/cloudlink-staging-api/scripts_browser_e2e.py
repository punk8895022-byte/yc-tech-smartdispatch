"""Chromium UI E2E bridged to the real ASGI FastAPI app/SQLite, without live HTTP.
Run locally: pip install playwright && playwright install chromium; python scripts_browser_e2e.py
No real customers, payment, internet, or production privileges.
"""
import os
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from playwright.sync_api import sync_playwright
from app import create_app

ROOT=Path(__file__).resolve().parent
TOKENS={r:r+"-abcdefghijklmnopqrstuvwxyz" for r in ("customer","reviewer","contractor")}
with tempfile.TemporaryDirectory() as directory:
    os.environ.update({"XY_ALLOW_DEMO_API":"1","XY_DEMO_DB_PATH":str(Path(directory)/"demo.sqlite"),
                       **{"XY_DEMO_"+r.upper()+"_TOKEN":t for r,t in TOKENS.items()}})
    client=TestClient(create_app())
    html=(ROOT/"web/index.html").read_text().replace('<link rel="stylesheet" href="/ui/styles.css" />','').replace('<script defer src="/ui/app.js"></script>','')
    css=(ROOT/"web/styles.css").read_text()
    js=(ROOT/"web/app.js").read_text()
    assert "localStorage" not in js and "sessionStorage" not in js
    def bridge(source,path,method="GET",authorization="",content_type="",payload=None):
        response=client.request(method,path,headers={"Authorization":authorization,"Content-Type":content_type},content=payload)
        return {"status":response.status_code,"body":response.text,"contentType":response.headers.get("content-type","application/json")}

    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={"width":390,"height":844})
        page.expose_binding("__apiFetch",bridge)
        def mount_ui():
            page.set_content(html)
            page.add_style_tag(content=css)
            page.evaluate("""window.fetch = async (path, options={}) => {
                const r=await window.__apiFetch(String(path),options.method||'GET',
                    options.headers?.Authorization||'',options.headers?.['Content-Type']||'',
                    options.body||null);
                return new Response(r.body,{status:r.status,
                    headers:{'Content-Type':r.contentType}});
            }""")
            page.add_script_tag(content=js)
        mount_ui()
        page.locator("#token").fill(TOKENS["customer"])
        page.get_by_role("button",name="新增測試案件").click()
        page.locator("#customer-list .item").wait_for()
        assert "PENDING" in page.locator("#customer-list").inner_text()
        assert client.get("/requests",headers={"Authorization":"Bearer "+TOKENS["contractor"]}).json()==[]
        page.locator("#role").select_option("reviewer")
        page.locator("#token").fill(TOKENS["reviewer"])
        page.locator("#load").click()
        page.locator("#review-list .item").wait_for()
        page.get_by_role("button",name="核准公開").click()
        page.locator("#review-list .empty").wait_for()
        page.locator("#role").select_option("contractor")
        page.locator("#token").fill(TOKENS["contractor"])
        page.locator("#load").click()
        page.locator("#contractor-list .item").wait_for()
        page.get_by_role("button",name="提交示範報價").click()
        page.locator("#role").select_option("customer")
        page.locator("#load").click()
        page.get_by_role("button",name="選擇此報價").wait_for()
        page.get_by_role("button",name="選擇此報價").click()
        page.get_by_text("此報價已選擇").wait_for()
        assert "SELECTED" in page.locator("#customer-list").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        mount_ui()
        page.locator("#token").fill(TOKENS["customer"])
        page.locator("#load").click()
        page.get_by_text("此報價已選擇").wait_for()
        print("BROWSER_BRIDGED_ASGI_E2E_PASS: 3 roles, API SQLite, 390px, reread")
        browser.close()
