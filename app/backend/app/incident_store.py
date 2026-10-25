"""Owner-scoped incident snapshots with atomic, optimistic revision updates."""
import json
import sqlite3

from .cloud_store import to_python
from .paths import RUNTIME

SCHEMA = """CREATE TABLE IF NOT EXISTS incidents (
 id TEXT PRIMARY KEY, owner_email TEXT NOT NULL, revision INTEGER NOT NULL,
 snapshot TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
); CREATE INDEX IF NOT EXISTS incidents_owner ON incidents(owner_email, updated_at);"""


class RevisionConflict(ValueError):
    pass


class SQLiteIncidentStore:
    def __init__(self, owner_email="local-demo@localhost"):
        self.owner_email = owner_email

    def connect(self):
        RUNTIME.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(RUNTIME / "incidents.sqlite3")
        db.row_factory = sqlite3.Row
        db.executescript(SCHEMA)
        return db

    async def create(self, incident):
        with self.connect() as db:
            db.execute("INSERT INTO incidents VALUES(?,?,?,?,?,?)", (
                incident["id"], self.owner_email, incident["revision"], json.dumps(incident),
                incident["created_at"], incident["updated_at"]))
        return incident

    async def get(self, incident_id):
        with self.connect() as db:
            row = db.execute("SELECT snapshot FROM incidents WHERE id=? AND owner_email=?",
                             (incident_id, self.owner_email)).fetchone()
        return json.loads(row["snapshot"]) if row else None

    async def list(self):
        with self.connect() as db:
            rows = db.execute("SELECT snapshot FROM incidents WHERE owner_email=? ORDER BY updated_at DESC, id",
                              (self.owner_email,)).fetchall()
        return [json.loads(row["snapshot"]) for row in rows]

    async def save(self, incident, previous_revision):
        with self.connect() as db:
            cursor = db.execute("UPDATE incidents SET revision=?,snapshot=?,updated_at=? "
                                "WHERE id=? AND owner_email=? AND revision=?", (
                                    incident["revision"], json.dumps(incident), incident["updated_at"],
                                    incident["id"], self.owner_email, previous_revision))
            if cursor.rowcount != 1:
                raise RevisionConflict("Incident changed; reload before updating")
        return incident


class D1IncidentStore:
    def __init__(self, db, owner_email):
        self.db, self.owner_email = db, owner_email

    async def create(self, incident):
        row = await self.db.prepare("INSERT INTO incidents VALUES(?,?,?,?,?,?) RETURNING id").bind(
            incident["id"], self.owner_email, incident["revision"], json.dumps(incident),
            incident["created_at"], incident["updated_at"]).first()
        if row is None:
            raise RuntimeError("Incident was not persisted")
        return incident

    async def get(self, incident_id):
        row = await self.db.prepare("SELECT snapshot FROM incidents WHERE id=? AND owner_email=?").bind(
            incident_id, self.owner_email).first()
        return json.loads(to_python(row)["snapshot"]) if row is not None else None

    async def list(self):
        result = await self.db.prepare("SELECT snapshot FROM incidents WHERE owner_email=? ORDER BY updated_at DESC, id").bind(
            self.owner_email).all()
        return [json.loads(row["snapshot"]) for row in to_python(result.results)]

    async def save(self, incident, previous_revision):
        row = await self.db.prepare("UPDATE incidents SET revision=?,snapshot=?,updated_at=? "
                                    "WHERE id=? AND owner_email=? AND revision=? RETURNING id").bind(
                                        incident["revision"], json.dumps(incident), incident["updated_at"],
                                        incident["id"], self.owner_email, previous_revision).first()
        if row is None:
            raise RevisionConflict("Incident changed; reload before updating")
        return incident
