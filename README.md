# Dati per il progetto Water Hack

Il repository contiene una raccolta di dati su acque, fiumi, precipitazioni, umidità del suolo e flotte pescherecce, riferita soprattutto alla Bulgaria.

Consultare il [catalogo del dataset](Dataset/README.md) per contenuti, periodi, formati, istruzioni d'uso e limiti. Ogni cartella del dataset contiene un proprio `README.md` in italiano.

I nomi dei file sono in italiano, con traslitterazione dei nomi propri. I contenuti originali sono invariati. Il [registro delle rinomine](Dataset/registro_rinomine.csv) conserva i percorsi originali, quelli attuali e gli hash SHA-256 per tracciabilità.

## Crisis2Action MVP

Local, offline-capable decision preparation and procedural traceability for a historical Bulgarian Iskar discharge scenario. Five views: Crisis Monitor, Scenario Lab, Response Navigator, Coverage Matrix, Legal Package & Evidence.

**DEMONSTRATION — NOT FOR OPERATIONAL USE.** Real historical values, synthetic what-if trajectories, demo thresholds and unreviewed legal interpretations are explicitly separated. No live feed, calibrated forecast, official crisis designation, dispatch or infrastructure control is implemented.

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

Cloud resources are deployed at **https://crisis2action.spunto-speak.workers.dev** and run independently of this PC. **Cloudflare Access is enabled and gateway identifiers are configured.** Unauthenticated requests redirect to the Cloudflare sign-in page. The app allowlist contains `francescogabrielg@gmail.com` and `517357835k@gmail.com`; users sign in with an email PIN. The owner has confirmed login works; the colleague has not yet confirmed their individual login.

Follow the [hosting and Access setup guide](docs/CLOUDFLARE_SHARING.md) before sharing the app; it includes exact resources, deployment commands, tests and the administrator step. The Python backend has no public route, reviews use a separate D1 database, and original/private research inputs are excluded from public assets. [Deployment state and versions](cloud/deployment.json). The shared agent handoff also lives at `C:\Development\Repositories\README.md`.

The header language selector offers **English, Italiano, Русский and Български**, remembers the browser preference and preserves the current scenario/review when switching. Original legal evidence and exported drafts retain their original language. [Language scope and validation](docs/LANGUAGES.md).

### Demonstrate / review

- [90-second demo](docs/DEMO_SCRIPT.md)
- [Data audit](docs/DATA_AUDIT.md)
- [Legal evidence and limitations](docs/LEGAL_EVIDENCE.md)
- [Aliaksei's review checklist](docs/LEGAL_REVIEW_CHECKLIST.md)
- [Differentiation and value hypotheses](docs/DIFFERENTIATION.md)
- [Pitch outline](docs/PITCH_OUTLINE.md)
- [Implementation progress](docs/PROGRESS.md)
- [Validation and acceptance evidence](docs/VALIDATION.md)
- [Private sharing with Cloudflare: verified account and setup options](docs/CLOUDFLARE_SHARING.md)

Use Start guided demo to select Novi Iskar, 25 September 2025: 9.922 m3/s. The +8 m3/s/day, two-day synthetic scenario reaches 25.922 m3/s (WARNING → DANGER under the demo pack). Alternate thresholds change it to WARNING. No threshold activates a legal obligation. A review note and acknowledgement are required to download the unapproved draft.

Original datasets and the confidential event PDF remain local and unchanged, excluded from Git and frontend assets. Redistribution rights for original measurements are not established. Do not publish the source inputs or expose the local development ports.
