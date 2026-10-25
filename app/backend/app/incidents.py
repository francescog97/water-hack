"""Demonstration verification workflow; never establishes pollution or legal powers."""
import hashlib
import json
import math
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4
from urllib.parse import urlsplit

from fastapi import APIRouter, HTTPException, Request
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .incident_store import RevisionConflict, SQLiteIncidentStore
from .paths import CONFIG

router = APIRouter(prefix="/api/incidents", tags=["Demonstration incidents"])
SCENARIO_ID = "iskar-pollution-demo"
DEMO_NOTICE = "Self-recorded demonstration review and assignments only; no verified institutional appointment, statutory authorization, notification or dispatch."


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CreateIncident(StrictModel):
    scenario_id: Literal["iskar-pollution-demo"] = SCENARIO_ID


class Mutation(StrictModel):
    expected_revision: int | None = Field(default=None, ge=1)
    note: str = Field(min_length=5, max_length=4000)


class TaskMutation(Mutation):
    status: Literal["system_suggested", "specialist_approved", "in_progress", "completed", "rejected", "blocked"]
    assignee_name: str | None = Field(default=None, min_length=2, max_length=120)
    assignee_role: str | None = Field(default=None, min_length=2, max_length=120)
    internal_target_at: AwareDatetime | None = None


class ReviewMutation(Mutation):
    decision: Literal["needs_changes", "demo_approved"]
    reviewer_name: str = Field(min_length=2, max_length=120)
    reviewer_role: str = Field(min_length=2, max_length=120)
    acknowledged: Literal[True]


class OutcomeMutation(Mutation):
    status: Literal["monitoring", "closed_unconfirmed", "closed_demo"]


class TaskDefinition(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    title: str = Field(min_length=1)
    kind: Literal["verification", "response"]
    required_for_review: bool
    evidence_required: bool
    proposed_owner_role: str
    due_label: str
    source_ids: list[str]
    institution_assignment: Literal["NOT_ASSIGNED"]


class DemoObservation(BaseModel):
    model_config = ConfigDict(extra="allow")
    parameter: Literal["total_suspended_solids"]
    unit: Literal["mg/L"]
    baseline: float = Field(strict=True, gt=0, allow_inf_nan=False)
    value: float = Field(strict=True, ge=0, allow_inf_nan=False)
    threshold: float = Field(strict=True, ge=0, allow_inf_nan=False)
    comparator: Literal[">="]
    mode: Literal["SIMULATED_LAB_DEMONSTRATION"]
    lab_confirmation: Literal["NONE"]
    confidence: Literal["UNVERIFIED"]
    threshold_classification: Literal["DEMO_CONFIG"]


def validate_sources(scenario, tasks):
    sources = scenario["sources"]
    if not scenario["authorities"] or not scenario["legal_checks"]:
        raise ValueError("Institutional candidates and legal checks are required")
    ids = [source["id"] for source in sources]
    if not sources or len(set(ids)) != len(ids) or any(not isinstance(i, str) or not i for i in ids):
        raise ValueError("Missing or duplicate source identity")
    for source in sources:
        if source.get("verification") not in {"SOURCE_LOCATED_UNREVIEWED", "LOCAL_CONTENT_INSPECTED"} or source.get("reviewer") is not None:
            raise ValueError("No professionally verified sources are configured for this exercise")
        if source.get("verified") or source.get("legal_authorization"):
            raise ValueError("Unsupported source verification claim")
        url = source.get("url")
        if url is not None:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.port not in {None, 443}:
                raise ValueError("Source URL must be an HTTPS reference without credentials")
        elif not isinstance(source.get("path"), str) or not source["path"]:
            raise ValueError("Source needs a URL or local provenance path")
    for item in [*tasks, *scenario["authorities"], *scenario["legal_checks"]]:
        references = item["source_ids"]
        if not references or any(reference not in ids for reference in references):
            raise ValueError("Missing source reference")
    for authority in scenario["authorities"]:
        if authority["verification"] != "SOURCE_LOCATED_UNREVIEWED" or authority["institution_assignment"] != "NOT_ASSIGNED" or authority["jurisdiction_status"] != "PENDING_EXPERT_CONFIRMATION":
            raise ValueError("Authority competence remains unverified in this exercise")
    for check in scenario["legal_checks"]:
        if check["verification"] != "SOURCE_LOCATED_UNREVIEWED" or check["expert_review"] != "PENDING" or check["statutory_claim"] is not False or check["deadline_value"] is not None or check["deadline_type"] != "NONE_VERIFIED":
            raise ValueError("Unsupported legal verification or deadline")


def now():
    return datetime.now(timezone.utc).isoformat()


def load_scenario():
    """Only one explicit packaged file is readable, never a user-supplied path."""
    try:
        content = (CONFIG / "incidents" / f"{SCENARIO_ID}.json").read_bytes()
        scenario = json.loads(content)
        if scenario["id"] != SCENARIO_ID or scenario["mode"] != "SIMULATED_DEMONSTRATION":
            raise ValueError("Invalid demonstration identity")
        tasks = [TaskDefinition.model_validate(task).model_dump() for task in scenario["tasks"]]
        if not tasks or len({t["id"] for t in tasks}) != len(tasks):
            raise ValueError("Missing or duplicate task IDs")
        if not any(t["required_for_review"] and t["kind"] == "verification" for t in tasks):
            raise ValueError("Verification gates required")
        if any(t["required_for_review"] and t["kind"] != "verification" for t in tasks):
            raise ValueError("Review gate cannot depend on response")
        observation = DemoObservation.model_validate(scenario["observation"]).model_dump()
        ratio = observation["value"] / observation["baseline"]
        # Even finite inputs can overflow during division.
        if not math.isfinite(ratio):
            raise ValueError("Observation ratio is not finite")
        observation["ratio"] = ratio
        observation["anomaly_status"] = "DEMO_TRIGGER_EXCEEDED" if observation["value"] >= observation["threshold"] else "NO_DEMO_TRIGGER"
        observation["statutory_limit"] = False
        observation["pollution_confirmed"] = False
        scenario["observation"] = observation
        validate_sources(scenario, tasks)
        scenario["tasks"] = tasks
        scenario["content_sha256"] = hashlib.sha256(content).hexdigest()
        return scenario
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(422, "Demonstration configuration unavailable or malformed; no replacement evidence invented") from exc


def store_for(request):
    env = request.scope.get("env")
    if env is not None:
        store = getattr(request.state, "incident_store", None)
        if store is None:
            # Identity is established by the private-backend middleware, not here.
            raise HTTPException(403, "Authenticated private gateway required")
        return store
    return SQLiteIncidentStore()


async def get_incident(store, incident_id):
    incident = await store.get(incident_id)
    if incident is None:
        raise HTTPException(404, "Incident not found")
    return incident


def check_revision(incident, mutation):
    if mutation.expected_revision is not None and mutation.expected_revision != incident["revision"]:
        raise HTTPException(409, "Incident changed; reload before updating")


def timeline(incident, kind, note, **details):
    incident["timeline"].append({"id": uuid4().hex, "at": now(), "kind": kind,
                                 "revision": incident["revision"] if kind == "incident_created" else incident["revision"] + 1,
                                 "note": note, "actor": "LOCAL_DEMO_USER" if incident["identity_mode"] == "LOCAL_DEMO" else "AUTHENTICATED_WORKSPACE_OWNER",
                                 "demonstration_only": True, **details})


async def save(store, incident):
    previous = incident["revision"]
    incident["revision"] += 1
    incident["updated_at"] = now()
    try:
        return await store.save(incident, previous)
    except RevisionConflict as exc:
        raise HTTPException(409, str(exc)) from exc


def ensure_open(incident):
    if incident["status"].startswith("closed_"):
        raise HTTPException(409, "Reopen the demonstration to monitoring before editing")


@router.get("/scenario")
async def scenario():
    return load_scenario()


@router.post("")
async def create(request: Request, body: CreateIncident = CreateIncident()):
    scenario = load_scenario()
    timestamp = now()
    incident = {"id": "WQ-DEMO-" + uuid4().hex[:12], "scenario": scenario,
                "revision": 1, "created_at": timestamp, "updated_at": timestamp,
                "identity_mode": "PRIVATE_GATEWAY" if request.scope.get("env") is not None else "LOCAL_DEMO",
                "status": "verification_required", "finding_status": "UNCONFIRMED_ANOMALY" if scenario["observation"]["anomaly_status"] == "DEMO_TRIGGER_EXCEEDED" else "NO_DEMO_TRIGGER",
                "review_status": "pending", "official_authorization": False,
                "dispatch_available": False, "institution_assignment": "NOT_ASSIGNED",
                "notice": DEMO_NOTICE, "reviews": [], "timeline": [], "outcome": None,
                "tasks": [{**task, "status": "system_suggested", "assignee_name": None,
                           "assignee_role": None, "note": None, "evidence_status": "NOT_RECORDED",
                           "internal_target_at": None,
                           "internal_target_classification": "USER_SET_DEMO_TARGET_NOT_STATUTORY"}
                          for task in scenario["tasks"]]}
    timeline(incident, "incident_created", "Opened hypothetical anomaly for verification; no pollution confirmed.")
    return await store_for(request).create(incident)


@router.get("")
async def list_incidents(request: Request):
    return await store_for(request).list()


@router.get("/{incident_id}")
async def read(incident_id: str, request: Request):
    return await get_incident(store_for(request), incident_id)


@router.patch("/{incident_id}/tasks/{task_id}")
async def update_task(incident_id: str, task_id: str, body: TaskMutation, request: Request):
    store = store_for(request)
    incident = await get_incident(store, incident_id)
    check_revision(incident, body)
    ensure_open(incident)
    task = next((t for t in incident["tasks"] if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(404, "Task not found")
    if task["status"] == "rejected" and body.status not in {"rejected", "system_suggested"}:
        raise HTTPException(409, "Reset the rejected task to system_suggested with a reason before progressing")
    if task["kind"] == "response" and body.status in {"specialist_approved", "in_progress", "completed"} and incident["review_status"] != "demo_approved":
        raise HTTPException(409, "Response tasks require a current demo technical review")
    assignee_name = body.assignee_name or task["assignee_name"]
    assignee_role = body.assignee_role or task["assignee_role"]
    if body.status in {"specialist_approved", "in_progress", "completed"} and not (assignee_name and assignee_role):
        raise HTTPException(422, "Record a demo task owner name and role")
    previous_status = task["status"]
    previous_target = task.get("internal_target_at")
    internal_target = previous_target
    if "internal_target_at" in body.model_fields_set:
        internal_target = body.internal_target_at.isoformat() if body.internal_target_at is not None else None
    task.update(status=body.status, assignee_name=assignee_name, assignee_role=assignee_role,
                note=body.note, updated_at=now(), institution_assignment="NOT_ASSIGNED",
                internal_target_at=internal_target,
                internal_target_classification="USER_SET_DEMO_TARGET_NOT_STATUTORY",
                evidence_status="SELF_RECORDED_DEMO_CHECK" if body.status == "completed" else "NOT_RECORDED")
    reset_rejected = previous_status == "rejected" and body.status == "system_suggested"
    if (task["kind"] == "verification" or reset_rejected) and incident["review_status"] == "demo_approved":
        incident["review_status"] = "pending"
        incident["status"] = "verification_required"
        timeline(incident, "review_invalidated", "Verification changed or rejected task reconsidered; repeat the demonstration review.")
    timeline(incident, "task_updated", body.note, task_id=task_id, previous_status=previous_status,
             status=body.status, assignee_name=assignee_name, assignee_role=assignee_role,
             previous_internal_target_at=previous_target, internal_target_at=internal_target,
             internal_target_classification="USER_SET_DEMO_TARGET_NOT_STATUTORY")
    return await save(store, incident)


@router.post("/{incident_id}/review")
async def review(incident_id: str, body: ReviewMutation, request: Request):
    store = store_for(request)
    incident = await get_incident(store, incident_id)
    check_revision(incident, body)
    ensure_open(incident)
    outstanding = [t["id"] for t in incident["tasks"] if t["required_for_review"] and t["status"] != "completed"]
    if body.decision == "demo_approved" and outstanding:
        raise HTTPException(409, {"message": "Complete the required demo verification checks first", "outstanding_task_ids": outstanding})
    record = {**body.model_dump(exclude={"expected_revision"}), "id": uuid4().hex,
              "at": now(), "scope": "SELF_RECORDED_DEMO_TECHNICAL_REVIEW", "legal_authorization": False,
              "source_versions": {"scenario_sha256": incident["scenario"]["content_sha256"]}}
    incident["reviews"].append(record)
    incident["review_status"] = body.decision
    incident["status"] = "demo_plan_approved" if body.decision == "demo_approved" else "verification_required"
    timeline(incident, "review_recorded", body.note, decision=body.decision, reviewer_name=body.reviewer_name,
             reviewer_role=body.reviewer_role, legal_authorization=False)
    return await save(store, incident)


@router.post("/{incident_id}/outcome")
async def outcome(incident_id: str, body: OutcomeMutation, request: Request):
    store = store_for(request)
    incident = await get_incident(store, incident_id)
    check_revision(incident, body)
    if body.status == "closed_demo":
        if incident["review_status"] != "demo_approved" or any(t["status"] not in {"completed", "rejected"} for t in incident["tasks"]):
            raise HTTPException(409, "Demo closure requires a current review and all tasks completed or rejected with justification")
    incident["outcome"] = {"status": body.status, "note": body.note, "at": now(),
                           "pollution_confirmed": False, "legal_violation_established": False,
                           "demonstration_only": True}
    incident["status"] = body.status
    timeline(incident, "outcome_recorded", body.note, status=body.status)
    return await save(store, incident)


@router.get("/{incident_id}/export")
async def export(incident_id: str, request: Request):
    incident = await get_incident(store_for(request), incident_id)
    scenario = incident["scenario"]
    lines = [f"# {incident['id']} — demonstration incident record", "", DEMO_NOTICE, "",
             f"Scenario: {incident['scenario']['title']}", f"Status: {incident['status']}",
             f"Technical review: {incident['review_status']}", f"Finding: {incident['finding_status']}",
             f"Scenario SHA-256: {scenario['content_sha256']}", f"Incident revision: {incident['revision']}"]
    # Preserve complete evidence fields rather than silently dropping provenance,
    # uncertainty or future additions from the human-readable principal export.
    def evidence_section(title, value):
        lines.extend(["", f"## {title}", "", "```json", json.dumps(value, ensure_ascii=False, indent=2), "```"])

    evidence_section("Observation — constructed sample; demo trigger is not a statutory limit", scenario["observation"])
    evidence_section("Location — illustrative geometry and unconfirmed jurisdiction", scenario["waterbody"])
    evidence_section("Evidence provenance — historical context is not joined to this incident", scenario.get("evidence", {}))
    evidence_section("Uncertainty and limitations — no pollution or violation established", scenario.get("limitations", []))
    evidence_section("Potential receptors — illustrative; exposure unverified; no propagation forecast", scenario.get("receptors", []))
    evidence_section("Candidate institutions — competence unconfirmed; no official assignment", scenario.get("authorities", []))
    evidence_section("Legal and procedural checks — pending qualified review; no verified statutory duties", scenario.get("legal_checks", []))
    lines.extend(["", "## Tasks — internal user-set targets are not statutory deadlines"])
    lines.extend(f"- {t['title']}: {t['status']}; demo owner: {t['assignee_name'] or 'unassigned'} ({t['assignee_role'] or t['proposed_owner_role']}); institution NOT_ASSIGNED. Internal target: {t.get('internal_target_at') or 'not set'} (USER_SET_DEMO_TARGET_NOT_STATUTORY). Source deadline status: {t['due_label']}. Note: {t['note'] or 'none'}" for t in incident["tasks"])
    evidence_section("Review history — self-declared demonstration reviewers; no official authorization", incident["reviews"])
    evidence_section("Recorded outcome — demonstration only; pollution remains unconfirmed", incident["outcome"])
    lines.extend(["", "## Timeline"])
    lines.extend(f"- {event['at']} · revision {event.get('revision', 'not recorded')} · {event['kind']}: {event['note']}" for event in incident["timeline"])
    evidence_section("Full timeline evidence", incident["timeline"])
    evidence_section("Source references and provenance — links do not certify applicability", scenario.get("sources", []))
    return {"incident": incident, "markdown": "\n".join(lines), "official_authorization": False,
            "dispatch_available": False}
