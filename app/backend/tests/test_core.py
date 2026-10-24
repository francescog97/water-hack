import copy
import csv
import hashlib
import json
from datetime import date

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.backend.app.briefing import make_briefing
from app.backend.app.ingest import load_case, parse_date, parse_number, read_discharge
from app.backend.app.legal import coverage, evaluate_legal, evaluate_legal_rules, load_legalpacks, validate_package
from app.backend.app.main import app
from app.backend.app.models import Facts, Observation, RulePack, ScenarioRequest
from app.backend.app.paths import ROOT
from app.backend.app.review import acknowledge
from app.backend.app.rules import classify, load_rulepacks
from app.backend.app.scenario import evaluate

client = TestClient(app)


def obs(value=9.922, **kwargs):
    return Observation(observation_id="test", source_id="iskar-novi", station_id="iskar-novi",
                       waterbody="Iskar", observed_at="2025-09-25T00:00:00Z", date=date(2025, 9, 25),
                       value=value, provenance_file="fixture", **kwargs)


@pytest.mark.parametrize("value,expected", [(0,"NORMAL"),(7.999,"NORMAL"),(8,"WARNING"),(19.999,"WARNING"),(20,"DANGER"),(49.999,"DANGER"),(50,"EMERGENCY")])
def test_exact_thresholds(value, expected):
    assert classify(obs(value), load_rulepacks()["iskar-demo"])["band"] == expected


@pytest.mark.parametrize("values", [{"WARNING":20,"DANGER":8,"EMERGENCY":50},{"WARNING":8,"DANGER":8,"EMERGENCY":50},{"WARNING":-1,"DANGER":8,"EMERGENCY":50},{"WARNING":8,"DANGER":20}])
def test_invalid_threshold_order(values):
    raw = load_rulepacks()["iskar-demo"].model_dump()
    raw["thresholds"] = values
    with pytest.raises(ValidationError):
        RulePack.model_validate(raw)


@pytest.mark.parametrize("observation", [None,obs(None),obs(-1),obs(20,unit="m"),obs(20,quality_flags=["duplicate"]),obs(20,quality_flags=["outlier_suspect"])])
def test_untrusted_is_unknown(observation):
    assert classify(observation, load_rulepacks()["iskar-demo"])["band"] == "UNKNOWN"


def test_station_identity_is_required():
    altered = obs().model_copy(update={"station_id":"unknown-gauge"})
    assert classify(altered, load_rulepacks()["iskar-demo"])["band"] == "UNKNOWN"


@pytest.mark.parametrize("case_id", ["iskar-novi","iskar-orehovitsa"])
def test_real_ingestion(case_id):
    result = load_case(case_id)
    assert result["summary"]["rows"] == 146
    assert len(result["summary"]["missing_days"]) == 27
    assert len(result["timeline"]) == 173
    assert result["summary"]["duplicates"] == 0
    assert all(o["station_id"] == case_id and o["mode"] == "historical" and o["unit"] == "m3/s" for o in result["observations"])
    assert result["station"]["latitude"] is None and result["station"]["municipality"] is None
    assert all(o["date"].startswith("2025-") and "raster" not in o["source_id"] for o in result["observations"])


def test_original_hashes_unchanged():
    with (ROOT / "Dataset/registro_rinomine.csv").open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 172
    for row in rows:
        assert hashlib.sha256((ROOT / row["percorso_italiano"]).read_bytes()).hexdigest() == row["sha256"]


def test_missing_day_not_interpolated():
    result = evaluate(ScenarioRequest(selected_date=date(2025,10,10),simulate=True))
    assert result["observation"] is None
    assert result["classification"]["band"] == "UNKNOWN"
    assert not result["simulation"]


@pytest.mark.parametrize("failure", ["stale","sensor_offline"])
def test_failure_injection_closes_simulation(failure):
    result = evaluate(ScenarioRequest(simulate=True, **{failure:True}))
    assert result["classification"]["band"] == "UNKNOWN"
    assert result["effective_value"] is None
    assert result["simulation"] == []


def test_demo_transition_and_whole_day_crossing():
    result = evaluate(ScenarioRequest(simulate=True))
    assert result["observation"]["value"] == 9.922
    assert result["historical_classification"]["band"] == "WARNING"
    assert result["classification"]["band"] == "DANGER"
    assert result["simulation"][1]["value"] == pytest.approx(25.922)
    assert all(p["mode"] == "simulated" for p in result["simulation"])
    assert result["simulation_assumptions"]["crossings"][0]["step"] == 2
    assert result["simulation_assumptions"]["forecast_available"] is False
    assert all(p["date"] <= "2025-09-25" for p in result["historical_timeline"])


def test_config_swaps_are_observable():
    first = evaluate(ScenarioRequest(simulate=True))
    alternate = evaluate(ScenarioRequest(simulate=True,rule_pack_id="alternate-demo"))
    minimal = evaluate(ScenarioRequest(simulate=True,legal_pack_id="bulgaria-source-only"))
    assert first["classification"]["band"] == "DANGER"
    assert alternate["classification"]["band"] == "WARNING"
    assert first["context_id"] != alternate["context_id"]
    assert len(first["response"]["cards"]) == 4 and minimal["response"]["cards"] == []
    assert first["coverage"]["rows"][1]["cells"][3]["status"] != minimal["coverage"]["rows"][1]["cells"][3]["status"]


def test_actual_json_content_edit_changes_evaluation(tmp_path, monkeypatch):
    from app.backend.app import rules, legal
    config=tmp_path/"config"
    (config/"rulepacks").mkdir(parents=True)
    (config/"legalpacks").mkdir()
    for folder in ["rulepacks","legalpacks"]:
        for source in (ROOT/"app/config"/folder).glob("*.json"):
            (config/folder/source.name).write_bytes(source.read_bytes())
    monkeypatch.setattr(rules,"CONFIG",config)
    monkeypatch.setattr(legal,"CONFIG",config)
    first=evaluate(ScenarioRequest(simulate=True))
    path=config/"rulepacks/iskar-demo.json"
    raw=json.loads(path.read_text(encoding="utf-8"))
    raw["thresholds"]["DANGER"]=30
    raw["version"]="1.0.1-test"
    path.write_text(json.dumps(raw),encoding="utf-8")
    second=evaluate(ScenarioRequest(simulate=True))
    assert first["classification"]["band"]=="DANGER" and second["classification"]["band"]=="WARNING"
    assert first["context_id"]!=second["context_id"]
    # No production config or original dataset is edited by this test.


def test_severity_never_generates_powers_or_deadlines():
    pack = load_legalpacks()["bulgaria-flood"]
    for band in ["NORMAL","WARNING","DANGER","EMERGENCY","UNKNOWN"]:
        result = evaluate_legal(pack,Facts(jurisdiction_confirmed=True,municipal_plan_available=True,formal_disaster_declared=True,basin_authority_confirmed=True),band)
        assert result["authorized_actions"] == [] and result["legal_designation"] == "NOT DETERMINED"
        assert all(not c["authorized"] and not c["legally_required"] and c["deadline_type"] == "NONE_VERIFIED" for c in result["cards"])
        assert all(c["evaluation"] == "NEEDS_VERIFICATION" for c in result["cards"])


def test_unknown_unmet_conditions_distinct():
    pack = load_legalpacks()["bulgaria-flood"]
    unknown = evaluate_legal(pack,Facts(),"DANGER")
    unmet = evaluate_legal(pack,Facts(jurisdiction_confirmed=False),"DANGER")
    assert all(c["status"] == "UNKNOWN" for c in unknown["cards"][0]["conditions"])
    assert any(c["evaluation"] == "CONDITION_NOT_MET" for c in unmet["cards"])


def test_statutory_deadline_without_review_is_withheld():
    pack = copy.deepcopy(load_legalpacks()["bulgaria-flood"])
    pack["procedures"][0].update(deadline_type="STATUTORY",deadline_value=2,deadline_unit="hours")
    result = evaluate_legal(pack,Facts(jurisdiction_confirmed=True),"EMERGENCY")
    card = next(c for c in result["cards"] if c["procedure_id"] == "verify-jurisdiction")
    assert card["deadline_value"] is None and card["deadline_type"] == "NONE_VERIFIED"


def test_expert_label_without_effective_version_cannot_supply_deadline():
    pack=copy.deepcopy(load_legalpacks()["bulgaria-flood"])
    proc=pack["procedures"][0]
    proc.update(verification_status="VERIFIED_BY_DOMAIN_EXPERT",reviewer="TEST FIXTURE",deadline_type="STATUTORY",deadline_value=2,deadline_unit="hours")
    pack["sources"][0].update(review_status="VERIFIED_BY_DOMAIN_EXPERT",reviewer="TEST FIXTURE")
    card=next(c for c in evaluate_legal(pack,Facts(jurisdiction_confirmed=True),"EMERGENCY",date(2025,9,25))["cards"] if c["procedure_id"]==proc["procedure_id"])
    assert card["deadline_type"]=="NONE_VERIFIED" and card["deadline_value"] is None


def test_unsourced_claim_not_verified():
    pack = copy.deepcopy(load_legalpacks()["bulgaria-flood"])
    pack["procedures"][0].update(source_ids=[],verification_status="VERIFIED_BY_DOMAIN_EXPERT")
    result = evaluate_legal(pack,Facts(jurisdiction_confirmed=True),"EMERGENCY")
    assert next(c for c in result["cards"] if c["procedure_id"] == "verify-jurisdiction")["evaluation"] == "NEEDS_VERIFICATION"


def test_illegal_severity_trigger_rejected():
    pack = copy.deepcopy(load_legalpacks()["bulgaria-flood"])
    pack["legal_rules"] = [{"source_ids":["ec-structure"],"conditions":["severity_is_emergency"]}]
    with pytest.raises(ValueError):
        validate_package(pack)


def test_coverage_is_package_coverage():
    matrix = coverage(load_legalpacks()["bulgaria-flood"])
    assert len(matrix["rows"]) == 4 and len(matrix["rows"][0]["cells"]) == 5
    assert set(matrix["legend"]) == {"VERIFIED","SOURCE_FOUND_REVIEW_PENDING","UNMAPPED","NOT_APPLICABLE","DEMO_ONLY"}
    assert "not an assessment" in matrix["scope"]
    for row in matrix["rows"]:
        assert row["cells"][2]["status"] == "UNMAPPED"
        assert "does not imply a gap" in row["cells"][2]["explanation"]


def test_reviewed_rule_needs_event_effective_version_and_facts():
    # Synthetic test metadata, never loaded as Bulgarian law or shown in the app.
    pack = copy.deepcopy(load_legalpacks()["bulgaria-flood"])
    pack["legal_rules"] = [{"rule_id":"fixture-only","source_ids":["ec-structure"],"conditions":["jurisdiction_confirmed"],"review_status":"VERIFIED_BY_DOMAIN_EXPERT","reviewer":"TEST FIXTURE"}]
    facts = Facts(jurisdiction_confirmed=True)
    assert evaluate_legal_rules(pack,facts,date(2025,9,25))[0]["evaluation"] == "NEEDS_VERIFICATION"
    source=pack["sources"][0]
    source.update(review_status="VERIFIED_BY_DOMAIN_EXPERT",reviewer="TEST FIXTURE",effective_date_from="2026-01-01")
    assert evaluate_legal_rules(pack,facts,date(2025,9,25))[0]["evaluation"] == "NEEDS_VERIFICATION"
    source["effective_date_from"]="2025-01-01"
    result=evaluate_legal_rules(pack,facts,date(2025,9,25))[0]
    assert result["evaluation"] == "REVIEWED_APPLICABILITY_CANDIDATE" and result["authorized"] is False
    assert evaluate_legal_rules(pack,Facts(),date(2025,9,25))[0]["evaluation"] == "NEEDS_VERIFICATION"


def test_review_and_export_bound_to_exact_context():
    result = evaluate(ScenarioRequest(simulate=True))
    with pytest.raises(ValueError):
        make_briefing(result,[])
    record = acknowledge(result["context_id"],"incident-review","Reviewed uncertainty; expert interpretation remains pending.")
    report = make_briefing(result,[record["id"]])
    assert report["official_authorization"] is False
    assert record["legal_authorization"] == 0
    assert report["mode"] == "simulated" and report["historical_observation"]["mode"] == "historical"
    assert "UNAPPROVED DRAFT" in report["markdown"] and "https://" in report["markdown"]
    changed = evaluate(ScenarioRequest(simulate=True,steps=3))
    with pytest.raises(ValueError):
        make_briefing(changed,[record["id"]])


def test_historical_brief_does_not_claim_scenario_was_applied():
    result=evaluate(ScenarioRequest())
    review=acknowledge(result["context_id"],"incident-review","Historical evidence checked; legal interpretation remains pending.")
    report=make_briefing(result,[review["id"]])
    assert report["scenario_applied"] is False and report["mode"] == "historical"
    assert "No synthetic trajectory was applied" in report["markdown"]


def test_readers_diagnostics_and_decimal_comma(tmp_path):
    p=tmp_path / "sample.csv"
    p.write_text("date;discharge(m3/s)\n25.09.2025;9,922\ndate;discharge(m3/s)\n25.09.2025;10,1\n26.09.2025;nil\n",encoding="utf-8")
    observations, diagnostics = read_discharge(p,"iskar-novi")
    assert observations[0].value == 9.922 and "duplicate" in observations[0].quality_flags
    assert observations[-1].value is None and diagnostics
    p.write_text("date,level(m)\n2025-01-01,2\n")
    with pytest.raises(ValueError):
        read_discharge(p,"iskar-novi")
    assert parse_date("25/09/2025") == date(2025,9,25)
    assert parse_number("nan") is None


@pytest.mark.parametrize("patch", [{"daily_increase":-1},{"daily_increase":"NaN"},{"daily_increase":"8"},{"steps":True},{"steps":8},{"selected_date":"not-a-date"},{"facts":{"jurisdiction_confirmed":"yes"}},{"unexpected":"x"}])
def test_api_schema(patch):
    assert client.post("/api/evaluate",json=patch).status_code == 422


def test_api_smoke_and_path_protection():
    assert client.get("/api/health").json()["live_feed"] is False
    assert len(client.get("/api/cases").json()) == 2
    assert client.post("/api/simulate",json={"simulate":True}).json()["classification"]["band"] == "DANGER"
    assert client.post("/api/evaluate",json={"case_id":"../Dataset"}).status_code == 404
    assert client.post("/api/evaluate",json={"legal_pack_id":"missing"}).status_code == 404
    for path in ["/Dataset/portata_iskar_novi_iskar_2025.csv","/EIT%20Water%20Hackathon%20Sofia%202026%20v7.pdf","/runtime/reviews.sqlite3","/.git/config"]:
        assert client.get(path).status_code == 404
    assert client.post("/api/evaluate",json={},headers={"Origin":"https://example.com"}).status_code == 403


def test_offline_evaluation_does_not_request_external_feeds(monkeypatch):
    import httpx
    monkeypatch.setattr(httpx,"get",lambda *a,**k: pytest.fail("Unexpected external request"))
    assert evaluate(ScenarioRequest())["classification"]["band"] == "WARNING"
