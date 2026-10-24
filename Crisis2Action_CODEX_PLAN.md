# Crisis2Action — EIT Water Hackathon Sofia 2026
## Implementation plan and evidence contract for Codex `/goal`

**Status:** hackathon MVP specification, prepared 2026-10-24. **Deadline target:** 2026-10-25 before 14:30 in Italy (CET after the autumn clock change); confirm final delivery time in HackathonHost. **Team:** software/cloud engineer + environmental/regulatory specialist. **Language:** build and demo in English; optionally support Bulgarian later. **Context:** hybrid, remote team. **Primary case:** Bulgarian flood response. **Expansion:** drought, additional countries, hardware/IoT.

> **Mission:** Produce a working, polished, locally runnable web application that converts a *historical or explicitly simulated* river-flow event into transparent scenario risk classifications, traceable institutional information, source-linked procedural checklists, and a coverage/uncertainty matrix. Never confuse technical classification with an official emergency designation, or potential legal relevance with verified legal advice.

## 0. Operating rules for the implementation agent

1. **Actually implement** the MVP, not merely write a plan. Inspect the repository first; then build, test, and document. Make reasonable independent decisions and deliver a runnable artifact within this scope.
2. Do **not** delete, rename, overwrite, or mutate any files inside `Dataset/`. Preserve all original 172 files and metadata. Respect existing README, `DeepResearch-prompt.md`, `t1.png`, and the hackathon PDF. Read `Dataset/README.md` and category READMEs before selecting a case; inspect only small bounded samples initially. `t1.png` is a reference for layout, not a demand to duplicate aesthetics.
3. The PDF has access credentials. **Never print, log, commit, hardcode, screenshot, or expose credentials, tokens or private links in the app or repository.** Keep source PDF internal. Add `.gitignore` and redact logs if necessary.
4. No real emergency alerts, emergency dispatch, infrastructure actuation, or real-time legal determinations. This is **research/prototype decision support**, with mandatory human review. No external operations, public messages, or actuator commands.
5. Prefer deterministic, testable rules and source registries over LLM-generated claims. A model or chatbot is not needed to make the MVP compelling. If an LLM is later introduced, it may only help retrieve text; never supply uncited authority or compliance conclusions.
6. **No invented legal articles, thresholds, deadlines, locations, measured values, benefits, live feeds, or scores.** Demo thresholds may be chosen transparently as illustrative values for the observed variable and selected station. Keep `scenario`, `historical`, and `live` modes visibly distinct. Only claim a live feed if ingestion actually works and its timestamp is displayed.
7. Conduct every implementation iteration as: identify next smallest high-value deliverable -> edit -> run relevant checks -> inspect output -> fix -> log progress. Do not let decorative polish displace core correctness.
8. If external data or legislation cannot be retrieved/verified, keep a convincing **offline demo** using original local historical measurements and transparent synthetic scenario overlays. Mark legal records **UNVERIFIED** unless their exact provision, source version, and scope have been checked.
9. Build a useful fallback instead of stopping for noncritical missing information. Stop and report genuine blockers only when requirements cannot be met truthfully.
10. Scope work to this repo. Do not deploy publicly or push to GitHub without explicit permission. Development dependencies and local test commands are fine. Do not access private remote systems. No unnecessary cloud services.

## 1. Product thesis and intended differentiation

**Working name:** Crisis2Action — *From Water Signals to Legally Traceable Decisions*.

**Users:** municipal civil-protection officers, water utility operation/administrative staff, basin authority analysts, and environmental/regulatory consultants. For MVP, optimize for **one municipal crisis coordinator** using Bulgarian historical data.

**Core user question:** "This hydrological signal is getting worse. Which institutions should be consulted, which procedures might apply, what is each claim based on, what remains unverified, and what do we need to do next to prepare a responsible decision?"

**Distinct product hypothesis:** EXISTING flood products emphasize monitoring, forecasting, maps and plan implementation. Crisis2Action tests a *case-specific chain of evidence*: observed signal -> scenario rule -> possible institutional responsibility -> sourced provision or plan -> approval/review checklist -> documented audit record. Add explicit gaps in **coverage of the project's legal knowledge package**, not unsupported declarations of legislative deficiencies. An operational bridge, not a national warning system or a generic legal chatbot.

Known adjacent services to compare honestly in docs/pitch:
- Bulgarian ISURN flood-risk management information system: https://isurn.moew.government.bg/ISURN.Web/BaseProject/homepage/aboutEN.html
- Bulgarian 2022–2027 Flood Risk Management Plans: https://www.moew.government.bg/en/flood-risk-management-plans-for-the-period-2022-2027-have-been-adopted/
- Copernicus Emergency Management: https://emergency.copernicus.eu/
- Mozaika ISME-HYDRO, MERATCH/Floodar, DSLL LLcloud (research as needed; don't claim feature absence without evidence).

**Unique demo moment:** Advance a historical/simulated flood from WARNING to DANGER. The evidence-linked action workspace updates, highlights which institutional role is relevant **under stated conditions**, reveals one deliberately missing or unreviewed procedural field, and requires a human acknowledgement before exporting a draft briefing. Swap the threshold config (or legal-package config) live; show that results change without source-code edits. Also trigger a stale/missing-data scenario and show the system refusing an unjustified forecast or recommendation.

## 2. Local resources: inspect these, do not assume more than the inventory states

Repo root: `C:/Development/Repositories/eit-hackathon` (use actual current working directory; support Windows paths, never hard-code them into app).

- `README.md`: project overview.
- `Dataset/README.md`, per-folder README files, `Dataset/registro_rinomine.csv`: dataset catalogue, rename provenance and SHA-256. Use as the first source of truth.
- `DeepResearch-prompt.md`: background and ideation; not app logic.
- `t1.png`: prior user mockup of risk dashboard, forecasts, action plan, maps, legal matrix. Evaluate for UI guidance.
- `EIT Water Hackathon Sofia 2026 v7.pdf`: event details, jurors and mentor information, **includes confidential credentials**. Do not distribute.

Dataset inventory supplied by the user (verify in actual files):

| Category | Files & coverage | Use for this MVP | Critical caveat |
|---|---|---|---|
| `groundwater Bulgaria` | 22 CSV; ~133k water-chemistry observations 2018–2024 | Background/future quality track, maybe an optional catalog card | No station IDs or coordinates; NOT flood alerts |
| `surfacewater Bulgaria_best` | 39 CSV; ~335k records 2019–2024 | Background / future environmental layer | `best` is filename, not proven quality classification; no spatial station mapping |
| `surfacewater Bulgaria_weak` | 28 CSV; ~41k records 2019–2024 | Background / future environmental layer | `weak` is NOT proven pollution status |
| `portata_iskar_novi_iskar_2025.csv` | 146 daily discharge observations, July–Dec 2025 | **Preferred primary single-station historical flood scenario** | **m³/s flow**, not water level in meters. 27 missing calendar days; verify duplicates and timestamps |
| `portata_iskar_orehovitsa_2025.csv` | Another 2025 discharge series | Second station / compare if schema, location, and chronology confirmed | Do not infer direct hydrologic propagation/travel times between gauges |
| `Danube/` | 2 CSV, station bulletins June–Nov 2021 | Optional alternate sample | Repeated header rows, blank cells, text values |
| `cds_output/` | 26 GeoTIFF + 2 CSV, mostly precipitation and soil moisture, monthly 2024 | Optional historic/map layer only with correct 2024 labels | Grid ~0.1°, aggregation and missing cells need checks; NOT simultaneous 2025 rain |
| `gee_output/` | 27 GeoTIFF + 3 CSV, 2024 and precipitation Mar–Apr 2026 | Optional exploratory geospatial layer | Sensor/units/aggregation undocumented; NO unsupported overlays |
| `Cascade Arda/` | 11 `.xls`, 334 daily bulletins for 3 reservoirs, Feb–Dec 2017 | **Fallback/optional second narrative**: reservoir monitoring, physical volume/level changes | Verify workbook structure, formulas, units; don't infer mandated gate operations |
| `Fishing Black Sea/` | 2 PDFs, 1 DOCX, 4 images | Exclude | No flood-relevant sensor measurements |

Total user-supplied inventory: 172 original dataset files, about 21 MB. If local files differ, record exact observations rather than forcing these counts.

**Data-source selection decision:**
1. Load/inspect the two Iskăr discharge CSVs, their metadata and actual stations. If clean enough, use **one selected 2025 Iskăr station** as the primary working event to avoid incompatible dates and units.
2. Use actual historical discharge values in m³/s. Derive transparent illustrative thresholds from explicit config, not "Bulgarian official limits". Choose threshold values only after inspecting the numerical distribution; mark as demo-defined. Showing changes to illustrative thresholds is a FEATURE, not a claim of official warning regimes.
3. Optional: replay a short **synthetic future path** derived from a specified scenario configuration. Render it differently from historical measurements. It is NOT a calibrated prediction.
4. If Iskăr series cannot be parsed or lacks required timestamps, use Arda reservoir historical records and a more suitable reservoir-operations monitoring story, with caveats. **Never mix Arda 2017, Iskăr 2025, 2024 rasters or 2026 precipitation as though they describe one event.**
5. NIMH external feed is optional, *after* offline demo works. Bulgarian NIMH open portal: https://info.meteo.bg/openData/ and https://info.meteo.bg/openData/river-runoff (daily discharge published for a set of stations). Verify station identity, unit, licensing, dates, reliability and access before claiming integration. Fail closed to local mode.
6. The water-chemistry tables may be profiled and listed as "available for future quality-of-water pack" but shall not be plotted at invented coordinates or attached to the chosen event without crosswalk evidence.

## 3. Scientific engine and uncertainty contract

Create a canonical `Observation` representation:
- `observation_id`, `source_id`, `station_id`, `waterbody`, `observed_at`, `parameter` (e.g. `discharge`), `value`, `unit` (e.g. `m3/s`), `provenance_file`, `mode` (`historical|live|simulated`), `quality_flags` (`missing|duplicate|outlier_suspect|stale|good`), optional verified lat/lon.
- `Station` registry with raw station name, display name, basin, region/municipality only when source-verified, coordinates nullable. NO generated pseudo-coordinates.
- Preserve all raw values and source row references; never silently interpolate missing days. Expose missing 27 calendar days as gaps when verified.

Three user-visible demo bands: `WARNING`, `DANGER`, `EMERGENCY`; optionally `NORMAL`, `UNKNOWN`. Define them by a versioned **ScenarioRulePack** with explicit parameter, units, selected station/case, thresholds, comparator, source classification (`DEMO_CONFIG` vs `OFFICIAL_VERIFIED`) and validity. Do not assert they activate any statutory powers.

Use simple deterministic classification; validated units are mandatory. Test boundary equality, negative or null values, reversed threshold ordering, missing values, stale timestamps, and unit mismatch. Default to `UNKNOWN` when input cannot be trusted. Time-zone display uses Europe/Sofia or user-friendly locale; preserve UTC timestamps internally.

Forecast/next-threshold feature:
- Primary: show a user-configurable **what-if timeline** with explicit assumptions (e.g., scenario inflow/flow rises at a configured rate), distinctly titled *Illustrative threshold-crossing simulation*.
- Optional: historic-slope extrapolation ONLY if there are enough recent uninterrupted observations and positive trend; display it as extrapolation, not a hydrological forecast; mark confidence/limitations. If not defensible, show "Unavailable: insufficient evidence" rather than fabricating minutes/hours.
- If using daily data, **do not display minute precision** for threshold estimates. Use dates or time steps consistent with the underlying series. Do not equate a water-level threshold in meters with a discharge threshold in m³/s.

For a convincing demo, ensure crossing changes *scenario status* while the corresponding legal result updates **only when a verified legal rule with all relevant conditions exists**. A simulated threshold alone cannot trigger legal duty.

## 4. Legal/institutional engine: central differentiation and safety-critical guardrails

**Central design rule:** technical alert severity != formal disaster declaration != legal trigger != automatically authorized action.

Use an immutable/traceable `LegalPackage` (JSON or YAML) with versioned records:

- `source_id`, `source_title`, `publisher`, `official_url`, `language`, `document_type` (statute / flood-risk plan / municipal procedure / guidance), `version_or_last_verified`, `retrieved_at`, `effective_date_from/to` if independently verified, `article_or_section`, `exact_quote` optional bounded fair-use, `paraphrase`, `translation_status`, `review_status` (`VERIFIED_BY_DOMAIN_EXPERT`, `SOURCE_LOCATED_UNREVIEWED`, `DEMO_ONLY`, `UNKNOWN`), `reviewer` optional.
- `authority_id`, `authority_name`, `jurisdiction_scope`, `role_type`, `legal_source_ids`, `conditions`, `confidence_label` or review state.
- `procedure_id`, `title`, `action_type` (`POSSIBLE_MEASURE`, `REQUIRED_STEP`, `INFORMATION_REQUEST`, `REVIEW_TASK`), `trigger_conditions`, `applicable_authority_ids`, `deadline_value`, `deadline_unit`, `deadline_type` (`STATUTORY`, `PLAN`, `INTERNAL_TARGET`, `NONE_VERIFIED`), `dependencies`, `source_ids`, `verification_status`, `notes`.
- `LegalRule` should be **condition-based**, not severity-equals-power. It may evaluate legal facts manually supplied (declared disaster? competent geographic authority? specific plan? river basin?) only when reviewed and sourced. When facts are missing, return `NEEDS_VERIFICATION`.

**Official primary-source leads to research carefully (do not auto-assert exact clause interpretations):**
- Bulgarian disaster management structure overview by European Commission: https://civil-protection-humanitarian-aid.ec.europa.eu/what/civil-protection/national-disaster-management-system/bulgaria_en
- Bulgarian Disaster Protection Act official government landing page: https://www.me.government.bg/en/library/disaster-protection-act-304-c25-m1515-1.html
- Official Bulgarian Ministry of Interior legal index: https://www.mvr.bg/gdnp/дирекцията/нормативна-уредба/zakoni (verify redirect/availability; alternatives okay)
- Bulgarian MOEW 2022–2027 FRMP page: https://www.moew.government.bg/en/flood-risk-management-plans-for-the-period-2022-2027-have-been-adopted/
- ISURN description: https://isurn.moew.government.bg/ISURN.Web/BaseProject/homepage/aboutEN.html
- Official Bulgarian Water Act PDF source (may not be consolidated through every 2026 amendment): https://moew.government.bg/static/media/ups/tiny/file/Legislation/Zakoni/Zakon_za_vodite.pdf
- 2026 Water Act amendment adopted/published by Bulgarian parliament: https://www.parliament.bg/en/desision/ID/167018

A September 2026 Water Act amendment *proposal* appears in Bulgarian parliament records. **A draft bill is NOT enacted law.** Codex must distinguish enacted amendments from proposals, and must verify applicable wording and effective dates for the event. Do not trust unversioned English translations as up-to-date law.

Seed 3–5 **source-linked, reviewable** institutional/plan cards from the most defensible public facts (e.g., municipality mayors' disaster-management role, regional governors' role, Basin Directorates' flood-risk planning responsibility), clearly separating planning responsibilities from concrete emergency powers. EITHER confirm the precise current clause and show `SOURCE_LOCATED_UNREVIEWED` until Aliaksei reviews it OR use deliberately marked demo-only placeholder mappings. Do not hardcode assertive instructions such as "Mayor MUST evacuate within two hours".

**Coverage matrix** (provisional evaluation of the loaded package, NOT identification of missing legislation):
rows = scenario classifications `NORMAL`, `WARNING`, `DANGER`, `EMERGENCY`;
columns = `Authority`, `Possible measures`, `Deadlines`, `Procedures`, `Legal sources` (and optionally `Conditions`).
Cell statuses = `VERIFIED`, `SOURCE_FOUND_REVIEW_PENDING`, `UNMAPPED`, `NOT_APPLICABLE`, `DEMO_ONLY`.
For `UNMAPPED`, explain "No verified mapping in the loaded knowledge package". NEVER "Bulgarian law has a gap" unless separate genuine legal analysis confirms it.

**Review workflow**:
- Operator can view cited original, mark a draft item reviewed/acknowledged (client session or local SQLite), write a note, export an *unapproved draft* briefing with source list and quality caveats.
- All records track whether official text, translation, and law-package mapping were reviewed by a domain expert; if no expert review, clearly say so.
- Do not present an approval click as a legally valid institutional decision. Do not forge signatures or officials.
- Missing data and unverified obligations must become prominent review tasks, never hidden.

## 5. UX / screens: make it presentation-grade but functional

Design: modern minimal public-sector intelligence dashboard, charcoal/navy text, restrained teal/cyan accents, warm amber only for uncertainty, strong accessibility and spacing; useful on laptop (1366x768) and responsive. English UI. Prominent **DEMONSTRATION · NOT FOR OPERATIONAL USE** banner and **Historical observation / Synthetic scenario / Live verified** mode label visible throughout. Add labels for units, sources, station and dates.

Five routes or tabs (avoid complexity if necessary):

1. **Overview / Crisis Monitor** — case selector (Iskăr station, optional Arda fallback), clean timeline of historical **discharge in m³/s** with data gaps, bands with demo-only legend, source/date freshness, current historic-selected observation, scenario launch, risk summary. A map only if positions are VERIFIED; otherwise a tasteful basin/station info panel, no invented map pins.
2. **Scenario Lab** — scrub a timeline or press "Simulate rising discharge". Visible water-flow diagram (SVG) and 3-band risk indicator; controls for scenario rate and starting observation; side-by-side observed vs projected plot with dashed styling; "sensor offline" and "data stale" controls; if unknown, degrade to UNKNOWN. Events update shared global state consistently.
3. **Response Navigator** — for selected timestamp/severity, cards showing institutional responsibilities, possible measures, whether prerequisites are met/unmet/unknown, verified legal citation with clickable URL, any deadline type, explicit evidence confidence, and required human checks. Ordering: "What we know", "What to verify", "Possible next review steps". No legally binding auto decisions.
4. **Regulatory Coverage Matrix** — severity × authority/measures/deadlines/procedure/sources; state legend and click-through evidence drawer; highlight incomplete knowledge package, not legislator's presumed failure.
5. **Legal Package & Evidence** — list of loaded laws/plans with jurisdiction, sections, dates, verification statuses and references; package selector/config inspection; working demo of config swap. Optional download of a draft incident briefing with evidence & limitations. A separate `Dataset Sources` side panel is useful.

Global interactions MUST be wired to real state and actual data (not decorative controls). Include one guided **Demo Tour** or numbered on-screen narrative to run in ~90 seconds.

Optional: use `t1.png` for visual inspiration. Avoid generic flashy sci-fi command centers and unnecessary graphics. The central wow factor is **clickable provenance and explainable state transitions**.

## 6. Tech stack and interfaces

Preferred if repo is empty: **React + Vite + TypeScript + Tailwind CSS** frontend; **Python FastAPI + pandas** backend; SQLite or bundled JSON for audit events and legal/source packs. Prefer `Recharts` for timeline, `Lucide` icons, plain SVG for conceptual flow; map library optional and only if trustworthy coordinates exist. A single-process Streamlit alternative is acceptable ONLY if faster and similarly usable. Do not add infrastructure complexity. Compatible with Windows PowerShell and local development.

Suggested minimal structure (adjust to existing repo):

```
app/
  frontend/src/{components,pages,lib,types,styles}/
  backend/app/{main.py,models.py,ingest.py,rules.py,legal.py,scenario.py,briefing.py}/
  backend/tests/
  config/rulepacks/{iskar-demo.json,alternate-demo.json}
  config/legalpacks/{bulgaria-flood.json,fictional-test-only.json}
  public-demo/ (small generated cleaned sample, if redistribution/license allows)
  scripts/ (data profile and demo preparation)
  docs/{DATA_AUDIT.md,LEGAL_EVIDENCE.md,DIFFERENTIATION.md,DEMO_SCRIPT.md,PITCH_OUTLINE.md,PROGRESS.md}
```

Possible API routes:
- `GET /api/health`
- `GET /api/cases` / `GET /api/cases/{id}/observations`
- `GET /api/sources`
- `GET /api/rulepacks` / `POST /api/simulate` (validate scenario config and compute)
- `GET /api/legalpacks` / `POST /api/response/evaluate` (deterministic, no LLM)
- `GET /api/coverage?legal_pack=...`
- `POST /api/briefings` (produces **draft** JSON or print view; source and warning included)

Prefer simple schema-validated APIs; do not include users/auth unless a realistic need exists. No cloud, secret keys, external paid AI, or telemetry required for demo. If adding IoT extensibility, define interfaces like `SensorObservationProvider` and `ActuatorProposalSink` but DO NOT command real hardware. MQTT adapter is roadmap-only, or entirely simulated in memory if it improves demo clarity.

Source- and package-switchability must be **demonstrated with actual JSON config changes**, not claimed from folder naming.

## 7. Data audit and trustworthy integration: mandatory artifacts

Generate `docs/DATA_AUDIT.md` with a compact, actual-file audit: verified path, rows, periods, variables, units, missingness, sample source rows, and selected primary case. Respect SHA-256 registry and avoid modifying source data. Clearly state why 2024 rasters and 2018–24 unlocated chemistry observations cannot be treated as spatially joined with 2025 Iskăr.

Build a repeatable loader and small normalized cache. Handle day-month/year, decimal commas, Bulgarian encodings, duplicated headers, Excel legacy readers, missing dates and optional external NIMH latency. If a file is malformed, provide helpful diagnostics, not silent data replacement. Do not assume time or station location from filename alone without documenting verification.

If original local data cannot ship in a distributable demo, bundle a few source-compatible sample rows with clear license and provenance or a small separately labelled synthetic dataset, and keep the ingestion adapter intact.

## 8. Model and rules evaluation tests (automated)

At minimum tests must cover:
1. Exact threshold boundaries, sorted thresholds, and unit consistency.
2. Missing observation -> UNKNOWN, not safe; stale observation -> UNKNOWN or STALE.
3. Historical input not represented as live or current.
4. Discharge `m3/s` never mislabeled water level `m`.
5. 2025 Iskăr timestamps and 2017 Arda not accidentally joined with 2024/2026 meteorological rasters.
6. Two stations cannot be mixed without independent ID/metadata match.
7. Simulated future values styled and labeled separate from observations.
8. Crossing-time simulation cannot imply validated forecast or minute precision for daily data.
9. Deterministic legal engine doesn't infer statutory powers solely from risk band.
10. Legal result without citation and source verification is withheld or marked unverified.
11. No statutory deadline shown if `deadline_type != STATUTORY` and evidence incomplete.
12. Coverage matrix `UNMAPPED` does not assert a law is absent.
13. Config pack A vs B yields a predictable state change with no code edit.
14. Review acknowledgement creates an audit record but not an official authorization.
15. Export contains visible simulated/historical warning and cited sources.
16. API schema validation: invalid numeric inputs, ranges, date and legal-pack IDs.
17. Offline mode works without network and survives a missing optional external feed.
18. All usable UI controls visibly change state, and source links open appropriate URLs.
19. No secret strings or confidential credential-containing PDF copies in built frontend artifacts.
20. `npm run build` and backend tests pass; smoke-test startup commands.

If Playwright is installed or easily added, script an end-to-end smoke test: launch -> choose station -> choose historic date -> run scenario -> see level change -> inspect responsibility with source -> see unmapped cell -> export draft. If browser automation unavailable, document manual smoke test instructions and run what tools permit.

## 9. Work phases: prioritise vertical slice over features

### Phase 0: inventory and decisions (short)
Inspect repo, source files, sample of Iskăr data, t1.png and legal-source availability. Write brief `docs/PROGRESS.md` with actual findings and decisions. **Do not spend hours auditing every dataset before building.**

### Phase 1: functional core
One station and one valid historical discharge timeline, scenario threshold config, deterministic classifier, scenario stepping and API. Unit tests. Confirm historical vs simulated labels.

### Phase 2: legal traceability and human review
Versioned legal/source pack (small!), institutional cards, condition evaluation, coverage matrix, audit log, demo-only fallback pack. Validate exact provisions with official sources; clearly mark unreviewed mapping. Give Aliaksei a concise `docs/LEGAL_REVIEW_CHECKLIST.md` asking for 3–5 clause reviews.

### Phase 3: polished UI + guided demo
5 views or fewer, responsive layout, UX-first transitions, source drawer, offline fallback, failure injection (sensor stale), export draft. Make 90s demo smooth. Use realistic data where available.

### Phase 4: pitch-ready and documented
Create `docs/PITCH_OUTLINE.md` with max 8 slides (unless event portal confirms different number): 1 Problem; 2 Fragmented workflow; 3 Market gap & adjacent solutions; 4 Crisis2Action approach; 5 Live demo; 6 Trust/provenance/modularity; 7 Who pays and value hypothesis; 8 Team + roadmap + pilot. State claimed market/impact metrics as hypotheses pending validation. In `docs/DIFFERENTIATION.md`, explain specific differences vs ISURN/monitoring tools without unsupported uniqueness claims.

### Phase 5: verification and handoff
Run lint, typecheck, frontend build, backend tests, and local startup. Write `docs/DEMO_SCRIPT.md`: 90-second reproducible scenario with fixed station/date/steps, plus 3-minute backup explanation. Include screenshot instructions. Record tests run, errors remaining, blocked source claims, and intended handoff to teammate.

**Priority order:** (1) working evidence-linked journey; (2) credible data provenance; (3) trust/uncertainty and tests; (4) pitch/demo UX; (5) secondary datasets, maps, bilingual UI, speculative forecasting, live integrations. Strictly de-scope 5 if anything earlier is broken.

## 10. Acceptance criteria / definition of done

The Goal can be considered complete only when:

1. The app starts locally via documented commands and works offline with at least one **real local historical** river discharge dataset unless source unavailability is explicitly reported.
2. Historical series has correct measured variable, units, station, dates, missing-data handling, and citations to origin file/source.
3. A user launches a **clearly labelled synthetic scenario**, sees `WARNING -> DANGER` (or an equivalent risk change using chosen demo thresholds), and a consistent update through dashboard, navigation and coverage views.
4. An institutional/procedural card points to a trustworthy primary source or is explicitly `UNVERIFIED`/`DEMO_ONLY`, and clicking shows conditions and gaps in knowledge. At least 3 evidence entries should be source-linked if public access permits.
5. The legal engine cannot transform demo severity into a legal power/obligation automatically. No invented deadlines, emergency triggers or authorized measures.
6. The coverage matrix has all requested axes and distinguishes `VERIFIED`, `SOURCE_FOUND_REVIEW_PENDING`, `UNMAPPED`, `NOT_APPLICABLE`, `DEMO_ONLY`.
7. Switching demo rule packs changes behavior without code edits; failure injection shows missing data/uncertainty and avoids fake forecasts.
8. Every key interactive control works; a clean 90s demo exists; a shareable draft briefing/print view includes a source ledger, caveats and human-review status.
9. Tests and build pass, or failing checks are clearly identified with reproduce steps. Provide `docs/DATA_AUDIT.md`, `docs/LEGAL_EVIDENCE.md`, `docs/DIFFERENTIATION.md`, `docs/DEMO_SCRIPT.md`, `docs/PITCH_OUTLINE.md`, `docs/PROGRESS.md` and human review checklist.
10. No original data or confidential PDF modified, no secrets included, no unapproved deploy/push.

## 11. Evidence and status discipline for all outputs

Every important panel/report must distinguish:
- `HISTORICAL OBSERVATION` — measured in local file at stated historical timestamp.
- `SIMULATED SCENARIO` — value created by the app with documented assumptions.
- `EXTERNAL LIVE OBSERVATION` — only if an external feed is actually running and its timestamp, freshness and station provenance have been checked.
- `DEMO RISK RULE` — provisional thresholds, never official Bulgarian thresholds.
- `VERIFIED LEGAL SOURCE` — exact document provision and version located; expert-reviewed mapping only when specifically marked.
- `SOURCE FOUND, INTERPRETATION UNREVIEWED` — public statute may exist but applying it to this event is unresolved.
- `KNOWLEDGE PACKAGE UNMAPPED` — missing from currently configured database, **not** necessarily a gap in the law.

Don't call this emergency-management automation. Call it **decision preparation and procedural traceability**.

## 12. Questions to hand to Aliaksei (do not block implementation)

1. Which single institutional persona and geography should the demo represent? If uncertain, use a generic municipal crisis coordinator and label jurisdiction verification pending.
2. Can you review 3–5 official Bulgarian statutory / flood-plan provisions for precise actor, role, prerequisite, obligation vs discretionary power, and date/version?
3. Does a real incident illustrate fragmented access to responsibilities or procedures? If none verified, describe the problem as a hypothesis and do not fabricate a case study.
4. Are warning/danger/emergency bands only a UI demo classification or can a station-specific official threshold be verified? Default to demo-only.
5. What would be the single concrete output this institutional user most needs: a briefing, evidence checklist, or assignment draft? Default to **traceable review briefing**.

## 13. Handoff

At the end report: (a) what was actually built, (b) paths added or changed, (c) commands to run on Windows, (d) exact datasets used, (e) verified/unverified legal claims and missing facts, (f) tests/build/smoke outcomes, (g) 90-second demo steps, (h) outstanding risks, and (i) the next single highest-value improvement.

**Non-negotiable:** It is better to show a truthful and useful decision-support MVP with unresolved legal mappings than a polished but fictitious system that tells authorities what the law requires.
