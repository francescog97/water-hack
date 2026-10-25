import sqlite3
import json
from types import SimpleNamespace

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.backend.app import incident_store, incidents
from app.backend.app.paths import ROOT


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(incident_store, "RUNTIME", tmp_path)
    app = FastAPI()
    app.include_router(incidents.router)
    return TestClient(app)


def create(client):
    response = client.post("/api/incidents", json={"scenario_id": incidents.SCENARIO_ID})
    assert response.status_code == 200, response.text
    return response.json()


def update(client, incident, task, status="completed"):
    return client.patch(f"/api/incidents/{incident['id']}/tasks/{task['id']}", json={
        "status": status, "assignee_name": "Demo analyst", "assignee_role": "Technical specialist",
        "note": "Self-recorded exercise check; no external verification asserted.",
        "expected_revision": incident["revision"],
    })


def review_body():
    return {"decision": "demo_approved", "reviewer_name": "Demo reviewer", "reviewer_role": "Technical reviewer",
            "note": "Exercise reviewed with unconfirmed evidence and external authority checks outstanding.", "acknowledged": True}


def test_complete_demo_workflow_and_invalidation(client):
    incident = create(client)
    path = f"/api/incidents/{incident['id']}"
    assert incident["finding_status"] == "UNCONFIRMED_ANOMALY"
    assert client.post(path + "/review", json=review_body()).status_code == 409
    response_task = next(t for t in incident["tasks"] if t["kind"] == "response")
    assert update(client, incident, response_task).status_code == 409
    for task in incident["tasks"]:
        if task["required_for_review"]:
            response = update(client, incident, task)
            assert response.status_code == 200, response.text
            incident = response.json()
    response = client.post(path + "/review", json=review_body())
    assert response.status_code == 200, response.text
    incident = response.json()
    assert incident["review_status"] == "demo_approved"
    assert incident["reviews"][-1]["legal_authorization"] is False
    for task in incident["tasks"]:
        if task["status"] != "completed":
            incident = update(client, incident, task).json()
    response = client.post(path + "/outcome", json={"status": "closed_demo", "note": "Demonstration workflow completed."})
    assert response.status_code == 200
    assert response.json()["outcome"]["pollution_confirmed"] is False
    assert update(client, response.json(), response_task).status_code == 409
    incident = client.post(path + "/outcome", json={"status": "monitoring", "note": "Reopen exercise for correction."}).json()
    verification = next(t for t in incident["tasks"] if t["kind"] == "verification")
    incident = update(client, incident, verification, "blocked").json()
    assert incident["review_status"] == "pending"
    assert update(client, incident, response_task).status_code == 409
    exported = client.get(path + "/export").json()
    assert exported["official_authorization"] is False
    assert "UNCONFIRMED_ANOMALY" in exported["markdown"]
    assert "NOT_ASSIGNED" in exported["markdown"]
    assert len(exported["incident"]["timeline"]) > len(incident["tasks"])


def test_validation_stale_updates_and_no_official_states(client):
    incident = create(client)
    path = f"/api/incidents/{incident['id']}"
    task = incident["tasks"][0]
    assert client.patch(path + f"/tasks/{task['id']}", json={"status": "completed", "note": "Check performed"}).status_code == 422
    updated = update(client, incident, task)
    assert updated.status_code == 200
    assert update(client, incident, task).status_code == 409
    assert client.post(path + "/review", json={**review_body(), "acknowledged": False}).status_code == 422
    assert client.post(path + "/outcome", json={"status": "confirmed_pollution", "note": "Should never become confirmed"}).status_code == 422
    assert client.patch(path + f"/tasks/{task['id']}", json={"status": "dispatched", "note": "No dispatch allowed"}).status_code == 422
    assert client.post(path + "/outcome", json={"status": "closed_demo", "note": "Missing current review"}).status_code == 409
    closed = client.post(path + "/outcome", json={"status": "closed_unconfirmed", "note": "Natural cause remains plausible; exercise ended."}).json()
    assert closed["outcome"]["legal_violation_established"] is False
    assert client.get(path).json()["revision"] == closed["revision"]
    assert client.post("/api/incidents", json={"scenario_id": "../../secret"}).status_code == 422


def test_missing_scenario_fails_without_synthetic_fallback(client, tmp_path, monkeypatch):
    monkeypatch.setattr(incidents, "CONFIG", tmp_path)
    assert client.get("/api/incidents/scenario").status_code == 422
    assert client.post("/api/incidents", json={}).status_code == 422
    assert client.get("/api/incidents").json() == []


def altered_config(tmp_path, monkeypatch, change):
    scenario = json.loads((ROOT / "app/config/incidents/iskar-pollution-demo.json").read_text(encoding="utf-8"))
    change(scenario)
    folder = tmp_path / "incidents"
    folder.mkdir(exist_ok=True)
    (folder / "iskar-pollution-demo.json").write_text(json.dumps(scenario), encoding="utf-8")
    monkeypatch.setattr(incidents, "CONFIG", tmp_path)


@pytest.mark.parametrize("field,value", [
    ("baseline", 0), ("baseline", -1), ("baseline", float("nan")),
    ("value", -1), ("value", float("inf")), ("value", True), ("value", "96"),
    ("threshold", float("inf")), ("threshold", -1), ("unit", "NTU"),
    ("parameter", "PFAS"), ("lab_confirmation", "CONFIRMED"),
    ("threshold_classification", "STATUTORY"), ("comparator", "<="),
])
def test_observation_invalid_inputs_fail_closed(client, tmp_path, monkeypatch, field, value):
    altered_config(tmp_path, monkeypatch, lambda s: s["observation"].update({field: value}))
    assert client.get("/api/incidents/scenario").status_code == 422
    assert client.post("/api/incidents", json={}).status_code == 422
    assert client.get("/api/incidents").json() == []


@pytest.mark.parametrize("value,expected_status", [(30, "DEMO_TRIGGER_EXCEEDED"), (12, "NO_DEMO_TRIGGER"), (0, "NO_DEMO_TRIGGER")])
def test_anomaly_and_ratio_derived_from_validated_inputs(client, tmp_path, monkeypatch, value, expected_status):
    altered_config(tmp_path, monkeypatch, lambda s: s["observation"].update(value=value, baseline=4, ratio=999999))
    result = client.get("/api/incidents/scenario").json()["observation"]
    assert result["ratio"] == value / 4
    assert result["anomaly_status"] == expected_status
    assert result["statutory_limit"] is False
    assert result["pollution_confirmed"] is False
    incident = create(client)
    assert incident["finding_status"] == ("UNCONFIRMED_ANOMALY" if value >= 30 else "NO_DEMO_TRIGGER")
    assert incident["official_authorization"] is False


@pytest.mark.parametrize("change", [
    lambda s: s["observation"].pop("value"),
    lambda s: s["observation"].update(value=1e308, baseline=1e-308),
    lambda s: s.update(sources=[]),
    lambda s: s.update(legal_checks=[]),
    lambda s: s.update(authorities=[]),
    lambda s: s["tasks"][0].update(source_ids=["missing-source"]),
    lambda s: s["sources"][0].update(url="javascript:alert(1)"),
    lambda s: s["sources"][0].update(url="https://user:password@example.com/"),
    lambda s: s["sources"][0].update(verification="EXPERT_VERIFIED", reviewer="Claimed reviewer"),
    lambda s: s["legal_checks"][0].update(statutory_claim=True),
    lambda s: s["legal_checks"][0].update(deadline_value="24 hours"),
    lambda s: s["authorities"][0].update(institution_assignment="ASSIGNED"),
])
def test_missing_provenance_and_unsupported_verified_claims_fail_closed(client, tmp_path, monkeypatch, change):
    altered_config(tmp_path, monkeypatch, change)
    assert client.get("/api/incidents/scenario").status_code == 422
    assert client.post("/api/incidents", json={}).status_code == 422


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


def test_cloud_owner_isolation_no_local_fallback_and_revision_atomicity(tmp_path, monkeypatch):
    monkeypatch.setattr(incident_store, "RUNTIME", tmp_path / "must-not-exist")
    db = sqlite3.connect(tmp_path / "d1.sqlite3", check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / "cloud/backend/migrations/0002_incidents.sql").read_text())
    binding = SimpleNamespace(prepare=lambda sql: Statement(db, sql))
    app = FastAPI()

    @app.middleware("http")
    async def identity(request: Request, call_next):
        request.scope["env"] = SimpleNamespace(DB=binding)
        # This test harness models already verified gateway identities.
        if request.headers.get("x-test-verified-owner"):
            request.state.incident_store = incident_store.D1IncidentStore(binding, request.headers["x-test-verified-owner"])
        return await call_next(request)

    app.include_router(incidents.router)
    owner = TestClient(app, headers={"x-test-verified-owner": "owner@example.com"})
    other = TestClient(app, headers={"x-test-verified-owner": "other@example.com"})
    anonymous = TestClient(app)
    incident = create(owner)
    path = f"/api/incidents/{incident['id']}"
    assert other.get(path).status_code == 404
    assert other.get("/api/incidents").json() == []
    assert other.post(path + "/review", json=review_body()).status_code == 404
    assert other.get(path + "/export").status_code == 404
    assert anonymous.get("/api/incidents").status_code == 403
    assert update(owner, incident, incident["tasks"][0]).status_code == 200
    assert update(owner, incident, incident["tasks"][0]).status_code == 409
    assert not (tmp_path / "must-not-exist").exists()
    assert db.execute("SELECT owner_email FROM incidents").fetchone()[0] == "owner@example.com"
    db.close()


def test_main_private_middleware_incident_boundary_and_owner_isolation(tmp_path, monkeypatch):
    from app.backend.app.main import app

    monkeypatch.setattr(incident_store, "RUNTIME", tmp_path / "no-cloud-fallback")
    db = sqlite3.connect(tmp_path / "main-d1.sqlite3", check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.executescript((ROOT / "cloud/backend/migrations/0002_incidents.sql").read_text())
    binding = SimpleNamespace(prepare=lambda sql: Statement(db, sql))
    origin = "https://navigator.example"
    env = SimpleNamespace(DEPLOYMENT_MODE="private-cloud-backend", DB=binding,
                          PUBLIC_ORIGIN=origin, ALLOWED_EMAILS="one@example.com,two@example.com")

    async def worker(scope, receive, send):
        scope["env"] = env
        await app(scope, receive, send)

    owner = TestClient(worker, base_url="https://crisis2action-api.internal",
                       headers={"x-c2a-user-email": "one@example.com", "Origin": origin})
    incident = create(owner)
    path = f"/api/incidents/{incident['id']}"
    assert owner.get(path).status_code == 200
    assert owner.get(path, headers={"x-c2a-user-email": "two@example.com"}).status_code == 404
    assert owner.get("/api/incidents", headers={"x-c2a-user-email": "two@example.com"}).json() == []
    assert owner.get(path + "/export", headers={"x-c2a-user-email": "two@example.com"}).status_code == 404
    assert owner.post(path + "/outcome", headers={"x-c2a-user-email": "two@example.com"},
                      json={"status": "closed_unconfirmed", "note": "Attempt another owner incident"}).status_code == 404
    assert owner.get(path, headers={"x-c2a-user-email": "attacker@example.com"}).status_code == 403
    assert owner.get(path, headers={"x-c2a-user-email": ""}).status_code == 403
    assert owner.get(path, headers={"host": "public.example"}).status_code == 403
    assert owner.post("/api/incidents", headers={"Origin": "https://untrusted.example"}, json={}).status_code == 403
    assert not (tmp_path / "no-cloud-fallback").exists()
    assert db.execute("SELECT owner_email FROM incidents").fetchone()[0] == "one@example.com"
    db.close()


def approved_incident(client):
    incident = create(client)
    for task in incident["tasks"]:
        if task["required_for_review"]:
            incident = update(client, incident, task).json()
    response = client.post(f"/api/incidents/{incident['id']}/review", json=review_body())
    assert response.status_code == 200
    return response.json()


def test_rejected_response_requires_explicit_reset_and_renewed_review(client):
    incident = approved_incident(client)
    task = next(t for t in incident["tasks"] if t["kind"] == "response")
    incident = update(client, incident, task, "rejected").json()
    revision = incident["revision"]
    for status in ["specialist_approved", "in_progress", "completed", "blocked"]:
        assert update(client, incident, task, status).status_code == 409
    path = f"/api/incidents/{incident['id']}"
    assert client.get(path).json()["revision"] == revision
    # Reset is an accountable reconsideration, never an implicit approval.
    assert client.patch(path + f"/tasks/{task['id']}", json={"status": "system_suggested", "note": ""}).status_code == 422
    incident = update(client, incident, task, "system_suggested").json()
    assert incident["review_status"] == "pending"
    assert update(client, incident, task, "in_progress").status_code == 409
    incident = client.post(path + "/review", json=review_body()).json()
    assert update(client, incident, task, "in_progress").status_code == 200


def test_timeline_records_actual_mutation_revision_and_keeps_legacy_unknown(client):
    incident = approved_incident(client)
    assert incident["timeline"][0]["revision"] == 1
    verification = next(t for t in incident["tasks"] if t["kind"] == "verification")
    previous = incident["revision"]
    incident = update(client, incident, verification, "blocked").json()
    assert incident["revision"] == previous + 1
    assert [event["kind"] for event in incident["timeline"][-2:]] == ["review_invalidated", "task_updated"]
    assert all(event["revision"] == incident["revision"] for event in incident["timeline"][-2:])
    # Simulate an existing persisted record created before event revisions existed.
    store = incident_store.SQLiteIncidentStore()
    with store.connect() as db:
        incident["timeline"][0].pop("revision")
        db.execute("UPDATE incidents SET snapshot=? WHERE id=?", (json.dumps(incident), incident["id"]))
    exported = client.get(f"/api/incidents/{incident['id']}/export").json()
    assert "revision not recorded" in exported["markdown"]
    assert "revision" not in exported["incident"]["timeline"][0]


def test_internal_target_persists_preserves_and_explicit_null_clears(client):
    incident = create(client)
    task = incident["tasks"][0]
    assert task["internal_target_at"] is None
    assert task["internal_target_classification"] == "USER_SET_DEMO_TARGET_NOT_STATUTORY"
    path = f"/api/incidents/{incident['id']}"
    body = {"status": "system_suggested", "note": "Set internal exercise target", "internal_target_at": "2026-10-26T12:30:00+02:00"}
    response = client.patch(path + f"/tasks/{task['id']}", json=body)
    assert response.status_code == 200, response.text
    incident = response.json()
    expected = "2026-10-26T12:30:00+02:00"
    assert incident["tasks"][0]["internal_target_at"] == expected
    incident = update(client, incident, task).json()
    assert incident["tasks"][0]["internal_target_at"] == expected
    assert client.get(path).json()["tasks"][0]["internal_target_at"] == expected
    exported = client.get(path + "/export").json()
    assert expected in exported["markdown"]
    assert "USER_SET_DEMO_TARGET_NOT_STATUTORY" in exported["markdown"]
    assert all(check["deadline_value"] is None for check in incident["scenario"]["legal_checks"])
    incident = client.patch(path + f"/tasks/{task['id']}", json={**body, "internal_target_at": None}).json()
    assert incident["tasks"][0]["internal_target_at"] is None
    event = incident["timeline"][-1]
    assert event["previous_internal_target_at"] == expected
    assert event["internal_target_at"] is None
    assert event["internal_target_classification"] == "USER_SET_DEMO_TARGET_NOT_STATUTORY"


@pytest.mark.parametrize("target", ["2026-10-26T12:30:00", "2026-10-26", "not-a-date", "2026-13-50T25:00:00Z"])
def test_internal_target_requires_valid_timezone_aware_datetime(client, target):
    incident = create(client)
    task = incident["tasks"][0]
    response = client.patch(f"/api/incidents/{incident['id']}/tasks/{task['id']}", json={
        "status": "system_suggested", "note": "Invalid date must not persist", "internal_target_at": target})
    assert response.status_code == 422
    assert client.get(f"/api/incidents/{incident['id']}").json()["revision"] == 1


def test_markdown_draft_preserves_evidence_review_and_outcome(client):
    incident = approved_incident(client)
    path = f"/api/incidents/{incident['id']}"
    incident = client.post(path + "/outcome", json={"status": "closed_unconfirmed", "note": "Laboratory evidence absent; retain uncertainty."}).json()
    exported = client.get(path + "/export").json()
    markdown = exported["markdown"]
    observation = incident["scenario"]["observation"]
    for value in [observation["unit"], observation["observed_at"], observation["baseline_observed_at"],
                  observation["mode"], observation["sample_id"], "DEMO_CONFIG", "UNVERIFIED",
                  "PENDING_EXPERT_CONFIRMATION", "SOURCE_LOCATED_UNREVIEWED", "NONE_VERIFIED",
                  "Demo reviewer", "Technical reviewer", review_body()["note"],
                  "Laboratory evidence absent; retain uncertainty.", "pollution_confirmed", "legal_violation_established"]:
        assert value in markdown
    for collection in ["receptors", "authorities", "legal_checks", "sources"]:
        for item in incident["scenario"][collection]:
            assert item["id"] in markdown
    assert '"value": 96.0' in markdown
    assert '"threshold": 30.0' in markdown
    assert exported["incident"] == incident
    assert exported["official_authorization"] is False
    assert "no verified statutory duties" in markdown
