import os, sys
os.environ["DATABASE_URL"] = "sqlite://"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from main import app  # noqa: E402


def test_health():
    r = app.test_client().get("/health")
    assert r.status_code == 200 and r.json["status"] == "ok"


def test_yaml_safe():
    r = app.test_client().post("/config/parse", data="a: 1\nb: [1, 2]")
    assert r.json == {"a": 1, "b": [1, 2]}
