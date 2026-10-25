import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.backend.app.main import app
from app.backend.app.paths import ROOT

EMAIL = "francescogabrielg@gmail.com"
ORIGIN = "https://crisis2action.spunto-speak.workers.dev"


class Statement:
    def __init__(self, db, sql):
        self.db, self.sql, self.params = db, sql, ()

    def bind(self, *params):
        self.params = params
        return self

    async def first(self):
        row = self.db.execute(self.sql, self.params).fetchone()
        self.db.commit()
        return dict(row) if row else None

    async def all(self):
        return SimpleNamespace(results=[dict(r) for r in self.db.execute(self.sql, self.params).fetchall()])


def cloud_client(tmp_path):
    db = sqlite3.connect(tmp_path / "d1.sqlite3", check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / "cloud/backend/migrations/0001_reviews.sql").read_text())
    binding = SimpleNamespace(prepare=lambda sql: Statement(db, sql))
    env = SimpleNamespace(DEPLOYMENT_MODE="private-cloud-backend", PUBLIC_ORIGIN=ORIGIN,
                          ALLOWED_EMAILS=EMAIL + ",second@example.com", DB=binding)

    async def worker(scope, receive, send):
        scope["env"] = env
        await app(scope, receive, send)

    return TestClient(worker, base_url="https://crisis2action-api.internal", headers={
        "x-c2a-user-email": EMAIL, "Origin": ORIGIN,
    }), db


def test_cloud_private_boundary_and_origin(tmp_path):
    client, db = cloud_client(tmp_path)
    assert client.get("/api/cases", headers={"x-c2a-user-email": "attacker@example.com"}).status_code == 403
    assert client.get("/api/cases", headers={"x-c2a-user-email": ""}).status_code == 403
    assert client.get("/api/cases", headers={"host": "external.example"}).status_code == 403
    assert client.post("/api/evaluate", json={}, headers={"Origin": "https://other.example"}).status_code == 403
    assert client.get("/api/health").json()["mode"] == "private-cloud-historical-demo"
    db.close()


def test_cloud_review_persistence_owner_isolation_and_briefing(tmp_path):
    client, db = cloud_client(tmp_path)
    scenario = {"simulate": True}
    evaluation = client.post("/api/evaluate", json=scenario).json()
    assert evaluation["classification"]["band"] == "DANGER"
    review = client.post("/api/reviews", json={
        "context_id": evaluation["context_id"], "item_id": "scenario-review",
        "note": "Historical evidence reviewed; current law still needs expert review.", "acknowledged": True,
    })
    assert review.status_code == 200
    record = review.json()
    assert record["owner_email"] == EMAIL
    assert db.execute("SELECT COUNT(*) FROM reviews").fetchone()[0] == 1
    path = f"/api/reviews/{evaluation['context_id']}"
    assert client.get(path).json()[0]["id"] == record["id"]
    assert client.get(path, headers={"x-c2a-user-email": "second@example.com"}).json() == []
    body = {"scenario": scenario, "review_ids": [record["id"]]}
    result = client.post("/api/briefings", json=body)
    assert result.status_code == 200
    assert result.json()["official_authorization"] is False
    assert "https://" in result.json()["markdown"]
    assert client.post("/api/briefings", json=body, headers={"x-c2a-user-email": "second@example.com"}).status_code == 409
    body["scenario"]["rule_pack_id"] = "alternate-demo"
    assert client.post("/api/briefings", json=body).status_code == 409
    db.close()


def test_cloud_bundle_matches_original_sources_and_no_private_extras():
    manifest = json.loads((ROOT / "cloud/data-manifest.json").read_text())
    import hashlib
    expected = {"Dataset/portata_iskar_novi_iskar_2025.csv", "Dataset/portata_iskar_orehovitsa_2025.csv"}
    assert {name for name in manifest if name.startswith("Dataset/")} == expected
    assert len(manifest) == 7
    assert "app/config/incidents/iskar-pollution-demo.json" in manifest
    for name, digest in manifest.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    assert all(Path(name).suffix in {".json", ".csv"} for name in manifest)
