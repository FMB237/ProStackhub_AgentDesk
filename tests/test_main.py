import os
import sys
from pathlib import Path

# Add project root to Python path so 'import main' works
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

os.environ["GEMINI_API_KEY"] = "dummy"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_research_empty_goal():
    resp = client.post("/research", json={"goal": "   "})
    assert resp.status_code == 400

def test_research_stub():
    # With dummy key, agent returns dummy report
    resp = client.post("/research", json={"goal": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert "report" in data
    assert "log" in data
    assert data["goal"] == "test"