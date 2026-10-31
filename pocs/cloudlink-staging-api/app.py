"""Offline/staging-only CloudLink matching workflow. NOT a public authentication system.
Run: XY_ALLOW_DEMO_API=1 XY_DEMO_CUSTOMER_TOKEN=... XY_DEMO_CONTRACTOR_TOKEN=...
     XY_DEMO_REVIEWER_TOKEN=... XY_DEMO_DB_PATH=/tmp/xy_cloudlink_demo.db
     uvicorn app:create_app --factory --host 127.0.0.1
"""
import os
import secrets
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

Category = Literal["network", "cctv", "access"]


class NewRequest(BaseModel):
    category: Category
    region: str = Field(min_length=2, max_length=60)
    description: str = Field(min_length=12, max_length=1000)


class NewQuote(BaseModel):
    request_id: str
    price_ntd: int = Field(gt=0, le=10_000_000)
    scope: str = Field(min_length=10, max_length=1000)


class Review(BaseModel):
    decision: Literal["APPROVED", "REJECTED"]


@contextmanager
def connection(db_path: str):
    db = sqlite3.connect(db_path, timeout=5)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    finally:
        db.close()


def create_app() -> FastAPI:
    if os.getenv("XY_ALLOW_DEMO_API") != "1":
        raise RuntimeError("Demo API locked: XY_ALLOW_DEMO_API=1 required")
    tokens = {
        "customer": os.getenv("XY_DEMO_CUSTOMER_TOKEN", ""),
        "contractor": os.getenv("XY_DEMO_CONTRACTOR_TOKEN", ""),
        "reviewer": os.getenv("XY_DEMO_REVIEWER_TOKEN", ""),
    }
    if any(len(v) < 20 for v in tokens.values()) or len(set(tokens.values())) != 3:
        raise RuntimeError("Three distinct 20+ character demo tokens required")
    path = os.getenv("XY_DEMO_DB_PATH", "")
    if not path or path == ":memory:":
        raise RuntimeError("Explicit isolated SQLite file path required")
    if not Path(path).parent.is_dir():
        raise RuntimeError("Database directory does not exist")
    with connection(path) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS requests (
          id TEXT PRIMARY KEY, customer TEXT NOT NULL, category TEXT NOT NULL,
          region TEXT NOT NULL, description TEXT NOT NULL,
          state TEXT NOT NULL CHECK(state IN ('PENDING','APPROVED','REJECTED','SELECTED')),
          selected_quote TEXT);
        CREATE TABLE IF NOT EXISTS quotes (
          id TEXT PRIMARY KEY, request_id TEXT NOT NULL, contractor TEXT NOT NULL,
          price_ntd INTEGER NOT NULL, scope TEXT NOT NULL,
          FOREIGN KEY(request_id) REFERENCES requests(id));
        """)
    app = FastAPI(title="CloudLink controlled staging POC", version="0.1.0")

    def role(authorization: str | None = Header(default=None)) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bearer demo token required")
        presented = authorization[7:]
        for identity, token in tokens.items():
            if secrets.compare_digest(presented, token):
                return identity
        raise HTTPException(status_code=401, detail="Invalid demo token")

    def authorize(actual: str, allowed: str):
        if actual != allowed:
            raise HTTPException(status_code=403, detail="Role not allowed")

    @app.get("/health")
    def health():
        return {"ok": True, "environment": "STAGING_DEMO_ONLY", "payments_enabled": False}

    @app.post("/requests", status_code=201)
    def create_request(body: NewRequest, actor: str = Depends(role)):
        authorize(actor, "customer")
        rid = str(uuid4())
        with connection(path) as db:
            db.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?)",
                       (rid, actor, body.category, body.region, body.description, "PENDING", None))
        return {"id": rid, "state": "PENDING"}

    @app.post("/requests/{request_id}/moderate")
    def moderate(request_id: str, body: Review, actor: str = Depends(role)):
        authorize(actor, "reviewer")
        with connection(path) as db:
            cur = db.execute("UPDATE requests SET state=? WHERE id=? AND state='PENDING'",
                             (body.decision, request_id))
            if cur.rowcount != 1:
                raise HTTPException(status_code=409, detail="Not pending or not found")
        return {"id": request_id, "state": body.decision}

    @app.get("/requests")
    def get_requests(actor: str = Depends(role)):
        authorize(actor, "contractor")
        with connection(path) as db:
            rows = db.execute("SELECT id,category,region,description,state FROM requests WHERE state='APPROVED'").fetchall()
        return [dict(r) for r in rows]

    @app.post("/quotes", status_code=201)
    def create_quote(body: NewQuote, actor: str = Depends(role)):
        authorize(actor, "contractor")
        qid = str(uuid4())
        with connection(path) as db:
            state = db.execute("SELECT state FROM requests WHERE id=?", (body.request_id,)).fetchone()
            if not state or state["state"] != "APPROVED":
                raise HTTPException(status_code=409, detail="Request not approved")
            db.execute("INSERT INTO quotes VALUES (?,?,?,?,?)",
                       (qid, body.request_id, actor, body.price_ntd, body.scope))
        return {"id": qid, "request_id": body.request_id}

    @app.get("/requests/{request_id}/quotes")
    def get_quotes(request_id: str, actor: str = Depends(role)):
        authorize(actor, "customer")
        with connection(path) as db:
            found = db.execute("SELECT customer FROM requests WHERE id=?", (request_id,)).fetchone()
            if not found or found["customer"] != actor:
                raise HTTPException(status_code=404, detail="Request not found")
            rows = db.execute("SELECT id,price_ntd,scope FROM quotes WHERE request_id=?", (request_id,)).fetchall()
        return [dict(r) for r in rows]

    @app.post("/quotes/{quote_id}/select")
    def select_quote(quote_id: str, actor: str = Depends(role)):
        authorize(actor, "customer")
        with connection(path) as db:
            db.execute("BEGIN IMMEDIATE")
            found = db.execute("""SELECT q.request_id,r.customer,r.state FROM quotes q
                                  JOIN requests r ON q.request_id=r.id WHERE q.id=?""",
                               (quote_id,)).fetchone()
            if not found or found["customer"] != actor:
                raise HTTPException(status_code=404, detail="Quote not found")
            if found["state"] != "APPROVED":
                raise HTTPException(status_code=409, detail="Request already selected")
            db.execute("UPDATE requests SET state='SELECTED',selected_quote=? WHERE id=?",
                       (quote_id, found["request_id"]))
        return {"request_id": found["request_id"], "selected_quote": quote_id, "state": "SELECTED"}

    return app
