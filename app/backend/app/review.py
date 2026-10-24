import sqlite3
from datetime import datetime, timezone

from .paths import RUNTIME


def connect():
    RUNTIME.mkdir(exist_ok=True)
    db = sqlite3.connect(RUNTIME / "reviews.sqlite3")
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        context_id TEXT NOT NULL, item_id TEXT NOT NULL,
        note TEXT NOT NULL, acknowledged_at TEXT NOT NULL,
        review_kind TEXT NOT NULL DEFAULT 'OPERATOR_ACKNOWLEDGEMENT',
        legal_authorization INTEGER NOT NULL DEFAULT 0)""")
    return db


def acknowledge(context_id, item_id, note):
    if len(context_id) != 64 or any(c not in "0123456789abcdef" for c in context_id):
        raise ValueError("Invalid scenario context fingerprint")
    now = datetime.now(timezone.utc).isoformat()
    with connect() as db:
        cursor = db.execute("INSERT INTO reviews(context_id,item_id,note,acknowledged_at) VALUES(?,?,?,?)",
                            (context_id, item_id, note, now))
        record = dict(db.execute("SELECT * FROM reviews WHERE id=?", (cursor.lastrowid,)).fetchone())
    return record


def list_reviews(context_id):
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM reviews WHERE context_id=? ORDER BY id", (context_id,))]
