"""Isolated-only, opt-in session lifecycle for synthetic YC Tech Match accounts.

No user enrollment, password authentication, HTTPS, OAuth, DB-backed tenancy,
or real-person identities. NEVER expose on public interfaces or reuse in production.
"""
import hashlib
import secrets
import sqlite3
import time
from pathlib import Path


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class StagingSessions:
    def __init__(self, database_path: str, ttl_seconds: int = 600):
        if not 5 <= ttl_seconds <= 900:
            raise ValueError("Session TTL must be between 5 and 900 seconds")
        if not Path(database_path).is_absolute() or not Path(database_path).parent.is_dir():
            raise ValueError("An isolated absolute SQLite path is required")
        self.path = database_path
        self.ttl_seconds = ttl_seconds
        with self._db() as db:
            db.executescript("""
              CREATE TABLE IF NOT EXISTS staging_sessions (
                token_hash TEXT PRIMARY KEY, actor TEXT NOT NULL,
                expires_at INTEGER NOT NULL, revoked_at INTEGER
              );
              CREATE TABLE IF NOT EXISTS staging_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at INTEGER NOT NULL, actor TEXT NOT NULL,
                method TEXT NOT NULL, route TEXT NOT NULL,
                status INTEGER NOT NULL
              );
            """)

    def _db(self):
        from contextlib import contextmanager

        @contextmanager
        def connect():
            db = sqlite3.connect(self.path, timeout=5)
            db.row_factory = sqlite3.Row
            try:
                yield db
                db.commit()
            finally:
                db.close()
        return connect()

    def issue(self, actor: str) -> tuple[str, int]:
        token = secrets.token_urlsafe(32)
        expires_at = int(time.time()) + self.ttl_seconds
        with self._db() as db:
            db.execute("INSERT INTO staging_sessions(token_hash,actor,expires_at) VALUES(?,?,?)",
                       (_hash(token), actor, expires_at))
        return token, self.ttl_seconds

    def authenticate(self, token: str) -> str | None:
        if not isinstance(token, str) or not 20 <= len(token) <= 256:
            return None
        with self._db() as db:
            row = db.execute("SELECT actor,expires_at,revoked_at FROM staging_sessions WHERE token_hash=?",
                             (_hash(token),)).fetchone()
        if row is None or row["revoked_at"] is not None or int(time.time()) >= row["expires_at"]:
            return None
        return str(row["actor"])

    def revoke(self, token: str, actor: str) -> bool:
        with self._db() as db:
            cursor = db.execute("""UPDATE staging_sessions SET revoked_at=?
                                   WHERE token_hash=? AND actor=? AND revoked_at IS NULL""",
                                (int(time.time()), _hash(token), actor))
        return cursor.rowcount == 1

    def audit(self, actor: str | None, method: str, route: str, status: int) -> None:
        # Only the route template, never request bodies or raw Authorization headers.
        with self._db() as db:
            db.execute("INSERT INTO staging_audit(created_at,actor,method,route,status) VALUES(?,?,?,?,?)",
                       (int(time.time()), actor or "anonymous", method[:12], route[:120], status))

    def recent_events(self, limit: int = 30) -> list[dict]:
        with self._db() as db:
            events = db.execute("""SELECT created_at,actor,method,route,status
                                   FROM staging_audit ORDER BY id DESC LIMIT ?""",
                                (max(1, min(limit, 100)),)).fetchall()
        return [dict(event) for event in events]
