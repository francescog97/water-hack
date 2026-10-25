# Dati per il progetto Water Hack

Il repository contiene una raccolta di dati su acque, fiumi, precipitazioni, umidità del suolo e flotte pescherecce, riferita soprattutto alla Bulgaria.

Consultare il [catalogo del dataset](Dataset/README.md) per contenuti, periodi, formati, istruzioni d'uso e limiti. Ogni cartella del dataset contiene un proprio `README.md` in italiano.

I nomi dei file sono in italiano, con traslitterazione dei nomi propri. I contenuti originali sono invariati. Il [registro delle rinomine](Dataset/registro_rinomine.csv) conserva i percorsi originali, quelli attuali e gli hash SHA-256 per tracciabilità.

## Water Crisis Decision Navigator

The default application prepares a documented response to **suspected river pollution in Bulgaria**, following Aliaksei's supplied report. Crisis2Action remains the technical and legacy name. Five views connect **Observation & evidence → Potential receptors → Institutions & legal checks → Action plan & history → Pilot & value**.

**DEMONSTRATION — NOT FOR OPERATIONAL USE.** The Iskar exercise uses invented suspended-solids samples: 8 → 96 mg/L (12×), with a configured demonstration trigger of 30 mg/L (`>=`). Reach geometry and every receptor are synthetic. No laboratory report, real pollution confirmation, contaminant identification, statutory limit or official authorization is established. The 9,657 anonymous historical TSS rows and the 2024 CDS geographic context remain separate and are not joined to the incident.

Incident records persist in local SQLite or owner-scoped cloud D1. Five required verification tasks must record named demonstration roles and evidence before an explicit self-recorded demonstration specialist review enables response work. Assignments, status changes, rejections, outcomes, revisions and draft exports retain the reasoning. Approval never verifies law or water quality; no notification is sent. Optimistic revisions prevent stale updates from silently overwriting a newer record.

The historical Iskar flood demonstration remains available at **`/?module=flood`**. Its real discharge observations and synthetic scenarios retain their original distinctions.

### Quick start — Windows PowerShell

```powershell
uv venv .venv
uv --cache-dir .cache/uv pip install --python .venv/Scripts/python.exe -r app/backend/requirements.lock
npm ci --cache .cache/npm
npm run build
.venv/Scripts/python.exe -m uvicorn app.backend.app.main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**. Development: `npm run dev` and open **http://127.0.0.1:5173**. Full setup, tests and troubleshooting: [RUN_LOCAL](docs/RUN_LOCAL.md).

### Private Cloudflare hosting

The existing cloud release is hosted at **https://crisis2action.spunto-speak.workers.dev** and runs independently of this PC. The report-aligned pollution navigator and browser pitch described here are local changes pending deployment; this URL must not be assumed to contain them yet. **Cloudflare Access is enabled and gateway identifiers are configured.** Unauthenticated requests redirect to the Cloudflare sign-in page. The app allowlist contains `francescogabrielg@gmail.com` and `517357835k@gmail.com`; users sign in with an email PIN. The owner has confirmed login works; the colleague has not yet confirmed their individual login.

Follow the [hosting and Access setup guide](docs/CLOUDFLARE_SHARING.md) before sharing the app; it includes exact resources, deployment commands, tests and the administrator step. The Python backend has no public route, reviews use a separate D1 database, and original/private research inputs are excluded from public assets. [Deployment state and versions](cloud/deployment.json). The shared agent handoff also lives at `C:\Development\Repositories\README.md`.

The header language selector offers **English, Italiano, Русский and Български**, remembers the browser preference and preserves the current scenario/review when switching. Original legal evidence and exported drafts retain their original language. [Language scope and validation](docs/LANGUAGES.md).

### Demonstrate / review

- [90-second demo](docs/DEMO_SCRIPT.md)
- [Data audit](docs/DATA_AUDIT.md)
- [Legal evidence and limitations](docs/LEGAL_EVIDENCE.md)
- [Aliaksei's review checklist](docs/LEGAL_REVIEW_CHECKLIST.md)
- [Differentiation and value hypotheses](docs/DIFFERENTIATION.md)
- [Pitch outline](docs/PITCH_OUTLINE.md)
- [Pitch orale in italiano](docs/PITCH_ITALIANO.md)
- [Implementation progress](docs/PROGRESS.md)
- [Validation and acceptance evidence](docs/VALIDATION.md)
- [Private sharing with Cloudflare: verified account and setup options](docs/CLOUDFLARE_SHARING.md)

Use **New exercise** to create a repeatable pollution case, then follow the guided scenario. Complete the five verification tasks with specific evidence notes, record an acknowledged demonstration specialist review, assign response work and export the draft/history. All roles are self-declared and all incident measurements remain invented. The [demo script](docs/DEMO_SCRIPT.md) includes the retained flood journey.

Open **`/presentation.html`** for the nine-slide Italian browser pitch; use arrow keys, speaker notes and print. Source files are `app/frontend/public/presentation.*`. Its economics and proposed customer study are hypotheses, not measured results. See [report alignment](docs/ALIAKSEI_ALIGNMENT.md) and [pollution data/legal audit](docs/POLLUTION_DATA_LEGAL_AUDIT.md). Qualified scientific, legal and jurisdiction review and actual customer interviews/pilot validation remain pending. Current check and release evidence belongs in [VALIDATION](docs/VALIDATION.md).

Original datasets and the confidential event PDF remain local and unchanged, excluded from Git and frontend assets. Redistribution rights for original measurements are not established. Do not publish the source inputs or expose the local development ports.
