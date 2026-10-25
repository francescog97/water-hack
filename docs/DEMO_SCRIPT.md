# Reproducible pollution navigator demonstration

Build and run locally using [RUN_LOCAL](RUN_LOCAL.md), then open http://127.0.0.1:8000. The default is **Water Crisis Decision Navigator**. The existing protected cloud URL may still serve the previous release until this work is deployed; consult [VALIDATION](VALIDATION.md) for current evidence.

## Reset and prepare

Select English for the labels below, or switch to Italiano, Русский or Български. Choose **New exercise** to create a fresh persistent incident for each rehearsal; earlier records/history remain retained. If no incident exists, choose **Start incident record**. Record the new incident identity so exports can be matched to it. These are self-declared demonstration personas, not institutionally verified identities.

## 90-second product story

| Time | Action | Say / verify |
|---|---|---|
| 0–15 s | Observation & evidence | Invented suspended solids increase from 8 to 96 mg/L: 12×. The 30 mg/L `>=` trigger is a demo setting, not an environmental quality standard. There is no actual laboratory report, contaminant identification or confirmed pollution. |
| 15–28 s | Potential receptors | All geometry and intake, habitat, settlement and industry markers are invented. Downstream relation/exposure need independent verification; no arrival time or dispersion forecast exists. |
| 28–43 s | Institutions & legal checks; open a source | Danube Basin Directorate and RIEW Sofia are candidate routes. Five source-backed procedure checks remain unreviewed. A source link does not establish jurisdiction, a duty or a deadline. |
| 43–70 s | Action plan & history | Show the five required verification tasks, named roles and evidence notes. Explain the explicit demonstration specialist review gate, assigned response tasks and traceable revisions. Use the prepared rehearsal record below if time is limited. |
| 70–90 s | Export; Pilot & value | Download the draft and full evidence JSON; nothing is sent. Show buyer/user/budget roles, assumption-based economics and the proposed equivalent-task customer test. No customer study or paid pilot is claimed. |

The real 9,657-row anonymous historical TSS file and 2024 CDS cells are separate context, without a station/time join to this exercise. Suspended solids in mg/L are not turbidity in NTU or a PFAS result.

## Full repeatable workflow / rehearsal record

1. Start a fresh exercise. In **Action plan & history**, open each of the five required verification tasks: sample provenance/units; uncertainty/alternative explanations; receptors/exposure; candidate authority routing; procedure sources/legal applicability.
2. For each task, enter a demonstration assignee and explicit demo role, choose **completed**, and save a specific evidence note. Example: “Demo Analyst / Environmental analyst — demo role. Checked synthetic sample ID and mg/L; no laboratory report or station-matched field evidence exists.” Adapt each note to the task; retain unresolved gaps. These are self-reported checks, not proof that external evidence has been obtained.
3. Before review, show that response progression requires specialist approval. Enter a reviewer name, simulated role and reason of at least five characters; acknowledge the demo-role disclosure. Choose **Approve demonstration plan**. Explain that this records a simulated review only and leaves source/legal/pollution verification unchanged. **Request changes with reason** demonstrates a reasoned return for further work.
4. Open a response task, assign an owner and role, record a specific note, then move through specialist-approved / in progress / completed as appropriate. Demonstrate **rejected** with a reason on another task; no external laboratory work or delivery is implied by these statuses.
   An optional internal target can be entered and cleared; it is never a statutory deadline. To reconsider a rejected task, explicitly reset it to **system suggested** with a reason; this revokes the previous approval and requires a new demo review before response execution.
5. Record an outcome note and **Continue monitoring**, or **Close as unconfirmed**. Inspect the ordered timeline, actors, revisions and reasons. Refresh and verify the same incident and recorded state return. Stale revisions require refreshing rather than overwriting newer work.
6. Download the Markdown draft and full evidence JSON. Match the incident identity/revision, verification/review state, assignments and timeline. Exports retain original evidence language and limitations. No notice is sent and no official authorization appears.
7. For a gate-reset demonstration, edit a required verification after approval: the previous demo approval is revoked, and response work requires a new review. Use **New exercise** again before the next rehearsal; do not erase prior history to reset the demo.

## Pitch and presentation backup

Open **http://127.0.0.1:8000/presentation.html** for the nine-slide Italian browser pitch. Navigate with arrow keys, show speaker notes and use print for a paper/PDF backup. The source is `app/frontend/public/presentation.*`. Match visible functionality to the local build; do not imply the current public release has already been updated. Qualified legal/scientific sign-off, current jurisdiction and permits, actual interviews and a measured customer pilot remain pending.

Keep synthetic labels and source limitations visible in screenshots. The app works locally after setup; opening original external sources requires a connection. Never include the confidential event PDF in captures or public assets.

---

# Retained historical flood demonstration

Open http://127.0.0.1:8000/?module=flood after the production build. The Start guided demo button resets the exact case/config below. Live feed and forecast are unavailable by design.

## 90 seconds

| Time | Action | Say / verify |
|---|---|---|
| 0–12 s | Start guided demo, Crisis Monitor | Novi Iskar, 25 September 2025, 9.922 m3/s, original CSV row 77. This is a historical measurement, not live. WARNING comes from demo thresholds |
| 12–27 s | Next → Scenario Lab | A synthetic increase of +8 m3/s per whole day over 2 days produces 25.922 m3/s and DANGER. Dashed line is not a calibrated forecast |
| 27–43 s | Next → Response Navigator; open a source card | The review emphasis changes. Potential institutional relevance is sourced, but local jurisdiction and procedure are unverified. No power or deadline is activated |
| 43–53 s | Close source; Next → Coverage Matrix; inspect DANGER/Deadlines | UNMAPPED describes our loaded package, not a gap in Bulgarian law |
| 53–65 s | Next → Legal Package & Evidence; select Alternate higher thresholds | The same 25.922 m3/s is WARNING under 15/35/70 instead of DANGER under 8/20/50. This is actual JSON-driven behavior |
| 65–90 s | Next → Response; Finish the guide, enter a note, acknowledge, download draft | Example note: “Historical source checked; jurisdiction and current legal interpretation remain pending.” Export remains an UNAPPROVED DRAFT with citations and limitations |

The tour is a guide, not an automatic assertion that a reviewer completed the checks. Notes and acknowledgement must be entered by the operator. Briefing download is disabled until acknowledgement succeeds for the exact current context.

## Additional trust demonstrations

1. In Scenario Lab select **Show a real missing day** (10 October 2025). Result: UNKNOWN, no fabricated observation or simulated path.
2. Restore 25 September. Toggle Input stale / Input unavailable. Result: UNKNOWN, no forecast. These toggles are failure injections, not real sensor status.
3. Change daily increase or whole-day horizon. Values and review fingerprint update.
4. Swap legal package to institutional references only. Procedures become UNMAPPED and no procedure cards are shown.
5. After acknowledgement change station/date/package/facts. Export disables until a new acknowledgement.
6. Open Dataset sources: 146 rows, 27 gaps, original row reference, source hash, license and timestamp caveats.

## Three-minute backup explanation

- 0:00–0:35: show the original CSV identity and real-date gaps. Explain m3/s vs water level and why no map pin appears.
- 0:35–1:10: contrast the observed anchor and synthetic trajectory. Inspect configured thresholds; no calibrated forecast is available.
- 1:10–1:45: open EC/MOEW source records. Show the dated statute warning and missing legal prerequisites.
- 1:45–2:20: inspect the knowledge-package matrix and live config swap.
- 2:20–3:00: acknowledge uncertainty, export draft, show source ledger and lack of official authorization.

## Screenshots / offline backup

`npm run test:e2e` writes overview, scenario and coverage desktop screenshots, a mobile screenshot and a downloaded draft under ignored `test-results/`. Open only those app screenshots for presentation. Never screenshot or copy the confidential event PDF. A source drawer shows bounded paraphrases and original URLs; opening originals requires network, but the app and source cards work offline.

For a manual capture: use a 1366×768 or larger browser, reset the tour, wait for Updating to finish, capture the overview, scenario, source drawer, coverage and draft. Keep DEMONSTRATION and historical/simulated labels visible. Do not present screenshots as proof of a live service.
