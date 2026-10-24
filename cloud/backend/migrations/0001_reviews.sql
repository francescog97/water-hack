CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    note TEXT NOT NULL,
    acknowledged_at TEXT NOT NULL,
    review_kind TEXT NOT NULL DEFAULT 'OPERATOR_ACKNOWLEDGEMENT',
    legal_authorization INTEGER NOT NULL DEFAULT 0 CHECK (legal_authorization = 0),
    owner_email TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS reviews_owner_context ON reviews(owner_email, context_id);
