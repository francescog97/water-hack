# Reproducible demonstration

Run the production build locally at http://127.0.0.1:8000. The Start guided demo button resets the exact case/config below. Live feed and forecast are unavailable by design.

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
