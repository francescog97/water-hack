"""D1 adapter. The authenticated gateway supplies identity over a private binding."""
from datetime import datetime, timezone


def check_context(context_id: str):
    if len(context_id) != 64 or any(c not in "0123456789abcdef" for c in context_id):
        raise ValueError("Invalid scenario context fingerprint")


def to_python(value):
    return value.to_py() if hasattr(value, "to_py") else value


class D1ReviewStore:
    def __init__(self, db, email: str):
        self.db, self.email = db, email

    async def acknowledge(self, context_id, item_id, note):
        check_context(context_id)
        now = datetime.now(timezone.utc).isoformat()
        record = await self.db.prepare(
            "INSERT INTO reviews(context_id,item_id,note,acknowledged_at,owner_email) "
            "VALUES(?,?,?,?,?) RETURNING *"
        ).bind(context_id, item_id, note, now, self.email).first()
        if record is None:
            raise RuntimeError("Review was not persisted")
        return to_python(record)

    async def list(self, context_id):
        check_context(context_id)
        result = await self.db.prepare(
            "SELECT * FROM reviews WHERE context_id=? AND owner_email=? ORDER BY id"
        ).bind(context_id, self.email).all()
        return to_python(result.results)
