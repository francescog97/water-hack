import hashlib
import json
from datetime import timedelta

from .ingest import load_case
from .legal import coverage, evaluate_legal, load_legalpacks
from .models import Band, Observation, ScenarioRequest
from .rules import classify, load_rulepacks


def evaluate(request: ScenarioRequest) -> dict:
    case = load_case(request.case_id)
    packs = load_rulepacks()
    legalpacks = load_legalpacks()
    if request.rule_pack_id not in packs or request.legal_pack_id not in legalpacks:
        raise KeyError("Unknown rule or legal package ID")
    pack, legalpack = packs[request.rule_pack_id], legalpacks[request.legal_pack_id]
    matches = [o for o in case["observations"] if o["date"] == request.selected_date.isoformat()]
    observed = Observation.model_validate(matches[0]) if len(matches) == 1 else None
    historical = classify(observed, pack, stale=request.stale, offline=request.sensor_offline)
    synthetic = []
    if request.simulate and historical["band"] != Band.UNKNOWN:
        for step in range(1, request.steps + 1):
            day = request.selected_date + timedelta(days=step)
            value = observed.value + request.daily_increase * step
            point = observed.model_copy(update={
                "observation_id": f"scenario:{request.case_id}:{day}",
                "date": day, "observed_at": f"{day}T00:00:00Z", "value": value,
                "source_row": None, "raw_value": None, "mode": "simulated",
            })
            synthetic.append({"date": day.isoformat(), "value": value, "step": step,
                              "mode": "simulated", "quality_flags": ["synthetic"],
                              "band": classify(point, pack)["band"], "unit": pack.unit})
    effective = historical
    if synthetic:
        last = observed.model_copy(update={"value": synthetic[-1]["value"], "mode": "simulated"})
        effective = classify(last, pack)
    crossings = []
    for band, threshold in pack.thresholds.items():
        point = next((p for p in synthetic if p["value"] >= threshold and observed.value < threshold), None)
        if point:
            crossings.append({"band": band, "date": point["date"], "step": point["step"],
                              "label": f"Day +{point['step']} · illustrative {band} crossing"})
    digest = {"request": request.model_dump(mode="json"), "data_sha256": case["source"]["sha256"],
              "rule_pack": pack.model_dump(), "legal_sha256": legalpack["content_sha256"]}
    context_id = hashlib.sha256(json.dumps(digest, sort_keys=True).encode()).hexdigest()
    history = [p for p in case["timeline"] if p["date"] <= request.selected_date.isoformat()]
    warnings = [
        "DEMONSTRATION · NOT FOR OPERATIONAL USE",
        "Historical local discharge, not a live observation; original method and aggregation unverified.",
        "Illustrative demo thresholds are not official Bulgarian thresholds or legal triggers.",
        "No calibrated forecast, validated probability, inundation map or safe route is available.",
        "No expert-verified event-specific legal interpretation; all institutional decisions remain external.",
    ]
    if request.stale:
        warnings.append("Stale-input failure injection enabled; classification withheld.")
    if request.sensor_offline:
        warnings.append("Missing-input failure injection enabled; classification withheld. This is not a real sensor status.")
    return {
        "context_id": context_id, "request": request.model_dump(mode="json"),
        "case": {"station": case["station"], "source": case["source"], "summary": case["summary"]},
        "observation": observed.model_dump(mode="json") if observed else None,
        "historical_classification": historical, "classification": effective,
        "effective_mode": "simulated" if synthetic else "historical",
        "effective_value": synthetic[-1]["value"] if synthetic else observed.value if observed and effective["band"] != Band.UNKNOWN else None,
        "historical_timeline": history, "simulation": synthetic,
        "simulation_assumptions": {"method": "Anchor discharge + configured linear daily increase",
            "daily_increase": request.daily_increase, "unit": "m3/s per day",
            "steps": request.steps, "precision": "Whole-day scenario steps; not a forecast",
            "crossings": crossings, "forecast_available": False},
        "rule_pack": pack.model_dump(), "legal_pack": legalpack,
        "response": evaluate_legal(legalpack, request.facts, effective["band"], request.selected_date),
        "coverage": coverage(legalpack), "warnings": warnings,
        "data_state": "UNKNOWN" if effective["band"] == Band.UNKNOWN else "Historical replay; current freshness not applicable",
    }
