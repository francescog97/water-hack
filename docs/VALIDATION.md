# Acceptance evidence — updated 25 October 2026

This records checks actually executed against the implementation, not intended future work. Tests establish software behavior and input integrity; they do not establish forecast accuracy, legal validity, customer value or operational readiness.

## Report-alignment branch — 25 October 2026, 12:36 UTC

Branch: `feat/water-crisis-navigator-alignment`, based on unchanged `main` commit `ef3c636`. This is a locally verified hackathon demonstrator. The existing Cloudflare deployment remains the previous release; this branch has not been deployed or merged.

| Actual check | Result |
|---|---|
| `npm run test:backend` | **93 passed**; includes SQLite/D1-adapter owner isolation, real main middleware boundary, atomic revisions, rejected-task reset/reapproval, same-mutation timeline revisions, evidence-rich export, aware optional internal targets, invalid/missing scenario fail-closed and original hashes |
| `npm run test:e2e` | **12 passed** in Microsoft Edge: six retained flood/language checks, two economics/comparison checks and four pollution/presentation/language/failure checks |
| Frontend | Typecheck, lint and production build passed; legacy flood module loads separately |
| Gateway | Typecheck and **3 security tests passed**; authentication/policy unchanged |
| `npm run audit:data` | **172 original file hashes matched**, both historical Iskar adapters usable, no input modifications |
| DOCX integrity | SHA-256 remains `4003771c60a88b8d319e3287993f03b7108c971c5bc894e620d76ffd1140d2d0` |
| Catalog integrity | All previous locale entries preserved: IT 324, RU 324, BG 325. Current totals IT 743, RU 749, BG 746; UTF-8 JSON parses without replacement characters |
| Bundle preparation | 13 explicit backend modules and 7 selected data/config inputs; research tree and confidential inputs excluded |
| Visual inspection | Actual desktop workflow, 390px mobile navigator and Italian economics slide screenshots inspected; no horizontal overflow in relevant browser checks |

The new end-to-end browser run creates a fresh exercise, inspects the constructed 96 mg/L sample and four schematic receptors, opens original source provenance, completes five named demo checks, records explicit demo approval, assigns/completes/rejects response tasks, records an internal target, closes unconfirmed, exports JSON and reloads persisted state. Export assertions retain no official authorization/dispatch and an unconfirmed finding. Backend tests additionally verify complete Markdown evidence, rejection-reset gates and legal/source flags.

The economics checks retain the insurer's negative €5,000 illustration and reject invalid assumptions. Customer-comparison inputs start empty; entered values export as self-reported, not as independently measured pilot evidence. The Italian nine-slide browser pitch supports keyboard navigation, notes and mobile display. Screenshots, traces and JSON results are local ignored test artifacts under `test-results/`.

Initial browser checks exposed numeric sidebar suffixes in accessible button names and same-document pitch hash navigation; both were fixed before the complete 12-test passing run. Independent review found four workflow/evidence issues, fixed with backend regression tests. Restricted Windows subprocess execution initially returned EPERM for Vite/test runners; authorized local execution resolved it. Remaining non-failing diagnostics: a roughly 550 kB initial JS chunk warning and one Starlette/httpx test-client deprecation warning.

**External gaps remain open:** no professionally verified event-specific Bulgarian legal package, confirmed jurisdiction/permits, actual incident sample, satellite retrieval, validated dispersion forecast, customer interview or measured customer pilot. Five source-backed procedure checks are research leads. Completing a demo task/review does not close these gaps. Operational legal acceptance M07 remains pending; the complete software demonstration uses the truthful fallback specified in the alignment audit. Current claim-source checks and retrieval limits are in [HACKATHON_STORY](HACKATHON_STORY.md).

New cloud schema/API acceptance is local/adapter-tested only. A future release must apply additive migration `0002_incidents.sql`, deploy backend and gateway, then retest actual D1, owner isolation, browser workflow and public Access redirects. Prior production evidence below is historical, not proof of deploying this branch.

## Historical checks — 24 October 2026

| Command / check | Observed result |
|---|---|
| `.venv/Scripts/python.exe -m pytest app/backend/tests -q` | **48 passed**. One dependency deprecation warning: Starlette TestClient's httpx integration; no failing test |
| `npm run typecheck` | Passed, no TypeScript errors |
| `npm run lint` | Passed, zero ESLint warnings/errors |
| `npm run build` | Passed. Vite production assets generated. Non-fatal warning: main JS chunk exceeds 500 kB; retained for this local MVP |
| `npm run test:e2e` | **4 passed**, final run against a freshly restarted backend. Full real-data journey, failure cases, config swaps, review/export, guided tour, mobile and source protection |
| `.venv/Scripts/python.exe scripts/audit_data.py` | **172/172 original hashes match**, two source-specific normalized caches generated, source files untouched |
| `.venv/Scripts/python.exe scripts/check_artifacts.py` | Passed bounded sensitive-marker/credential-pattern scan. Dist contains only application assets; no confidential input copies |
| Built frontend `GET /` | HTTP 200, text/html; actual browser rendered the real anchor value |
| `GET /api/health` | HTTP 200; offline-local-demo; live_feed=false; forecast_available=false |
| `npm run dev` | Both local listeners started: Vite 127.0.0.1:5173 and FastAPI 127.0.0.1:8000. Browser rendered Crisis Monitor, 9.922 m3/s, zero page errors; proxy health check passed |
| Development shutdown and production restart | Stopped the task-owned development session; single backend started successfully on 127.0.0.1:8000 serving the production build |
| Export readback | JSON: simulated mode, nested historical observation, scenario_applied=true, five source-ledger records, official_authorization=false, OPERATOR_ACKNOWLEDGEMENT, UNMAPPED deadline |

The managed sandbox required allowed helper-process execution for npm installation, build and browser launch. The first pytest run failed because Windows denied access to private pytest temp directories; inherited-ACL workspace temporary fixtures fixed the environment issue. The first mobile test exposed missing accessible navigation names; that was corrected and the full browser suite passed afterward. The initial artifact scan matched React DOM's `password: !0` type property; source inspection confirmed a library constant and the scan was refined to value-bearing patterns, without reading or printing confidential credentials.

## Definition of done — plan section 10

| Requirement | Authoritative evidence / result |
|---|---|
| 1. Local runnable app, real offline data | Production HTTP/browser checks and development launcher check passed. E2E intercepts and blocks all non-local requests |
| 2. Correct variable, units, identity, dates, gaps and provenance | `test_real_ingestion`, `test_missing_day_not_interpolated`, exact-row UI provenance check; DATA_AUDIT.md. 146 observations and 27 gaps independently for each station |
| 3. Historical → synthetic escalation across shared views | E2E historical evidence journey; 9.922 → 25.922 m3/s, WARNING → DANGER; all views share one evaluated context |
| 4. At least three linked institutional/source entries | Four consulted source records in default package, four review cards and three potential institutional roles. Source drawer and original URL tested. All event applications remain unreviewed |
| 5. No severity-to-power / invented deadlines | Backend tests across every band; even reported declaration and positive facts yield no authorized action. Unsourced/unreviewed or temporally unsupported deadlines withheld |
| 6. Coverage axes and statuses | Four bands × five fields, all five required legend states supported. Missing mapping explicitly refers to the package. No VERIFIED mapping fabricated |
| 7. Actual JSON pack swap and uncertainty | Default DANGER vs alternate WARNING at same value; copied JSON content edit changes evaluation/version/fingerprint; legal package reduces procedure cards from four to zero. Missing/stale/offline inputs return UNKNOWN and no trajectory |
| 8. Controls, 90-second tour and draft | Four E2E tests cover page navigation, station/date, sliders, failure toggles, facts, sources, matrix, selectors, guide completion, note/acknowledgement, Markdown/JSON downloads and preview. Changed context disables export |
| 9. Required documentation | DATA_AUDIT, LEGAL_EVIDENCE, DIFFERENTIATION, DEMO_SCRIPT, PITCH_OUTLINE, PROGRESS and LEGAL_REVIEW_CHECKLIST present, plus RUN_LOCAL and this report |
| 10. Original/confidential inputs preserved, no deployment/push | Registry integrity verified; data/PDF/mockup excluded from Git and static root; confidential/research-path HTTP requests return 404; no remote configured, no commit/push/deploy performed |

## Plan section 8 test contract

| Invariant | Coverage |
|---|---|
| Threshold equality, ordering and units | Parametrized exact boundary/invalid-order tests; unit mismatch -> UNKNOWN |
| Missing, null, negative, duplicate, stale and offline | Backend tests and browser failure injection; no safe replacement |
| Historical is not live; discharge is not water level | Canonical loader assertions, HTTP health flags and UI/source labels |
| No cross-year or cross-station joins | Independent whitelist registries, 2025-only ingestion assertions and no raster join code |
| Synthetic values distinct; whole-day crossing only | Separate returned series/mode, dashed SVG stroke assertion, Day +2 UI check; forecast flag false |
| Legal conditions/citations/review/version | Unit tests for unknown/unmet facts, no severity trigger, missing citation, absent effective version and future-only source version |
| No fabricated statutory countdown | Unreviewed statutory value withheld; UI and matrix display no verified deadline |
| Matrix is package coverage | Backend explanation assertions and clicked-cell E2E |
| Config actually changes behavior | API tests, actual temporary JSON edit test and both UI selectors |
| Acknowledgement is not authorization | SQLite values and exported JSON readback; context-bound export tests |
| Draft contains sources and mode warnings | Backend export tests, browser downloaded Markdown/JSON and preview checks; historical-only export explicitly says no synthetic trajectory applied |
| API validation | Numeric bounds, strict values, date, station/pack IDs, extra fields, facts and context checks |
| Offline | No external adapter/network calls in evaluation; non-local browser requests blocked throughout E2E |
| UI + links | Four full browser tests, source link URL assertions and desktop/mobile visual inspection |
| Secret/source protection | Build artifact scan and raw/research-path HTTP 404 checks; source originals never bundled |
| Build/tests/startup | Actual command and HTTP/browser results above |

## Visual review

Inspected generated overview, scenario and mobile screenshots. Laptop rendering was also checked at 1366×768. Charts, labels, source/uncertainty badges and controls are visible; mobile document width does not exceed the 390px viewport. Navigation and dialogs have accessible labels, keyboard focus handling and Escape close behavior. Screenshots are local, ignored evidence in test-results/, not public deliverables.

## Honest exclusions and unresolved evidence

- Iskar is usable; the conditional Arda fallback was not activated. No reservoir operations or gate-control interface is claimed.
- No external NIMH feed, IoT connection, automatic notifications, actuation, authenticated institutional identity, official legal approval, calibrated forecast, confidence probability or inundation routing is implemented. These are optional/roadmap capabilities, not hidden mocks.
- Station identity is from local documentation/filename; original gauge ID, coordinates, sampling timezone, aggregation, municipal crosswalk and redistribution license remain unresolved.
- No current domain-expert legal mapping is verified. The government-hosted English statute ends its listed amendments in 2011; current Bulgarian text, exact provisions and effective versions must be checked before any operational use.
- ISURN detailed retrieval returned 502; Parliament record was unreadable. No feature-absence or enactment claim is derived.
- The source links need network to open originals, while the packaged source metadata, application and demonstration work offline.
- GitHub issue/Project updates are unavailable because this repository has no remote. No board was created or modified.

## Highest-value next improvement

Have Aliaksei and one municipal coordinator verify the territorial crosswalk and one current municipal procedure against consolidated Bulgarian law. Validate that the resulting briefing improves their actual workflow before adding live feeds or more models.

## Subsequent authorized Cloudflare deployment — 24 October 2026

The earlier acceptance table records the original local/offline milestone before hosting was requested. The user then authorized cloud publication. Current hosting evidence supersedes the earlier no-deployment status; the source/legal limitations still apply.

| Check | Actual result |
| --- | --- |
| Backend | 51 passed, including D1 adapter persistence, owner isolation, context-bound export and 172 original hashes |
| Gateway security | 3 passed; signed/forged/expired JWT, audience/email, missing configuration, CSRF, body bounds, internal Host, blocked research paths |
| Frontend/gateway | Frontend lint, typecheck, production build and gateway typecheck passed |
| Live cloud data | Both private backend cases available with 146 rows; remote provenance hashes match the local original CSVs |
| Cloud browser workflow | 4 passed against deployed Python Worker and remote D1 through an authenticated localhost-only Wrangler harness |
| D1 write/read | Two tagged automated reviews observed in remote D1; summed legal_authorization = 0; test records subsequently removed |
| Public protection | Actual GET requests to `/`, `/api/cases`, and a built JS asset return 503 with login-setup-pending message and no app content |
| Backend exposure | `workers_dev: false`, `preview_urls: false`; backend is accessed only through service binding |
| Public Access login | **Pending/unverified**: Cloudflare rejects existing OAuth permissions (OTP create 403/1010, organization read 403/10000) |

The live-cloud acceptance run covered real history, synthetic escalation, package changes, gaps/failure injection, sources, review, draft/JSON export and mobile layout. It does not establish that an end user can receive OTP or sign in: that requires completing Access and testing the public path. No authentication bypass is present in the production gateway. The local test proxy must not be deployed.

An initial local screenshot capture failed transiently and passed on targeted rerun; all four tests subsequently passed in the cloud-backed run. Runtime tests also found and fixed internal Host forwarding and ephemeral-source initialization after Python snapshot restoration. Production dependency audit reported zero vulnerabilities; remaining npm audit findings concern Wrangler's development-only Miniflare/Undici chain. No forced downgrade was applied.

Resources, exact versions, login steps, commands and rollback: [CLOUDFLARE_SHARING](CLOUDFLARE_SHARING.md), [deployment metadata](../cloud/deployment.json). Cloud hosting runs independently of the PC. Original PDFs/research tree are excluded; two required CSVs are private backend inputs and their normalized measurements become visible only to authorized reviewers once login is configured. No Git push, Spunto change, paid-plan upgrade or domain purchase performed.

### Access activation follow-up

The user subsequently activated Access. Team domain and application audience are configured; both Workers were redeployed with `francescogabrielg@gmail.com` and `517357835k@gmail.com` as the exact app allowlist. Gateway typecheck and 3 security tests passed again. Unauthenticated `/`, `/api/cases`, `/api/session` and the deployed JS asset all returned **302 to steep-unit-4806.cloudflareaccess.com**; the login page itself returned 200 with the sign-in form. This supersedes the earlier 503/login-configuration-pending state.

No end-user PIN or authenticated session was used by the agent. OTP delivery and the complete public authenticated workflow remain pending user confirmation; the previous cloud-backed browser test evidence still validates backend/D1 behavior independently of that final login step.

### User login confirmation and multilingual UI

The user subsequently confirmed the deployed Access login works. This is user-confirmed acceptance, not an agent-controlled OTP session. The colleague's individual login has not been independently confirmed.

Added English/Italian/Russian/Bulgarian interface selection. Typecheck, lint and production build passed; **6 browser tests passed**, including the four original full-workflow tests and two language tests. The new checks exercise translated headings, all four selectable autonyms, localized numeric presentation, saved preference, unchanged scenario/review/evaluation count, original evidence text/links and mobile visibility/overflow. An initial mobile visibility failure was fixed with a sticky header and all six checks passed afterward. No datasets, rule/legal packages, review fingerprints or access policy were changed for localization. See [LANGUAGES](LANGUAGES.md).
