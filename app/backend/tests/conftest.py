import sys
from pathlib import Path
import pytest
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))


@pytest.fixture
def tmp_path():
    # Windows managed sandbox cannot re-open pytest's chmod(0700) directories.
    # Use ordinary inherited workspace ACLs; files remain under ignored .cache.
    target = Path(__file__).resolve().parents[3] / ".cache" / "tests" / uuid4().hex
    target.mkdir(parents=True)
    return target


@pytest.fixture(autouse=True)
def isolated_reviews(tmp_path, monkeypatch):
    from app.backend.app import review
    monkeypatch.setattr(review, "RUNTIME", tmp_path)
