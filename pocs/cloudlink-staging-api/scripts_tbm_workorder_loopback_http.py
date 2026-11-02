"""Real TCP/HTTP isolated CCTV bid -> simulated work order and acceptance."""
import json
import os
import secrets
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent


def run():
    with tempfile.TemporaryDirectory(prefix='xy-workorder-real-http-') as d:
        db = str(Path(d) / 'cctv_workorder.sqlite')
        keys = {role: secrets.token_urlsafe(32) for role in ('customer', 'contractor', 'reviewer')}
        env = {**os.environ, 'XY_ALLOW_DEMO_API': '1', 'XY_STAGING_SESSIONS': '1',
               'XY_ENABLE_WORKORDER_DEMO': '1', 'XY_DEMO_DB_PATH': db,
               **{'XY_DEMO_' + role.upper() + '_TOKEN': key for role, key in keys.items()}}
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app:create_app', '--factory',
                                    '--host', '127.0.0.1', '--port', str(port)], cwd=ROOT,
                                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            with httpx.Client(base_url='http://127.0.0.1:' + str(port), timeout=3) as c:
                for _ in range(50):
                    try:
                        if c.get('/health').status_code == 200: break
                    except httpx.RequestError:
                        time.sleep(.1)
                else:
                    raise RuntimeError('Server startup failed')
                def get_session(role):
                    r = c.post('/staging/session', headers={'Authorization': 'Bearer '+keys[role]})
                    assert r.status_code == 200, r.text
                    return {'Authorization': 'Bearer '+r.json()['access_token']}
                h = {role: get_session(role) for role in keys}
                assert c.get('/health').json()['payments_enabled'] is False
                req = c.post('/requests', headers=h['customer'], json={'category':'cctv',
                    'region':'台南市', 'description':'虛構 CCTV 店面四支攝影機與配線工程，僅限 staging。'})
                assert req.status_code == 201, req.text
                rid = req.json()['id']
                assert c.post(f'/requests/{rid}/moderate',headers=h['reviewer'],json={'decision':'APPROVED'}).status_code == 200
                quote = c.post('/quotes',headers=h['contractor'],json={'request_id':rid,
                    'price_ntd':18000,'scope':'4 支 CCTV 虛構施工報價，不是實際交易。'})
                assert quote.status_code == 201, quote.text
                qid = quote.json()['id']
                assert c.post(f'/quotes/{qid}/select',headers=h['customer']).status_code == 200
                wo = c.post('/staging/workorders',headers=h['customer'],json={'request_id':rid})
                assert wo.status_code == 201, wo.text
                wid = wo.json()['id']
                assert wo.json()['state'] == 'ASSIGNED'
                assert c.post('/staging/workorders',headers=h['contractor'],json={'request_id':rid}).status_code == 403
                assert c.post(f'/staging/workorders/{wid}/complete',headers=h['contractor'],
                              json={'evidence_ref':'synthetic:four-cameras-installed'}).status_code == 200
                assert c.post(f'/staging/workorders/{wid}/decide',headers=h['customer'],
                              json={'decision':'REQUEST_REWORK','evidence_ref':'synthetic:replace-one-camera'}).status_code == 200
                assert c.post(f'/staging/workorders/{wid}/complete',headers=h['contractor'],
                              json={'evidence_ref':'synthetic:four-cameras-rechecked'}).status_code == 200
                accepted = c.post(f'/staging/workorders/{wid}/decide',headers=h['customer'],
                                  json={'decision':'ACCEPT','evidence_ref':'synthetic:owner-review-only'})
                assert accepted.status_code == 200 and accepted.json()['state'] == 'SIMULATED_ACCEPTED', accepted.text
                assert accepted.json()['payments_enabled'] is False
                saved = c.get(f'/staging/workorders/{wid}',headers=h['customer'])
                assert saved.status_code == 200 and saved.json()['state']=='SIMULATED_ACCEPTED'
                with sqlite3.connect(db) as conn:
                    assert conn.execute('SELECT state FROM staging_workorders WHERE id=?',(wid,)).fetchone()[0]=='SIMULATED_ACCEPTED'
                    assert conn.execute('SELECT state FROM requests WHERE id=?',(rid,)).fetchone()[0]=='SELECTED'
                events = c.get(f'/staging/workorders/{wid}/events',headers=h['customer'])
                assert [x['event'] for x in events.json()] == ['CREATED','SUBMITTED','REWORK_REQUESTED','RESUBMITTED','SIMULATED_ACCEPTED']
                assert all('synthetic:' not in str(e) for e in events.json())
                assert c.get('/staging/audit',headers=h['customer']).status_code == 403
                audit = c.get('/staging/audit',headers=h['reviewer'])
                assert audit.status_code == 200
                assert any(e['route']=='/staging/workorders/{workorder_id}/decide' for e in audit.json())
                assert all(wid not in str(e) and rid not in str(e) for e in audit.json())
                print(json.dumps({'status':'CCTV_WORKORDER_REAL_LOOPBACK_HTTP_PASS',
                    'events':[e['event'] for e in events.json()], 'workorder_state':'SIMULATED_ACCEPTED',
                    'mode':'LOCAL_SYNTHETIC', 'payments_enabled':False},ensure_ascii=False))
        finally:
            process.terminate()
            try: process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill();process.communicate(timeout=2)

if __name__=='__main__':
    run()
