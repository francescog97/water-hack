"""Build an explicit private Python bundle; never traverse/copy the research tree."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cloud/backend/generated"
BACKEND_MODULES = ["__init__", "briefing", "cloud_store", "incident_store", "incidents", "ingest", "legal", "main", "models", "paths", "review", "rules", "scenario"]


def prepare():
    from app.backend.app.ingest import STATIONS
    files = {}
    for filename in {s["file"] for s in STATIONS.values()}:
        path = ROOT / "Dataset" / filename
        # Keep source bytes exactly, including any BOM; provenance hashes must match.
        files[f"Dataset/{filename}"] = path.read_bytes().decode("utf-8")
    for kind in ["rulepacks", "legalpacks", "incidents"]:
        for path in sorted((ROOT / "app/config" / kind).glob("*.json")):
            files[f"app/config/{kind}/{path.name}"] = path.read_bytes().decode("utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    payload = "FILES = " + repr(files) + "\n"
    (OUTPUT / "cloud_payload.py").write_text(payload, encoding="utf-8")
    for module in BACKEND_MODULES:
        source = ROOT / f"app/backend/app/{module}.py"
        destination = OUTPUT / f"app/backend/app/{module}.py"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
    for package in ["app", "app/backend"]:
        (OUTPUT / package / "__init__.py").write_text("", encoding="utf-8")
    (OUTPUT / "entry.py").write_text('''from pathlib import Path
import os
from cloud_payload import FILES

# Ephemeral files are immutable source/config material only. Reviews use D1.
# Install during fetch: filesystem writes made while creating a Python memory
# snapshot are not guaranteed to survive into a request isolate.
root = Path("/tmp/crisis2action")
os.environ["C2A_DATA_ROOT"] = str(root)

from app.backend.app.main import app
from workers import WorkerEntrypoint, asgi

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        for relative, content in FILES.items():
            target = root / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content.encode("utf-8"))
        return await asgi.fetch(app, request, self.env, self.ctx)
''', encoding="utf-8")
    manifest = {name: hashlib.sha256(content.encode("utf-8")).hexdigest() for name, content in files.items()}
    (ROOT / "cloud/data-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Prepared {len(BACKEND_MODULES)} Python modules and {len(files)} explicit data/config inputs; no research-directory upload.")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    prepare()
