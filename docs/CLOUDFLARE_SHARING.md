# Crisis2Action: hosting Cloudflare e login privato

Aggiornato il **24 ottobre 2026**. **Access attivo: il proprietario ha confermato il login. L'interfaccia include inglese, italiano, russo e bulgaro. L'accesso individuale del collega non è ancora confermato.** Hosting indipendente dal PC, autorizzato dall'utente.

## Risorse effettive

### Branch di allineamento del 25 ottobre 2026

La nuova versione si trova in `feat/water-crisis-navigator-alignment`. Introduce il navigatore inquinamento come percorso principale e il pitch `/presentation.html`, conservando l'alluvione in `/?module=flood`. **Questa revisione è verificata localmente e non è ancora distribuita:** `cloud/deployment.json` descrive la precedente release pubblica. Il branch non modifica le policy Access o gli indirizzi ammessi.

Per distribuirla dopo revisione, eseguire i controlli di [VALIDATION](VALIDATION.md), compilare il frontend, preparare il bundle e applicare la migrazione additiva `0002_incidents.sql` prima del nuovo backend:

```powershell
npm run build
npm run cloud:prepare
npm run cloud:migrate
npm run cloud:deploy:backend
npm run cloud:deploy:gateway
```

La migrazione crea i fascicoli incidenti separati per proprietario e non elimina i dati di revisione esistenti. Ripetere poi le prove backend/D1, percorso completo, isolamento fra utenti e redirect pubblico Access; aggiornare le versioni in `cloud/deployment.json` soltanto con risultati effettivi. I test locali di questa revisione non dimostrano il funzionamento del nuovo schema nel cloud. Per un rollback dell'app conservare la tabella additiva; non eliminare fascicoli o applicare downgrade distruttivi.

| Risorsa | Valore verificato |
| --- | --- |
| Account | `b58b919c2f318c56b4634925d3f84ca9` |
| URL | **https://crisis2action.spunto-speak.workers.dev** |
| Gateway | Worker `crisis2action`: frontend compilato e controllo JWT/email |
| Backend | Worker Python/FastAPI `crisis2action-api`, solo service binding `BACKEND` |
| Persistenza | D1 `crisis2action-db`, ID `c431c02e-a352-44f0-b936-4e353baf0aeb` |
| Schema applicato | `cloud/backend/migrations/0001_reviews.sql` |
| Indirizzi ammessi | `francescogabrielg@gmail.com` e `517357835k@gmail.com` |
| Team domain | `steep-unit-4806.cloudflareaccess.com` |
| Application Audience (AUD) | `c7b69a28d434b9df90a38033af6b6cafaf1a210ac4fb634a0ab6161f484ace42` |
| Route alternative | Preview disabilitate su entrambi; backend senza hostname pubblico |
| Domini personalizzati | Nessuno nell'inventario; `spunto-speak.workers.dev` è il sottodominio assegnato |
| Costi | Nessun upgrade a pagamento eseguito; fatturazione non leggibile con la sessione corrente |

Flusso: **browser → Access (codice email) → gateway con verifica JWT → backend privato → D1**. Frontend e backend sono su Cloudflare: il PC può essere spento. Non si usa un Tunnel locale. Spunto, il suo database e gli altri progetti non sono stati modificati. Versioni/stato: [deployment.json](../cloud/deployment.json).

## Access attivato: come entrare

L'utente ha attivato la protezione Access del Worker e riferito di aver autorizzato entrambi gli indirizzi. Il gateway e il backend hanno la stessa allowlist: `francescogabrielg@gmail.com` e `517357835k@gmail.com`.

1. Aprire **https://crisis2action.spunto-speak.workers.dev** in una finestra privata.
2. Nella pagina Cloudflare Access scegliere **One-time PIN** se compare una scelta di metodi, inserire la propria email autorizzata e richiedere il codice.
3. Inserire il codice ricevuto via email. Dopo il login verificare l'app e `/api/session`; completare la demo e provare separatamente il secondo utente.

La risposta pubblica osservata è ora **302 verso `https://steep-unit-4806.cloudflareaccess.com`**, che mostra la pagina **Sign in ・ Cloudflare Access** con modulo email/PIN. Non autenticati non ricevono HTML, asset o dati dell'app. **Il proprietario ha confermato che il login funziona**. L'agente non ha usato PIN o cookie personali; manca la conferma individuale del collega.

Il precedente messaggio `Private application: login configuration pending` indicava identificativi vuoti; ora team domain e AUD sono impostati. In caso di un vecchio messaggio aprire una nuova finestra privata; se resta, verificare versione distribuita e variabili. Per un rifiuto dopo il PIN controllare l'indirizzo esatto sia nella policy Access sia nelle due allowlist, senza allargare la policy.

L'AUD è stato recuperato dall'identificativo della pagina/redirect Access effettivamente serviti da Cloudflare. Gli identificativi sono non segreti; non registrare cookie, codici PIN, JWT o token amministrativi nei documenti.

### Ricreazione o modifica della protezione

Il dashboard corretto è **Workers & Pages → crisis2action → Access → All traffic**, con policy Allow limitata alle email nominate. In alternativa configurare un'app self-hosted sull'intero hostname. One-time PIN è l'identity provider; evitare Everyone, interi domini email e Bypass. Il team appartiene all'account `b58b919c2f318c56b4634925d3f84ca9`, piano Zero Trust Free come mostrato dall'utente.

Per riconfigurare gli identificativi reali (attualmente già salvati):

```powershell
npm run cloud:access:configure -- steep-unit-4806.cloudflareaccess.com c7b69a28d434b9df90a38033af6b6cafaf1a210ac4fb634a0ab6161f484ace42
npm run cloud:types
npm run cloud:typecheck
npm run cloud:test
npm run cloud:deploy:gateway
```

La sessione Wrangler continua a non poter amministrare Access: la creazione OTP era stata rifiutata con 403/1010 e la lettura organizzazione con 403/10000. Anche dopo l'attivazione, l'elenco app via quella sessione restituisce vuoto: **non interpretarlo come assenza di protezione**, verificare dashboard e redirect. Le policy attuali sono state configurate dall'utente, non dall'agente.

## Comandi di preparazione e aggiornamento

Dalla root `C:\Development\Repositories\eit-hackathon`, dopo i prerequisiti di [RUN_LOCAL](RUN_LOCAL.md):

```powershell
npm ci --cache .cache/npm
uv sync --directory cloud/backend --cache-dir .cache/uv
npm run build
npm run cloud:prepare
npm run test:backend
npm run cloud:types
npm run cloud:typecheck
npm run cloud:test
npm run cloud:migrate
npm run cloud:deploy:backend
npm run cloud:deploy:gateway
```

Il database esiste già: **non ricrearlo** e non usare `spunto-db`. Il comando backend rigenera il bundle prima del deployment. I config canonici sono `cloud/backend/wrangler.jsonc` e `cloud/gateway/wrangler.jsonc`; conservare gli identificativi Access validi negli aggiornamenti. Verificare la sessione con `npx wrangler whoami`, senza stampare/esportare token o copiare file OAuth. L'email del revisore non identifica necessariamente l'amministratore Cloudflare.

L'ambiente `cloud/backend` include Pywrangler, SDK e `uv >= 0.13.4`; non occorre aggiornare uv globale. Il primo avvio può scaricare Python/Pyodide. Lockfile host: `cloud/backend/uv.lock`; runtime: `cloud/backend/pylock.toml`. Per un dry run usare una directory di output assoluta sotto `.cache`, **fuori da `cloud/backend/generated`**, per non includere l'output come modulo nei build successivi.

## Dati e sicurezza

- `scripts/prepare_cloud.py` seleziona soltanto i moduli backend espliciti, i **due CSV Iskar** e quattro JSON dei pacchetti: [manifest/hash](../cloud/data-manifest.json). Nessuna copia ricorsiva di Dataset o della root. Tutti i **172 originali invariati**; documenti confidenziali esclusi.
- I sei input sono ricostruiti byte per byte nel Worker privato. I CSV non sono asset statici; dopo login i revisori potranno leggere le misure normalizzate via API. La licenza delle misure resta non documentata.
- I file effimeri di input/config sono inizializzati durante fetch, dopo il ripristino dello snapshot Python. Le revisioni persistono in **D1**, associate all'email verificata e isolate per utente/fingerprint; in locale resta SQLite.
- Il gateway controlla firma RS256, issuer, audience, scadenza ed email; sostituisce l'identità verso il backend, passa un Host interno esplicito e verifica gli Origin. HTML, asset e API passano dal gateway (`run_worker_first: true`). Nessun bypass di test è presente in produzione.
- L'identità autenticata non prova un ruolo istituzionale o un'approvazione legale. `legal_authorization` resta zero; soglie demo, dati storici, scenari simulati e interpretazioni non validate mantengono le etichette. Nessun feed live/forecast aggiunto.

## Verifiche eseguite

**51 test backend**, **3 test sicurezza gateway**, lint/typecheck/build frontend e typecheck gateway passati. **4 test browser contro backend Cloudflare e D1 remoto** passati: storico → simulazione → fonti → cambio pacchetti → revisione → export, incertezza e mobile. D1 ha confermato due revisioni di test e zero autorizzazioni legali; i record marcati di test vengono rimossi al termine.

I test cloud usano un proxy locale autenticato da Wrangler, non il login pubblico Access. **Redirect/modulo verificati dall'agente e login confermato dal proprietario; il collega resta da verificare individualmente.** Non dichiarare completata la pubblicazione privata prima di questo passaggio.

Nel primo giro locale la cattura screenshot ha avuto un errore transitorio: passato il singolo test alla ripetizione, poi tutti e quattro nel giro cloud. Audit produzione: zero vulnerabilità segnalate; restano avvisi nel tooling Wrangler/Miniflare/Undici, non nel bundle distribuito.

Per ripetere il controllo cloud:

```powershell
# Terminale 1: solo localhost, tramite binding remoto autenticato Wrangler.
npm run cloud:smoke:serve
# Terminale 2:
$env:C2A_TEST_BASE_URL = 'http://127.0.0.1:8789'
npm run test:e2e
Remove-Item Env:C2A_TEST_BASE_URL
```

`cloud/smoke` è un **test locale senza login: non distribuirlo**. Il suo proxy marca le revisioni `[AUTOMATED CLOUD TEST]`: rimuovere solo quei record dopo il controllo e arrestare il proxy. Non cancellare revisioni reali.

## Gestione accessi e rollback

Per aggiungere un altro revisore modificare sia Access sia `ALLOWED_EMAILS` nei due config, distribuire entrambi, rigenerare tipi e verificare le identità. Nessuna email di esempio è autorizzata.

Per bloccare la condivisione, rimuovere l'Allow/revocare sessioni Access mantenendo il controllo JWT. In caso di dubbio svuotare `ACCESS_AUD` e ridistribuire il gateway: torna a 503 senza dati. Non disabilitare Access lasciando aperta l'app. Per rollback applicativo usare le versioni della singola risorsa; non eliminare D1 o retrocedere schema senza valutare le revisioni esistenti. Non intervenire su Spunto.

Riferimenti: [FastAPI/Python Workers](https://developers.cloudflare.com/workers/languages/python/packages/fastapi/), [pacchetti/Pywrangler](https://developers.cloudflare.com/workers/languages/python/packages/), [Access sui Worker](https://developers.cloudflare.com/workers/configuration/cloudflare-access/), [One-time PIN](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/), [D1](https://developers.cloudflare.com/d1/examples/query-d1-from-python-workers/), [routing degli asset](https://developers.cloudflare.com/workers/static-assets/routing/worker-script/).

Non promettere gratuità illimitata: non è stato attivato alcun upgrade, ma i costi effettivi dell'account non sono stati verificati. Non attivare piani a pagamento senza autorizzazione.

## Selettore lingua

Il bordo superiore offre **English, Italiano, Русский e Български**, con preferenza locale persistente, formattazione di date/numeri e conservazione dello scenario/revisione. Fonti legali e bozze restano originali. [Dettagli e test](LANGUAGES.md). Per una modifica soltanto frontend distribuire il solo gateway dopo build e test.
