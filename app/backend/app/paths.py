import os
from pathlib import Path

ROOT = Path(os.environ.get("C2A_DATA_ROOT", Path(__file__).resolve().parents[3]))
CONFIG = ROOT / "app" / "config"
RUNTIME = ROOT / "runtime"
