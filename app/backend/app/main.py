import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse

from .briefing import make_briefing
from .cloud_store import D1ReviewStore
from .ingest import STATIONS, load_case, write_normalized_cache
from .legal import coverage, load_legalpacks
from .models import BriefingRequest, ReviewRequest, ScenarioRequest
from .paths import ROOT
from .review import acknowledge, list_reviews
from .rules import load_rulepacks
from .scenario import evaluate

app = FastAPI(title="Crisis2Action local demonstration", version="0.1.0", docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")


@app.middleware("http")
async def local_only(request: Request, call_next):
    env = request.scope.get("env")
    cloud = env is not None and getattr(env, "DEPLOYMENT_MODE", "") == "private-cloud-backend"
    host = request.url.hostname
    allowed_hosts = {"127.0.0.1", "localhost", "testserver", "::1"}
    allowed_origins = {"http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:5173", "http://localhost:5173"}
    if cloud:
        # Public access to this Worker is disabled. Only the authenticated gateway
        # invokes its private service binding and replaces these identity headers.
        allowed_hosts = {"crisis2action-api.internal"}
        allowed_origins = {str(env.PUBLIC_ORIGIN)}
        email = request.headers.get("x-c2a-user-email", "").lower()
        if not email or email not in str(env.ALLOWED_EMAILS).lower().split(","):
            return JSONResponse({"detail": "Authenticated gateway required"}, status_code=403)
        request.state.review_store = D1ReviewStore(env.DB, email)
    if host not in allowed_hosts:
        return JSONResponse({"detail": "Local demonstration only"}, status_code=403)
    origin = request.headers.get("origin")
    if request.method not in ("GET", "HEAD", "OPTIONS") and origin and origin not in allowed_origins:
        return JSONResponse({"detail": "Cross-origin writes are disabled"}, status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'"
    return response


def safe_evaluate(request: ScenarioRequest):
    try:
        return evaluate(request)
    except KeyError as exc:
        raise HTTPException(404, "Unknown case or package ID") from exc
    except (OSError, ValueError) as exc:
        logging.getLogger(__name__).warning("Local case/config could not be evaluated: %s", type(exc).__name__)
        raise HTTPException(422, "Local data/config is unavailable or malformed. No replacement observation was invented; check local audit diagnostics.") from exc


@app.get("/api/health")
async def health(request: Request):
    return {"status": "ok", "mode": "private-cloud-historical-demo" if request.scope.get("env") else "offline-local-demo", "live_feed": False, "forecast_available": False}


@app.get("/api/cases")
async def cases():
    result = []
    for case_id in STATIONS:
        try:
            case = load_case(case_id)
            result.append({"station": case["station"], "summary": case["summary"], "source": case["source"], "available": True})
        except (OSError, ValueError):
            result.append({"station": STATIONS[case_id], "available": False, "error": "Local source unavailable or malformed"})
    return result


@app.get("/api/cases/{case_id}/observations")
async def observations(case_id: str, request: Request):
    try:
        result = load_case(case_id)
        if not request.scope.get("env"):
            write_normalized_cache(result)
        return result
    except KeyError as exc:
        raise HTTPException(404, "Unknown case ID") from exc
    except (OSError, ValueError) as exc:
        raise HTTPException(422, "Source unavailable or malformed; no synthetic fallback substituted") from exc


@app.get("/api/rulepacks")
async def rulepacks():
    return [p.model_dump() for p in load_rulepacks().values()]


@app.get("/api/legalpacks")
async def legalpacks():
    return list(load_legalpacks().values())


@app.get("/api/sources")
async def sources():
    return {"local": [{"id": k, "path": f"Dataset/{v['file']}", "identity_evidence": v["identity_evidence"]} for k, v in STATIONS.items()],
            "legal": load_legalpacks()["bulgaria-flood"]["sources"]}


@app.get("/api/coverage")
async def get_coverage(legal_pack: str = "bulgaria-flood"):
    packs = load_legalpacks()
    if legal_pack not in packs:
        raise HTTPException(404, "Unknown legal package")
    return coverage(packs[legal_pack])


@app.post("/api/evaluate")
@app.post("/api/simulate")
@app.post("/api/response/evaluate")
async def simulate(request: ScenarioRequest):
    return safe_evaluate(request)


@app.post("/api/reviews")
async def review(request: ReviewRequest, http_request: Request):
    try:
        store = getattr(http_request.state, "review_store", None)
        if store is not None:
            return await store.acknowledge(request.context_id, request.item_id, request.note)
        return acknowledge(request.context_id, request.item_id, request.note)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.get("/api/reviews/{context_id}")
async def reviews(context_id: str, request: Request):
    store = getattr(request.state, "review_store", None)
    try:
        return await store.list(context_id) if store is not None else list_reviews(context_id)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.post("/api/briefings")
async def briefing(request: BriefingRequest, http_request: Request):
    result = safe_evaluate(request.scenario)
    try:
        store = getattr(http_request.state, "review_store", None)
        records = await store.list(result["context_id"]) if store is not None else None
        return make_briefing(result, request.review_ids, review_records=records)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


# Only the explicit built frontend directory is served. Research inputs are never a static root.
DIST = ROOT / "app" / "frontend" / "dist"


@app.get("/{path:path}")
async def frontend(path: str):
    if path.startswith(("api/", "Dataset/", ".", "runtime/")) or ".." in path or "\\" in path:
        raise HTTPException(404, "Not found")
    target = (DIST / path).resolve()
    if DIST.resolve() not in target.parents and target != DIST.resolve():
        raise HTTPException(404, "Not found")
    if path and target.is_file():
        return FileResponse(target)
    if Path(path).suffix:
        raise HTTPException(404, "Not found")
    if (DIST / "index.html").is_file():
        return FileResponse(DIST / "index.html")
    return JSONResponse({"detail": "Frontend not built. Run npm run build, or npm run dev for development."}, status_code=503)
