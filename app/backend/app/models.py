"""Explicit evidence types. A scenario classification is never a legal designation."""
from datetime import date
from enum import StrEnum
from math import isfinite
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Band(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    DANGER = "DANGER"
    EMERGENCY = "EMERGENCY"
    UNKNOWN = "UNKNOWN"


class Observation(Model):
    observation_id: str
    source_id: str
    station_id: str
    waterbody: str
    observed_at: str
    date: date
    parameter: str = "discharge"
    value: float | None
    unit: str = "m3/s"
    provenance_file: str
    source_row: int | None = None
    raw_value: str | None = None
    mode: Literal["historical", "simulated", "live"] = "historical"
    quality_flags: list[str] = Field(default_factory=lambda: ["good"])
    time_precision: str = "day"
    latitude: float | None = None
    longitude: float | None = None


class RulePack(Model):
    id: str
    name: str
    version: str
    parameter: str
    unit: str
    station_ids: list[str]
    thresholds: dict[str, float]
    comparator: Literal[">="] = ">="
    source_classification: Literal["DEMO_CONFIG"] = "DEMO_CONFIG"
    validity: str
    rationale: str

    @model_validator(mode="after")
    def ordered(self):
        if set(self.thresholds) != {"WARNING", "DANGER", "EMERGENCY"}:
            raise ValueError("Exactly WARNING, DANGER and EMERGENCY thresholds are required")
        a, b, c = (self.thresholds[k] for k in ("WARNING", "DANGER", "EMERGENCY"))
        if not all(isfinite(v) for v in (a, b, c)) or not 0 <= a < b < c:
            raise ValueError("Thresholds must be finite, non-negative and strictly increasing")
        return self


class Facts(Model):
    jurisdiction_confirmed: bool | None = Field(default=None, strict=True)
    municipal_plan_available: bool | None = Field(default=None, strict=True)
    formal_disaster_declared: bool | None = Field(default=None, strict=True)
    basin_authority_confirmed: bool | None = Field(default=None, strict=True)


class ScenarioRequest(Model):
    case_id: str = "iskar-novi"
    selected_date: date = date(2025, 9, 25)
    rule_pack_id: str = "iskar-demo"
    legal_pack_id: str = "bulgaria-flood"
    simulate: bool = False
    daily_increase: float = Field(default=8, ge=0, le=100, strict=True)
    steps: int = Field(default=2, ge=0, le=7, strict=True)
    sensor_offline: bool = False
    stale: bool = False
    facts: Facts = Field(default_factory=Facts)


class ReviewRequest(Model):
    context_id: str
    item_id: str = Field(min_length=1, max_length=100)
    note: str = Field(min_length=10, max_length=2000)
    acknowledged: Literal[True]

    @model_validator(mode="after")
    def substantive_note(self):
        self.note = self.note.strip()
        if len(self.note) < 10:
            raise ValueError("A review note needs at least ten non-padding characters")
        return self


class BriefingRequest(Model):
    scenario: ScenarioRequest
    review_ids: list[int] = Field(min_length=1, max_length=100)
