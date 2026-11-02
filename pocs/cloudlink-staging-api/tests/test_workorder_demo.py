"""TDD red tests for CCTV-only, opt-in, synthetic work-order / simulated acceptance.
No actual site work, no payment, no public access, no real customer evidence.
"""
import json
import secrets
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from app import create_app


def _setup(monkeypatch, tmp_path, *, enabled=True):
    keys = {r: secrets.token_urlsafe(32) for r in ('customer', 'contractor', 'reviewer')}
    other_customer = secrets.token_urlsafe(32)
    other_contractor = secrets.token_urlsafe(32)
    monkeypatch.setenv('XY_ALLOW_DEMO_API', '1')
    monkeypatch.setenv('XY_DEMO_DB_PATH', str(tmp_path / 'workorders.sqlite'))
    monkeypatch.setenv('XY_STAGING_SESSIONS', '1')
    monkeypatch.setenv('XY_STAGING_SESSION_TTL', '300')
    if enabled:
        monkeypatch.setenv('XY_ENABLE_WORKORDER_DEMO', '1')
    else:
        monkeypatch.delenv('XY_ENABLE_WORKORDER_DEMO', raising=False)
    for r, v in keys.items():
        monkeypatch.setenv('XY_DEMO_' + r.upper() + '_TOKEN', v)
    monkeypatch.setenv('XY_DEMO_ACTORS_JSON', json.dumps([
        {'id': 'other-customer', 'role': 'customer', 'token': other_customer},
        {'id': 'other-contractor', 'role': 'contractor', 'token': other_contractor},
    ]))
    client = TestClient(create_app())
    sessions = {}
    for name, token in {**keys, 'other_customer': other_customer, 'other_contractor': other_contractor}.items():
        response = client.post('/staging/session', headers={'Authorization': 'Bearer ' + token})
        assert response.status_code == 200, response.text
        sessions[name] = {'Authorization': 'Bearer ' + response.json()['access_token']}
    return client, sessions


def _selected_cctv(client, auth, *, category='cctv', region='台南市'):
    request = client.post('/requests', headers=auth['customer'], json={
        'category': category, 'region': region,
        'description': '虛構店面 4 支監控攝影機更換施工與錄影驗收流程，不含個資。',
    })
    assert request.status_code == 201, request.text
    rid = request.json()['id']
    assert client.post(f'/requests/{rid}/moderate', headers=auth['reviewer'],
                       json={'decision': 'APPROVED'}).status_code == 200
    quote = client.post('/quotes', headers=auth['contractor'], json={
        'request_id': rid, 'price_ntd': 18000,
        'scope': '虛構 CCTV 4 支設備與配線施工，僅限測試報價。',
    })
    assert quote.status_code == 201, quote.text
    assert client.post(f'/quotes/{quote.json()["id"]}/select', headers=auth['customer']).status_code == 200
    return rid


def test_workorder_endpoints_off_by_default(monkeypatch, tmp_path):
    c, auth = _setup(monkeypatch, tmp_path, enabled=False)
    rid = _selected_cctv(c, auth)
    assert c.post('/staging/workorders', headers=auth['customer'],
                  json={'request_id': rid}).status_code == 404


def test_workorder_full_rework_and_simulated_acceptance(monkeypatch, tmp_path):
    c, auth = _setup(monkeypatch, tmp_path)
    rid = _selected_cctv(c, auth)
    wrong = c.post('/staging/workorders', headers=auth['contractor'],
                   json={'request_id': rid})
    assert wrong.status_code == 403
    created = c.post('/staging/workorders', headers=auth['customer'], json={'request_id': rid})
    assert created.status_code == 201, created.text
    wid = created.json()['id']
    assert created.json()['state'] == 'ASSIGNED'
    assert created.json()['payments_enabled'] is False
    assert c.post('/staging/workorders', headers=auth['customer'],
                  json={'request_id': rid}).status_code == 409
    assert c.get(f'/staging/workorders/{wid}', headers=auth['other_customer']).status_code == 404
    assert c.get(f'/staging/workorders/{wid}', headers=auth['other_contractor']).status_code == 404
    assert c.post(f'/staging/workorders/{wid}/complete', headers=auth['customer'],
                  json={'evidence_ref': 'synthetic:four-cameras-checked'}).status_code == 403
    assert c.post(f'/staging/workorders/{wid}/complete', headers=auth['other_contractor'],
                  json={'evidence_ref': 'synthetic:four-cameras-checked'}).status_code == 404
    assert c.post(f'/staging/workorders/{wid}/complete', headers=auth['contractor'],
                  json={'evidence_ref': 'https://site.example/personal-photo'}).status_code == 422

    done = c.post(f'/staging/workorders/{wid}/complete', headers=auth['contractor'],
                  json={'evidence_ref': 'synthetic:four-cameras-checked'})
    assert done.status_code == 200, done.text
    assert done.json()['state'] == 'SUBMITTED_FOR_REVIEW'
    assert c.post(f'/staging/workorders/{wid}/complete', headers=auth['contractor'],
                  json={'evidence_ref': 'synthetic:four-cameras-checked'}).status_code == 409
    assert c.post(f'/staging/workorders/{wid}/decide', headers=auth['contractor'],
                  json={'decision': 'ACCEPT', 'evidence_ref': 'synthetic:customer-checklist'}).status_code == 403
    r = c.post(f'/staging/workorders/{wid}/decide', headers=auth['customer'],
               json={'decision': 'REQUEST_REWORK', 'evidence_ref': 'synthetic:needs-better-cabling'})
    assert r.status_code == 200 and r.json()['state'] == 'REWORK_REQUESTED', r.text
    assert c.post(f'/staging/workorders/{wid}/complete', headers=auth['contractor'],
                  json={'evidence_ref': 'synthetic:four-cameras-rechecked'}).status_code == 200
    accepted = c.post(f'/staging/workorders/{wid}/decide', headers=auth['customer'],
                      json={'decision': 'ACCEPT', 'evidence_ref': 'synthetic:customer-checklist'})
    assert accepted.status_code == 200 and accepted.json()['state'] == 'SIMULATED_ACCEPTED', accepted.text
    assert accepted.json()['payments_enabled'] is False
    assert c.post(f'/staging/workorders/{wid}/decide', headers=auth['customer'],
                  json={'decision': 'ACCEPT', 'evidence_ref': 'synthetic:customer-checklist'}).status_code == 409
    events = c.get(f'/staging/workorders/{wid}/events', headers=auth['customer'])
    assert events.status_code == 200
    assert [e['event'] for e in events.json()] == [
        'CREATED', 'SUBMITTED', 'REWORK_REQUESTED', 'RESUBMITTED', 'SIMULATED_ACCEPTED']
    assert all('synthetic:' not in str(e) and '18000' not in str(e) for e in events.json())
    assert c.get(f'/staging/workorders/{wid}/events', headers=auth['other_customer']).status_code == 404
    assert c.get('/health').json()['payments_enabled'] is False
    # Recreating the app must read the same isolated SQLite rather than in-memory state.
    restarted = TestClient(create_app())
    fetched = restarted.get(f'/staging/workorders/{wid}', headers=auth['customer'])
    assert fetched.status_code == 200 and fetched.json()['state'] == 'SIMULATED_ACCEPTED', fetched.text
    assert fetched.json()['completion_evidence_ref'] == 'synthetic:four-cameras-rechecked'
    assert fetched.json()['acceptance_evidence_ref'] == 'synthetic:customer-checklist'


def test_workorder_rejects_non_cctv_region_and_before_quote_selected(monkeypatch, tmp_path):
    c, auth = _setup(monkeypatch, tmp_path)
    rid = _selected_cctv(c, auth, category='network')
    assert c.post('/staging/workorders', headers=auth['customer'],
                  json={'request_id': rid}).status_code == 409
    rid = _selected_cctv(c, auth, region='高雄市')
    assert c.post('/staging/workorders', headers=auth['customer'],
                  json={'request_id': rid}).status_code == 409
    empty = c.post('/requests', headers=auth['customer'], json={
        'category': 'cctv', 'region': '台南市', 'description': '虛構攝影機需求，尚未審核與選報價。'})
    assert empty.status_code == 201
    assert c.post('/staging/workorders', headers=auth['customer'],
                  json={'request_id': empty.json()['id']}).status_code == 409


def test_workorder_requires_opt_in_session_mode(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path)
    monkeypatch.setenv('XY_STAGING_SESSIONS', '0')
    with pytest.raises(RuntimeError, match='Workorders require staging sessions'):
        create_app()
