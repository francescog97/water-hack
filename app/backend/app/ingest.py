"""Read-only, bounded, station-specific ingestion of the supplied Iskar files."""
import csv
import hashlib
import io
import statistics
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

from .models import Observation
from .paths import ROOT, RUNTIME

STATIONS = {
    "iskar-novi": {
        "id": "iskar-novi", "name": "Novi Iskar", "raw_name": "Нови Искър",
        "file": "portata_iskar_novi_iskar_2025.csv", "waterbody": "Iskar",
        "country": "Bulgaria", "basin": None, "municipality": None,
        "latitude": None, "longitude": None,
        "identity_evidence": "Local catalogue and source filename; original gauge identifier and coordinates unavailable.",
    },
    "iskar-orehovitsa": {
        "id": "iskar-orehovitsa", "name": "Orehovitsa", "raw_name": "Ореховица",
        "file": "portata_iskar_orehovitsa_2025.csv", "waterbody": "Iskar",
        "country": "Bulgaria", "basin": None, "municipality": None,
        "latitude": None, "longitude": None,
        "identity_evidence": "Local catalogue and source filename; no propagation or travel-time relationship inferred.",
    },
}


def parse_date(value: str) -> date:
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {value[:30]!r}")


def parse_number(value: str) -> float | None:
    import math
    value = value.strip()
    if value.lower() in ("", "nil", "null", "nan", "na"):
        return None
    number = float(value.replace(",", "."))
    if not math.isfinite(number):
        raise ValueError("Non-finite observation")
    return number


def read_discharge(path: Path, station_id: str) -> tuple[list[Observation], list[str]]:
    if station_id not in STATIONS:
        raise ValueError("Unknown station ID; cross-station inference is prohibited")
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251")
    delimiter = ";" if ";" in text.splitlines()[0] else "\t" if "\t" in text.splitlines()[0] else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    if reader.fieldnames != ["date", "discharge(m3/s)"]:
        raise ValueError("Expected date and discharge(m3/s) columns; refusing an incompatible variable or unit")
    observations, diagnostics = [], []
    for line, row in enumerate(reader, 2):
        if row.get("date", "").strip() == "date":
            diagnostics.append(f"Repeated header at source row {line}; excluded explicitly")
            continue
        try:
            day = parse_date(row["date"])
            value = parse_number(row["discharge(m3/s)"])
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError(f"{path.name}, source row {line}: {exc}") from exc
        flags = ["missing"] if value is None else ["outlier_suspect"] if value < 0 else ["good"]
        observations.append(Observation(
            observation_id=f"{station_id}:row:{line}", source_id=station_id,
            station_id=station_id, waterbody="Iskar", date=day,
            observed_at=f"{day.isoformat()}T00:00:00Z", value=value,
            provenance_file=f"Dataset/{path.name}", source_row=line,
            raw_value=row["discharge(m3/s)"], quality_flags=flags,
        ))
    counts = Counter(o.date for o in observations)
    for o in observations:
        if counts[o.date] > 1:
            o.quality_flags = [x for x in o.quality_flags if x != "good"] + ["duplicate"]
    return sorted(observations, key=lambda o: (o.date, o.source_row or 0)), diagnostics


def load_case(case_id: str) -> dict:
    if case_id not in STATIONS:
        raise KeyError("Unknown case ID")
    station = STATIONS[case_id]
    path = ROOT / "Dataset" / station["file"]
    observations, diagnostics = read_discharge(path, case_id)
    if not observations:
        raise ValueError("The local source has no observations; no synthetic replacement is used")
    indexed = {}
    for o in observations:
        indexed.setdefault(o.date, []).append(o)
    start, end = observations[0].date, observations[-1].date
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    timeline = []
    for day in days:
        present = indexed.get(day, [])
        timeline.append({
            "date": day.isoformat(),
            "value": present[0].value if len(present) == 1 else None,
            "quality_flags": present[0].quality_flags if len(present) == 1 else ["duplicate"] if present else ["missing"],
            "source_row": present[0].source_row if len(present) == 1 else None,
        })
    values = [o.value for o in observations if o.value is not None and o.value >= 0]
    source = {
        "id": case_id, "title": f"Iskar discharge · {station['name']}",
        "path": f"Dataset/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "mode": "historical", "unit": "m3/s", "parameter": "discharge",
        "license": "Not documented locally; redistribution permission not established",
        "origin": "User-supplied historical CSV; original measurement method unverified",
        "time_note": "Date-only observations. UTC midnight is a serialization convention, not a measured sampling time. Aggregation method and sampling timezone unavailable.",
        "period": [start.isoformat(), end.isoformat()],
    }
    return {
        "station": station, "source": source,
        "observations": [o.model_dump(mode="json") for o in observations],
        "timeline": timeline,
        "summary": {"rows": len(observations), "calendar_days": len(days),
                    "missing_days": [x["date"] for x in timeline if "missing" in x["quality_flags"]],
                    "duplicates": sum(n - 1 for n in counts_dates(observations).values()),
                    "minimum": min(values) if values else None,
                    "maximum": max(values) if values else None,
                    "median": statistics.median(values) if values else None},
        "diagnostics": diagnostics,
    }


def counts_dates(observations):
    return Counter(o.date for o in observations)


def write_normalized_cache(case: dict):
    """Derived local cache only, never an original input or a public-demo asset."""
    import json
    RUNTIME.mkdir(exist_ok=True)
    (RUNTIME / f"normalized-{case['station']['id']}.json").write_text(
        json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")
