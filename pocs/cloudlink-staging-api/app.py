"""Offline/staging-only CloudLink matching workflow. NOT a public authentication system.
Run: XY_ALLOW_DEMO_API=1 XY_DEMO_CUSTOMER_TOKEN=... XY_DEMO_CONTRACTOR_TOKEN=...
     XY_DEMO_REVIEWER_TOKEN=... XY_DEMO_DB_PATH=/tmp/xy_cloudlink_demo.db
     uvicorn app:create_app --factory --host 127.0.0.1
"""
import json
import os
import re
import secrets
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
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
    # Opt-in, environment-only synthetic identities for cross-account isolation tests.
    # This is NOT a production authentication provider or persisted user registry.
    identities = dict(tokens)
    extra_json = os.getenv("XY_DEMO_ACTORS_JSON")
    if extra_json:
        try:
            extra = json.loads(extra_json)
            if not isinstance(extra, list) or len(extra) > 12:
                raise ValueError("Expected a list with 0-12 actors")
            for item in extra:
                if not isinstance(item, dict) or set(item) != {"id", "role", "token"}:
                    raise ValueError("Each actor requires exactly id, role, token")
                role_name, name, token = item["role"], item["id"], item["token"]
                if role_name not in ("customer", "contractor"):
                    raise ValueError("Extra actor role must be customer or contractor")
                if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,30}", name):
                    raise ValueError("Invalid synthetic actor identifier")
                if not isinstance(token, str) or len(token) < 20:
                    raise ValueError("Synthetic token must contain 20+ characters")
                actor_id = role_name + ":" + name
                if actor_id in identities:
                    raise ValueError("Duplicate synthetic actor identifier")
                identities[actor_id] = token
            if len(set(identities.values())) != len(identities):
                raise ValueError("All synthetic tokens must be distinct")
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError("Invalid XY_DEMO_ACTORS_JSON staging configuration") from exc
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
    # Opt-in synthetic sessions. Bootstrap tokens are exchange-only when on.
    session_mode = os.getenv("XY_STAGING_SESSIONS") == "1"
    sessions = None
    if session_mode:
        from staging_sessions import StagingSessions
        try:
            ttl = int(os.getenv("XY_STAGING_SESSION_TTL", "600"))
            sessions = StagingSessions(path, ttl)
        except (ValueError, TypeError) as exc:
            raise RuntimeError("Invalid isolated staging session configuration") from exc
    app = FastAPI(title="CloudLink controlled staging POC", version="0.4.0")

    @app.middleware("http")
    async def loopback_only(request: Request, call_next):
        source = request.client.host if request.client else ""
        if source not in {"127.0.0.1", "::1", "testclient"}:
            return JSONResponse(status_code=403, content={"detail": "loopback only"})
        return await call_next(request)

    if sessions:
        @app.middleware("http")
        async def audit_actions(request: Request, call_next):
            response = await call_next(request)
            # Only API paths and decisions are logged. Never UUID paths, form
            # contents, query parameters, or Authorization headers.
            route = request.scope.get("route")
            template = getattr(route, "path", None)
            if request.url.path.startswith(("/requests", "/quotes", "/my/", "/review/", "/legacy/", "/staging/")):
                sessions.audit(getattr(request.state, "actor", None), request.method,
                               template or "unmatched", response.status_code)
            return response

    # Same-origin demo UI: NO public hosting, NO persisted tokens, NO real customer data.
    web = Path(__file__).resolve().parent / "web"
    if web.is_dir():
        app.mount("/ui", StaticFiles(directory=str(web)), name="demo-static")

        @app.get("/legacy-staging", include_in_schema=False)
        def legacy_staging_page():
            return FileResponse(str(web / "legacy.html"), headers={"Cache-Control": "no-store"})

        @app.get("/legacy-react", include_in_schema=False)
        def original_cloudlink_react():
            # Explicit opt-in: serve only a separately cloned, modified legacy HTML.
            if os.getenv("XY_ALLOW_LEGACY_REACT") != "1":
                raise HTTPException(status_code=404, detail="Original React staging disabled")
            raw_path = os.getenv("XY_CLOUDLINK_LEGACY_HTML_PATH", "")
            if not raw_path or not Path(raw_path).is_absolute():
                raise HTTPException(status_code=404, detail="Local React HTML not configured")
            legacy_html = Path(raw_path)
            if legacy_html.name != "index.html" or not legacy_html.is_file():
                raise HTTPException(status_code=404, detail="Original React index unavailable")
            return FileResponse(str(legacy_html), headers={"Cache-Control": "no-store"})

        @app.get("/demo", include_in_schema=False)
        def demo_page():
            return FileResponse(str(web / "index.html"), headers={"Cache-Control": "no-store"})


    def role(request: Request, authorization: str | None = Header(default=None)) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bearer test session required")
        presented = authorization[7:]
        if sessions:
            actor = sessions.authenticate(presented)
            if actor is None or actor not in identities:
                raise HTTPException(status_code=401, detail="Invalid or expired staging session")
            request.state.actor = actor
            return actor
        for identity, token in identities.items():
            if secrets.compare_digest(presented, token):
                request.state.actor = identity
                return identity
        raise HTTPException(status_code=401, detail="Invalid demo token")

    @app.post("/staging/session")
    def exchange_session(request: Request, authorization: str | None = Header(default=None)):
        if not sessions:
            raise HTTPException(status_code=404, detail="Staging sessions disabled")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Bootstrap token required")
        presented = authorization[7:]
        for actor, bootstrap in identities.items():
            if secrets.compare_digest(presented, bootstrap):
                request.state.actor = actor
                token, lifetime = sessions.issue(actor)
                return JSONResponse({"access_token": token, "expires_in": lifetime, "token_type": "Bearer"},
                                    headers={"Cache-Control": "no-store"})
        raise HTTPException(status_code=401, detail="Invalid bootstrap token")

    @app.post("/staging/session/revoke")
    def revoke_session(request: Request, actor: str = Depends(role), authorization: str | None = Header(default=None)):
        if not sessions or not authorization or not sessions.revoke(authorization[7:], actor):
            raise HTTPException(status_code=401, detail="Session unavailable")
        return {"revoked": True}

    @app.get("/staging/audit")
    def read_audit(actor: str = Depends(role)):
        if not sessions:
            raise HTTPException(status_code=404, detail="Audit disabled")
        authorize(actor, "reviewer")
        return sessions.recent_events()


    def authorize(actual: str, allowed: str):
        role_name = actual.split(":", 1)[0]
        if role_name != allowed:
            raise HTTPException(status_code=403, detail="Role not allowed")

    @app.get("/health")
    def health():
        return {"ok": True, "environment": "STAGING_DEMO_ONLY", "payments_enabled": False}

    from legacy_schema import LegacyRequest, normalize_legacy_request
    @app.post("/legacy/requests", status_code=201)
    def create_legacy_request(body: LegacyRequest, actor: str = Depends(role)):
        return create_request(NewRequest(**normalize_legacy_request(body)), actor=actor)

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

    @app.get("/my/requests")
    def my_requests(actor: str = Depends(role)):
        authorize(actor, "customer")
        with connection(path) as db:
            rows = db.execute("""SELECT id,category,region,description,state,selected_quote
                                 FROM requests WHERE customer=? ORDER BY rowid DESC""", (actor,)).fetchall()
        return [dict(r) for r in rows]

    @app.get("/review/requests")
    def review_requests(actor: str = Depends(role)):
        authorize(actor, "reviewer")
        with connection(path) as db:
            rows = db.execute("""SELECT id,category,region,description,state
                                 FROM requests WHERE state='PENDING' ORDER BY rowid DESC""").fetchall()
        return [dict(r) for r in rows]

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

    @app.get("/my/quotes")
    def my_quotes(actor: str = Depends(role)):
        authorize(actor, "contractor")
        with connection(path) as db:
            rows = db.execute("""SELECT id,request_id,price_ntd,scope
                                 FROM quotes WHERE contractor=? ORDER BY rowid DESC""",
                              (actor,)).fetchall()
        return [dict(r) for r in rows]

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
