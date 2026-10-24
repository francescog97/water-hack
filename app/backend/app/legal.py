"""Fail-closed institutional knowledge evaluator; no severity-to-power mapping."""
import hashlib
import json
from datetime import date
from urllib.parse import urlparse

from .models import Band, Facts
from .paths import CONFIG

REVIEW_STATES = {"VERIFIED_BY_DOMAIN_EXPERT", "SOURCE_LOCATED_UNREVIEWED", "DEMO_ONLY", "UNKNOWN"}
MATRIX_STATES = ["VERIFIED", "SOURCE_FOUND_REVIEW_PENDING", "UNMAPPED", "NOT_APPLICABLE", "DEMO_ONLY"]
FACT_KEYS = set(Facts.model_fields)


def load_legalpacks() -> dict:
    result = {}
    for path in sorted((CONFIG / "legalpacks").glob("*.json")):
        raw = path.read_bytes()
        pack = json.loads(raw)
        validate_package(pack)
        pack["content_sha256"] = hashlib.sha256(raw).hexdigest()
        if pack["id"] in result:
            raise ValueError("Duplicate legal package ID")
        result[pack["id"]] = pack
    return result


def validate_package(pack: dict):
    source_ids = {s["source_id"] for s in pack["sources"]}
    if len(source_ids) != len(pack["sources"]):
        raise ValueError("Duplicate source ID")
    authority_ids = {a["authority_id"] for a in pack["authorities"]}
    procedure_ids = {p["procedure_id"] for p in pack["procedures"]}
    if len(authority_ids) != len(pack["authorities"]) or len(procedure_ids) != len(pack["procedures"]):
        raise ValueError("Duplicate authority or procedure ID")
    for source in pack["sources"]:
        url = urlparse(source["official_url"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError("Source links must be public HTTPS URLs without credentials")
        if source["review_status"] not in REVIEW_STATES:
            raise ValueError("Unknown source review status")
        if source["review_status"] == "VERIFIED_BY_DOMAIN_EXPERT" and not source.get("reviewer"):
            raise ValueError("Expert verification requires a named reviewer")
    for authority in pack["authorities"]:
        if not set(authority["legal_source_ids"]) <= source_ids:
            raise ValueError("Authority references missing sources")
        if not set(authority["conditions"]) <= FACT_KEYS:
            raise ValueError("Unknown authority fact")
    for procedure in pack["procedures"]:
        if not set(procedure["source_ids"]) <= source_ids or not set(procedure["applicable_authority_ids"]) <= authority_ids:
            raise ValueError("Procedure references missing sources or authority")
        if not set(procedure["dependencies"]) <= procedure_ids or not set(procedure["trigger_conditions"]) <= FACT_KEYS:
            raise ValueError("Procedure has an unknown dependency or condition")
        if procedure["verification_status"] not in REVIEW_STATES:
            raise ValueError("Unknown procedure review status")
        if procedure["deadline_type"] not in {"STATUTORY", "PLAN", "INTERNAL_TARGET", "NONE_VERIFIED"}:
            raise ValueError("Unknown deadline type")
    for rule in pack["legal_rules"]:
        if not set(rule.get("source_ids", [])) <= source_ids or not set(rule.get("conditions", [])) <= FACT_KEYS:
            raise ValueError("Legal rules may only use explicit sourced legal facts, never scenario severity")


def condition_results(keys: list[str], facts: Facts):
    data = facts.model_dump()
    return [{"fact": key, "value": data[key],
             "status": "UNKNOWN" if data[key] is None else "MET" if data[key] else "UNMET",
             "evidence": "Operator-supplied scenario fact; not independently verified"} for key in keys]


def evaluate_legal_rules(pack: dict, facts: Facts, event_date: date | None) -> list[dict]:
    """Review applicability only when provision, version and conditions are evidenced.

    No bundled rule meets this gate. This interface permits a future expert-reviewed
    package without introducing a severity-based legal trigger or an action sink.
    """
    sources = {s["source_id"]: s for s in pack["sources"]}
    results = []
    for index, rule in enumerate(pack["legal_rules"]):
        conditions = condition_results(rule.get("conditions", []), facts)
        cited = [sources[s] for s in rule.get("source_ids", []) if s in sources]
        reviewed = rule.get("review_status") == "VERIFIED_BY_DOMAIN_EXPERT" and bool(rule.get("reviewer"))
        supported = reviewed and bool(cited) and event_date is not None
        for source in cited:
            try:
                valid_from = date.fromisoformat(source.get("effective_date_from") or "")
                valid_to = date.fromisoformat(source["effective_date_to"]) if source.get("effective_date_to") else date.max
            except ValueError:
                supported = False
                continue
            supported = supported and source["review_status"] == "VERIFIED_BY_DOMAIN_EXPERT" and bool(source.get("reviewer")) and bool(source.get("article_or_section")) and valid_from <= event_date <= valid_to
        state = "NEEDS_VERIFICATION"
        if supported and conditions and all(c["status"] == "MET" for c in conditions):
            state = "REVIEWED_APPLICABILITY_CANDIDATE"
        elif any(c["status"] == "UNMET" for c in conditions):
            state = "CONDITION_NOT_MET"
        results.append({"rule_id": rule.get("rule_id", f"rule-{index}"), "evaluation": state,
                        "conditions": conditions, "source_ids": rule.get("source_ids", []),
                        "authorized": False, "official_decision": False})
    return results


def evaluate_legal(pack: dict, facts: Facts, band: str, event_date: date | None = None) -> dict:
    source_lookup = {s["source_id"]: s for s in pack["sources"]}
    cards = []
    for procedure in pack["procedures"]:
        conditions = condition_results(procedure["trigger_conditions"], facts)
        sources = [source_lookup[s] for s in procedure["source_ids"]]
        verified = bool(sources) and event_date is not None and procedure["verification_status"] == "VERIFIED_BY_DOMAIN_EXPERT" and bool(procedure.get("reviewer"))
        for source in sources:
            try:
                valid_from = date.fromisoformat(source.get("effective_date_from") or "")
                valid_to = date.fromisoformat(source["effective_date_to"]) if source.get("effective_date_to") else date.max
            except ValueError:
                verified = False
                continue
            verified = verified and source["review_status"] == "VERIFIED_BY_DOMAIN_EXPERT" and bool(source.get("reviewer")) and bool(source.get("article_or_section")) and valid_from <= event_date <= valid_to
        met = bool(conditions) and all(c["status"] == "MET" for c in conditions)
        state = "NEEDS_VERIFICATION"
        if any(c["status"] == "UNMET" for c in conditions):
            state = "CONDITION_NOT_MET"
        elif verified and met:
            state = "REVIEWED_CONDITIONS_REPORTED_MET"
        # Even a reviewed mapping does not authorize action; formal decisions stay outside this app.
        deadline = None
        deadline_type = procedure["deadline_type"]
        if deadline_type == "INTERNAL_TARGET" and procedure["deadline_value"] is not None:
            deadline = f"Internal target only: {procedure['deadline_value']} {procedure['deadline_unit']}"
        elif deadline_type in ("STATUTORY", "PLAN") and verified and met and procedure["deadline_value"] is not None and procedure["deadline_unit"]:
            deadline = f"{deadline_type}: {procedure['deadline_value']} {procedure['deadline_unit']} (review source scope)"
        else:
            deadline_type = "NONE_VERIFIED"
        cards.append({**procedure, "deadline_value": procedure["deadline_value"] if deadline else None,
                      "deadline_unit": procedure["deadline_unit"] if deadline else None,
                      "deadline_type": deadline_type, "deadline_display": deadline or "No verified deadline in this package",
                      "conditions": conditions, "sources": sources, "evaluation": state,
                      "prioritized_for_review": band in procedure.get("review_priority", []),
                      "authorized": False, "legally_required": False})
    cards.sort(key=lambda c: (not c["prioritized_for_review"], c["procedure_id"]))
    return {"package_id": pack["id"], "package_version": pack["version"],
            "authorities": pack["authorities"], "cards": cards,
            "legal_designation": "NOT DETERMINED", "authorized_actions": [],
            "formal_disaster_declared": facts.formal_disaster_declared,
            "legal_rule_evaluations": evaluate_legal_rules(pack, facts, event_date),
            "expert_review": "No domain-expert event mapping is verified in the bundled packages",
            "review_tasks": ["Verify the selected observation and its date-only precision", *pack["deliberate_gaps"]] +
            (["Restore trustworthy input before making a scenario classification"] if band == Band.UNKNOWN else []),
            "notice": "Scenario severity changes review emphasis only. It cannot activate statutory powers, obligations or deadlines."}


def coverage(pack: dict) -> dict:
    def status(items):
        if not items:
            return "UNMAPPED"
        states = [i.get("verification_status", i.get("review_status", i.get("confidence_label", "UNKNOWN"))) for i in items]
        if all(s == "VERIFIED_BY_DOMAIN_EXPERT" for s in states):
            return "VERIFIED"
        if all(s == "DEMO_ONLY" for s in states):
            return "DEMO_ONLY"
        return "SOURCE_FOUND_REVIEW_PENDING"
    rows = []
    for band in (Band.NORMAL, Band.WARNING, Band.DANGER, Band.EMERGENCY):
        cells = []
        groups = {"Authority": pack["authorities"],
                  "Possible measures": [p for p in pack["procedures"] if p["action_type"] == "POSSIBLE_MEASURE"],
                  "Deadlines": [p for p in pack["procedures"] if p["deadline_type"] in ("STATUTORY", "PLAN")],
                  "Procedures": pack["procedures"], "Legal sources": pack["sources"]}
        for field, items in groups.items():
            refs = sorted({sid for item in items for sid in item.get("source_ids", item.get("legal_source_ids", [item["source_id"]] if "source_id" in item else []))})
            cell_status = status(items)
            cells.append({"field": field, "status": cell_status, "source_ids": refs,
                          "explanation": "No verified mapping in the loaded knowledge package. This does not imply a gap in Bulgarian law." if cell_status == "UNMAPPED" else "Source references are available; current wording, scope and event-specific interpretation require expert review." if cell_status == "SOURCE_FOUND_REVIEW_PENDING" else "Review state of the loaded package only; no operational authorization."})
        rows.append({"band": band, "cells": cells})
    return {"package_id": pack["id"], "rows": rows, "legend": MATRIX_STATES,
            "scope": "Coverage of this knowledge package, not an assessment of the completeness of legislation. Rows do not represent legal triggers."}
