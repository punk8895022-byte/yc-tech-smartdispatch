"""Opt-in CCTV-only synthetic work order lifecycle. NOT real work acceptance.

Stages: ASSIGNED -> SUBMITTED_FOR_REVIEW -> [REWORK_REQUESTED -> SUBMITTED_FOR_REVIEW] ->
SIMULATED_ACCEPTED. This module never creates a real contract, invoice, payment,
production event, verified consent, or actual job completion evidence.
"""
import re
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field


class CreateDemoWorkorder(BaseModel):
    request_id: str = Field(min_length=10, max_length=80)


class SyntheticEvidence(BaseModel):
    evidence_ref: str = Field(min_length=20, max_length=110, pattern=r"^synthetic:[a-z0-9][a-z0-9-]{8,80}$")


class SyntheticDecision(SyntheticEvidence):
    decision: Literal["REQUEST_REWORK", "ACCEPT"]


@contextmanager
def _db(path: str):
    conn = sqlite3.connect(path, timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def register_workorder_demo_routes(app: FastAPI, db_path: str, actor_dependency):
    """Register only under explicit env gate, with the already verified synthetic session role."""
    if not Path(db_path).is_absolute():
        raise RuntimeError("Workorders require an absolute isolated SQLite path")
    with _db(db_path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS staging_workorders (
                id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL UNIQUE,
                customer TEXT NOT NULL,
                contractor TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN (
                    'ASSIGNED','SUBMITTED_FOR_REVIEW','REWORK_REQUESTED','SIMULATED_ACCEPTED')),
                completion_evidence_ref TEXT,
                acceptance_evidence_ref TEXT,
                FOREIGN KEY(request_id) REFERENCES requests(id)
            );
            CREATE TABLE IF NOT EXISTS staging_workorder_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workorder_id TEXT NOT NULL,
                actor TEXT NOT NULL,
                event TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(workorder_id) REFERENCES staging_workorders(id)
            );
        """)

    def _require_role(actor: str, role: str):
        if actor.split(":", 1)[0] != role:
            raise HTTPException(403, "Staging role not allowed")

    def _load(db, workorder_id: str, actor: str):
        if actor.split(":", 1)[0] not in ("customer", "contractor"):
            raise HTTPException(403, "Staging role not allowed")
        row = db.execute("SELECT * FROM staging_workorders WHERE id=?", (workorder_id,)).fetchone()
        if row is None or actor not in (row["customer"], row["contractor"]):
            raise HTTPException(404, "Staging workorder not found")
        return row

    def _response(row):
        return {"id": row["id"], "request_id": row["request_id"],
                "state": row["state"], "completion_evidence_ref": row["completion_evidence_ref"],
                "acceptance_evidence_ref": row["acceptance_evidence_ref"],
                "payments_enabled": False, "staging_only": True}

    def _event(db, id: str, actor: str, event: str):
        db.execute("INSERT INTO staging_workorder_events(workorder_id,actor,event,created_at) VALUES(?,?,?,?)",
                   (id, actor, event, int(time.time())))

    @app.post("/staging/workorders", status_code=201)
    def create_workorder(body: CreateDemoWorkorder, actor: str = Depends(actor_dependency)):
        _require_role(actor, "customer")
        wid = str(uuid4())
        with _db(db_path) as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("""SELECT r.customer,r.category,r.region,r.state,r.selected_quote,
                                       q.contractor FROM requests r
                                LEFT JOIN quotes q ON q.id=r.selected_quote AND q.request_id=r.id
                                WHERE r.id=?""", (body.request_id,)).fetchone()
            if row is None or row["customer"] != actor:
                raise HTTPException(404, "Request not found")
            if (row["state"] != "SELECTED" or row["category"] != "cctv" or
                    row["region"] not in ("台南市", "臺南市") or row["contractor"] is None):
                raise HTTPException(409, "Selected CCTV quotation in Tainan required")
            if db.execute("SELECT id FROM staging_workorders WHERE request_id=?", (body.request_id,)).fetchone():
                raise HTTPException(409, "Staging workorder already exists")
            db.execute("""INSERT INTO staging_workorders(id,request_id,customer,contractor,state)
                          VALUES(?,?,?,?,?)""", (wid, body.request_id, actor, row["contractor"], "ASSIGNED"))
            _event(db, wid, actor, "CREATED")
            created = db.execute("SELECT * FROM staging_workorders WHERE id=?", (wid,)).fetchone()
        return _response(created)

    @app.get("/staging/workorders/{workorder_id}")
    def get_workorder(workorder_id: str, actor: str = Depends(actor_dependency)):
        with _db(db_path) as db:
            return _response(_load(db, workorder_id, actor))

    @app.post("/staging/workorders/{workorder_id}/complete")
    def submit_completion(workorder_id: str, body: SyntheticEvidence,
                          actor: str = Depends(actor_dependency)):
        _require_role(actor, "contractor")
        with _db(db_path) as db:
            db.execute("BEGIN IMMEDIATE")
            row = _load(db, workorder_id, actor)
            if row["contractor"] != actor:
                raise HTTPException(404, "Staging workorder not found")
            if row["state"] not in ("ASSIGNED", "REWORK_REQUESTED"):
                raise HTTPException(409, "Workorder not awaiting synthetic completion")
            db.execute("""UPDATE staging_workorders SET state='SUBMITTED_FOR_REVIEW',
                          completion_evidence_ref=?,acceptance_evidence_ref=NULL WHERE id=?""",
                       (body.evidence_ref, workorder_id))
            _event(db, workorder_id, actor,
                   "RESUBMITTED" if row["state"] == "REWORK_REQUESTED" else "SUBMITTED")
            updated = db.execute("SELECT * FROM staging_workorders WHERE id=?", (workorder_id,)).fetchone()
        return _response(updated)

    @app.post("/staging/workorders/{workorder_id}/decide")
    def decide(workorder_id: str, body: SyntheticDecision, actor: str = Depends(actor_dependency)):
        _require_role(actor, "customer")
        with _db(db_path) as db:
            db.execute("BEGIN IMMEDIATE")
            row = _load(db, workorder_id, actor)
            if row["customer"] != actor:
                raise HTTPException(404, "Staging workorder not found")
            if row["state"] != "SUBMITTED_FOR_REVIEW":
                raise HTTPException(409, "Workorder not awaiting simulated acceptance")
            status = "SIMULATED_ACCEPTED" if body.decision == "ACCEPT" else "REWORK_REQUESTED"
            db.execute("""UPDATE staging_workorders SET state=?,acceptance_evidence_ref=? WHERE id=?""",
                       (status, body.evidence_ref, workorder_id))
            _event(db, workorder_id, actor, status)
            updated = db.execute("SELECT * FROM staging_workorders WHERE id=?", (workorder_id,)).fetchone()
        return _response(updated)

    @app.get("/staging/workorders/{workorder_id}/events")
    def workorder_events(workorder_id: str, actor: str = Depends(actor_dependency)):
        with _db(db_path) as db:
            _load(db, workorder_id, actor)
            rows = db.execute("""SELECT actor,event,created_at FROM staging_workorder_events
                                 WHERE workorder_id=? ORDER BY id ASC""", (workorder_id,)).fetchall()
            return [dict(x) for x in rows]
