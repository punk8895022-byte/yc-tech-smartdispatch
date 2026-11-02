"""End-to-end over REAL loopback TCP HTTP, synthetic CCTV only, no live services.
Uses existing FastAPI endpoints and ephemeral SQLite. No external port or real customers.
"""
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

ROOT = Path(__file__).resolve().parent


def run():
    with tempfile.TemporaryDirectory(prefix='xy-cctv-isolated-') as d:
        db_path = str(Path(d) / 'cctv.sqlite')
        names = {role: secrets.token_urlsafe(32) for role in ('customer', 'contractor', 'reviewer')}
        customer_b = secrets.token_urlsafe(32)
        env = {**os.environ,
               'XY_ALLOW_DEMO_API': '1', 'XY_STAGING_SESSIONS': '1',
               'XY_STAGING_SESSION_TTL': '90', 'XY_DEMO_DB_PATH': db_path,
               'XY_DEMO_CUSTOMER_TOKEN': names['customer'],
               'XY_DEMO_CONTRACTOR_TOKEN': names['contractor'],
               'XY_DEMO_REVIEWER_TOKEN': names['reviewer'],
               'XY_DEMO_ACTORS_JSON': json.dumps([{'id': 'other', 'role': 'customer', 'token': customer_b}])}
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        url = f'http://127.0.0.1:{port}'
        p = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app:create_app', '--factory',
                              '--host', '127.0.0.1', '--port', str(port)],
                             cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            with httpx.Client(base_url=url, timeout=2) as http:
                for _ in range(50):
                    try:
                        if http.get('/health').status_code == 200: break
                    except httpx.RequestError:
                        time.sleep(.1)
                else:
                    raise AssertionError('Loopback uvicorn never started')
                assert http.get('/health').json()['payments_enabled'] is False
                auth = {}
                for who, token in {**names, 'other': customer_b}.items():
                    res = http.post('/staging/session', headers={'Authorization': f'Bearer {token}'})
                    assert res.status_code == 200, (who, res.text)
                    auth[who] = {'Authorization': f"Bearer {res.json()['access_token']}"}
                body = {'category': 'cctv', 'region': '台南市',
                        'description': '虛構案例：台南店家 4 支監控攝影機佈線及錄影測試，不含客戶真實資料。'}
                assert http.post('/requests', headers={'Authorization': f"Bearer {names['customer']}"}, json=body).status_code == 401
                assert http.post('/requests', headers=auth['contractor'], json=body).status_code == 403
                response = http.post('/requests', headers=auth['customer'], json=body)
                assert response.status_code == 201, response.text
                rid = response.json()['id']
                quote = {'request_id': rid, 'price_ntd': 18000,
                         'scope': '虛構 CCTV 4 支設備與本機佈線，非商業報價或工單承諾。'}
                assert http.post('/quotes', headers=auth['contractor'], json=quote).status_code == 409
                assert http.post(f'/requests/{rid}/moderate', headers=auth['customer'], json={'decision': 'APPROVED'}).status_code == 403
                assert http.post(f'/requests/{rid}/moderate', headers=auth['reviewer'], json={'decision': 'APPROVED'}).status_code == 200
                assert any(x['id'] == rid for x in http.get('/requests', headers=auth['contractor']).json())
                q = http.post('/quotes', headers=auth['contractor'], json=quote)
                assert q.status_code == 201, q.text
                qid = q.json()['id']
                assert http.get(f'/requests/{rid}/quotes', headers=auth['other']).status_code == 404
                assert http.post(f'/quotes/{qid}/select', headers=auth['other']).status_code == 404
                selected = http.post(f'/quotes/{qid}/select', headers=auth['customer'])
                assert selected.status_code == 200 and selected.json()['state'] == 'SELECTED', selected.text
                assert http.post(f'/quotes/{qid}/select', headers=auth['customer']).status_code == 409
                saved = http.get('/my/requests', headers=auth['customer']).json()
                assert any(x['id'] == rid and x['selected_quote'] == qid for x in saved)
                assert http.get('/staging/audit', headers=auth['customer']).status_code == 403
                audit = http.get('/staging/audit', headers=auth['reviewer']).json()
                assert any(x['status'] == 403 for x in audit)
                assert all(rid not in str(x) and qid not in str(x) and 'Bearer' not in str(x) for x in audit)
                import sqlite3
                with sqlite3.connect(db_path) as conn:
                    row = conn.execute('SELECT state,selected_quote FROM requests WHERE id=?', (rid,)).fetchone()
                    assert row == ('SELECTED', qid)
                print(json.dumps({'status': 'CCTV_REAL_LOOPBACK_HTTP_PASS',
                                  'steps': ['session_issue', 'create', 'moderate', 'quote', 'select', 'sqlite_readback',
                                            'role_deny', 'cross_customer_404', 'audit_redaction', 'no_payment'],
                                  'category': 'cctv', 'region': '台南市', 'payments_enabled': False,
                                  'transaction': 'SYNTHETIC_ONLY'}, ensure_ascii=False))
        finally:
            p.terminate()
            try:
                p.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill(); p.communicate(timeout=2)

if __name__ == '__main__':
    run()
