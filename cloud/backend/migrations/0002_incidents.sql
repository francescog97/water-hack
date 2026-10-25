CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    owner_email TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK (revision >= 1),
    snapshot TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS incidents_owner ON incidents(owner_email, updated_at);
