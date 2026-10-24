import json
from .models import Band, Observation, RulePack
from .paths import CONFIG


def load_rulepacks() -> dict[str, RulePack]:
    result = {}
    for path in sorted((CONFIG / "rulepacks").glob("*.json")):
        pack = RulePack.model_validate(json.loads(path.read_text(encoding="utf-8")))
        if pack.id in result:
            raise ValueError("Duplicate rule pack ID")
        result[pack.id] = pack
    return result


def classify(observation: Observation | None, pack: RulePack, *, stale=False, offline=False) -> dict:
    reasons = []
    if observation is None or observation.value is None:
        reasons.append("No trustworthy observation exists for the selected date")
    if stale:
        reasons.append("Stale-input failure injection: classification withheld")
    if offline:
        reasons.append("Missing-input failure injection: source unavailable in this scenario")
    if observation is not None:
        if observation.station_id not in pack.station_ids:
            reasons.append("Station identity does not match this rule pack")
        if observation.parameter != pack.parameter or observation.unit != pack.unit:
            reasons.append("Parameter/unit mismatch; discharge cannot be interpreted as water level")
        if any(f in observation.quality_flags for f in ("missing", "duplicate", "outlier_suspect", "stale")):
            reasons.append("Observation quality prevents classification")
        if observation.value is not None and observation.value < 0:
            reasons.append("Negative discharge is not accepted by this demo rule")
    if reasons:
        return {"band": Band.UNKNOWN, "reasons": reasons, "triggered_threshold": None,
                "rule_pack_id": pack.id, "rule_version": pack.version, "official_designation": False}
    band = Band.NORMAL
    for candidate in (Band.WARNING, Band.DANGER, Band.EMERGENCY):
        if observation.value >= pack.thresholds[candidate]:
            band = candidate
    threshold = pack.thresholds.get(band)
    return {"band": band, "reasons": [f"{observation.value:g} {pack.unit} " +
            (f">= {threshold:g} {pack.unit} illustrative {band} threshold" if threshold is not None else "is below the illustrative WARNING threshold")],
            "triggered_threshold": threshold, "rule_pack_id": pack.id,
            "rule_version": pack.version, "official_designation": False}
