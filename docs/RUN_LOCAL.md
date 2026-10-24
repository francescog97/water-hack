# Run Crisis2Action locally

## Windows PowerShell — first setup

Requires Node.js 22.12+ (tested with 24.14.1), Python 3.11+ (tested with 3.13.5), npm and optionally uv. Run commands from the repository root.

```powershell
uv venv .venv
uv --cache-dir .cache/uv pip install --python .venv/Scripts/python.exe -r app/backend/requirements.lock
npm ci --cache .cache/npm
npm run build
.venv/Scripts/python.exe -m uvicorn app.backend.app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**. A single backend process serves the built frontend and API. After dependencies are installed, the working demonstration requires no network.

If uv is unavailable:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r app/backend/requirements.lock
```

The uv-created environment does not itself contain pip; use uv for that environment.

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

Rule JSON is in `app/config/rulepacks/`; legal/source JSON is in `app/config/legalpacks/`. They are reread by the API, not compiled into UI logic. Restart after adding a new pack so the selector registry refreshes, or refresh the page. Content edits to existing packs take effect on the next evaluation. Review fingerprints include data and package contents, so changes invalidate earlier acknowledgements.

## Troubleshooting

- Source unavailable: restore the original local file through an authorized local copy. No fake fallback measurement is supplied.
- UNKNOWN on 10 October 2025: expected, this is a real missing date.
- UNKNOWN with failure injection: disable the stale/offline toggle.
- Download disabled: enter a note of at least 10 characters and acknowledge the exact current context.
- Blank production page: run `npm run build`, then refresh.
- API schema details: `GET /api/openapi.json`; development documentation is at `/api/docs` (Swagger assets may need network).
- No verified deadline / procedure: expected knowledge-package limitation. Add a reviewed record rather than guessing.
- Port conflict: stop your previous local process. Never kill an unrelated process automatically.

No authentication is implemented for this single-user local prototype. Do not expose its ports to a network or treat operator acknowledgements as identity-verified signatures.
