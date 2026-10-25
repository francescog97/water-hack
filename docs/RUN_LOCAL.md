# Run Water Crisis Decision Navigator locally

## Windows PowerShell — first setup

Requires Node.js 22.12+ (tested with 24.14.1), Python 3.11+ (tested with 3.13.5), npm and optionally uv. Run commands from the repository root.

```powershell
uv venv .venv
uv --cache-dir .cache/uv pip install --python .venv/Scripts/python.exe -r app/backend/requirements.lock
npm ci --cache .cache/npm
npm run build
.venv/Scripts/python.exe -m uvicorn app.backend.app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** for the default pollution navigator. A single backend process serves the built frontend and API. After dependencies are installed, the working demonstration requires no network.

If uv is unavailable:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r app/backend/requirements.lock
```

The uv-created environment does not itself contain pip; use uv for that environment.

## Routes and repeatable demonstration

- `/`: pollution navigator with five views: observation/evidence, receptors, institutions/legal checks, action/history, and pilot/value. Use **New exercise** to create a fresh record for a rehearsal; earlier records remain persistent.
- `/?module=flood`: retained historical Iskar discharge and synthetic flood demonstration.
- `/presentation.html`: nine-slide Italian browser pitch; arrow-key navigation, speaker notes and print. Sources: `app/frontend/public/presentation.*`.

The pollution exercise is synthetic TSS 8 → 96 mg/L (12×), demonstration trigger 30 mg/L (`>=`), with synthetic geometry and receptors. The anonymous 9,657-row historical TSS series and 2024 CDS context are separate, without an incident join. See [DEMO_SCRIPT](DEMO_SCRIPT.md) for the five required checks, explicit demonstration review gate, response assignment and export.

Incident state persists locally in SQLite; deployed records use owner-scoped D1. Reloading resumes persisted state. **New exercise** creates another record rather than deleting earlier decisions. Mutations carry an expected revision; refresh after a conflict before retrying. A demo specialist approval does not certify law, scientific findings or institutional authority. No notification is sent.

## Development mode

```powershell
npm run dev
```

The launcher starts FastAPI on 127.0.0.1:8000 and Vite on 127.0.0.1:5173. Open **http://127.0.0.1:5173**. Stop with Ctrl+C. Stop any earlier process on these ports before running the launcher. Both listeners bind to loopback, never 0.0.0.0.

## Validation

```powershell
.venv/Scripts/python.exe scripts/audit_data.py
.venv/Scripts/python.exe -m pytest app/backend/tests -q
npm run typecheck
npm run lint
npm run build
.venv/Scripts/python.exe scripts/check_artifacts.py
npm run test:e2e
```

Browser tests use installed Microsoft Edge in headless mode. Install Edge or change `channel` in playwright.config.ts to a locally available supported Chromium browser. Test results, screenshots and a downloaded draft are under ignored `test-results/`. The E2E runner starts the local backend if needed and otherwise reuses it.

This managed Windows environment blocks Vite/browser helper subprocesses in the restricted sandbox. The build and headless tests were run with execution permission outside that process sandbox. This is a host restriction, not an application requirement. Pytest uses inherited-ACL workspace temporary directories because private 0700 temp directories are inaccessible in this managed environment.

## Data and configuration

Required private local inputs:

- `Dataset/portata_iskar_novi_iskar_2025.csv`
- `Dataset/portata_iskar_orehovitsa_2025.csv`
- `Dataset/registro_rinomine.csv` for the full integrity audit

Original inputs, the confidential event PDF, caches, logs, review database and build/test outputs are gitignored. No original data is copied into frontend public assets. Do not remove these ignores to publish a demo. The code alone cannot reproduce the private real-data demonstration without authorized local data.

The pollution scenario is `app/config/incidents/iskar-pollution-demo.json`; it records sample modes, demonstration trigger, receptors, sources and tasks. Existing incidents retain their scenario snapshot; use a new exercise to demonstrate revised scenario configuration. Legacy flood rule JSON is in `app/config/rulepacks/`; legal/source JSON is in `app/config/legalpacks/`. They are reread by the API, not compiled into UI logic. Restart after adding a new pack so the selector registry refreshes, or refresh the page. Content edits to existing packs take effect on the next evaluation. Review fingerprints include data and package contents, so changes invalidate earlier acknowledgements.

## Troubleshooting

- Source unavailable: restore the original local file through an authorized local copy. No fake fallback measurement is supplied.
- UNKNOWN on 10 October 2025: expected, this is a real missing date.
- UNKNOWN with failure injection: disable the stale/offline toggle.
- Pollution response blocked: complete the five required verification tasks with assignee/role/evidence and record an acknowledged, reasoned demonstration specialist review. Editing a required verification revokes that approval.
- Revision conflict: refresh the incident and inspect newer history before retrying.
- Legacy flood download disabled: enter a note of at least 10 characters and acknowledge the exact current context.
- Blank production page: run `npm run build`, then refresh.
- API schema details: `GET /api/openapi.json`; development documentation is at `/api/docs` (Swagger assets may need network).
- No verified deadline / procedure: expected knowledge-package limitation. Add a reviewed record rather than guessing.
- Port conflict: stop your previous local process. Never kill an unrelated process automatically.

The single-user local server is not a substitute for cloud authentication. Keep its listeners on loopback; local demonstration names and acknowledgements are not identity-verified signatures. The hosted gateway uses Cloudflare Access and owner-scoped persistence; retain the [Access instructions](CLOUDFLARE_SHARING.md). The existing protected URL is https://crisis2action.spunto-speak.workers.dev; local changes described here remain pending deployment until recorded in [VALIDATION](VALIDATION.md).
