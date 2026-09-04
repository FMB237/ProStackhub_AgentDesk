import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add project root to Python path for absolute imports
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

@patch("main.run_research")
def test_research_stub(mock_run_research):
    # Mock the research function to return stub data
    mock_run_research.return_value = {
        "report": "Stub report for: test",
        "log": [{"step": "test", "detail": "Stub log entry"}]
    }
    
    resp = client.post("/research", json={"goal": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert "report" in data
    assert "log" in data
    assert data["goal"] == "test"
    assert data["report"] == "Stub report for: test"
    
    # Verify the mock was called with the correct goal
    mock_run_research.assert_called_once_with("test")