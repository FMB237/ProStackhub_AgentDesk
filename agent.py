import os
from typing import List, Dict, Any

# Import the new Google GenAI SDK. If unavailable, fall back to a dummy client.
try:
    from google import genai
    _SDK_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SDK_AVAILABLE = False
    class _DummyModel:
        def generate_content(self, prompt: str):
            class _Resp:
                text = f"[Dummy Gemini response for prompt: {prompt[:60]}...]"
            return _Resp()
    class _DummyClient:
        def __init__(self, api_key=None):
            pass
        @property
        def models(self):
            class _Models:
                @staticmethod
                def generate_content(model, contents):
                    class _Resp:
                        text = f"[Dummy Gemini response for model {model}]"
                    return _Resp()
            return _Models()
    genai = None

from dotenv import load_dotenv
from pathlib import Path
from utils import search_duckduckgo

# Load API key
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "dummy"

if _SDK_AVAILABLE:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = _DummyClient(api_key=GEMINI_API_KEY)

def _format_search_results(results: List[Dict[str, str]]) -> str:
    """Create a bullet list from DuckDuckGo results for the LLM prompt."""
    return "\n".join(
        f"{i}. {r.get('title','').strip()}: {r.get('snippet','').strip()}"
        for i, r in enumerate(results, start=1)
    )

def run_research(goal: str) -> Dict[str, Any]:
    """Search DuckDuckGo, feed results to Gemini, and return a report with a log."""
    log: List[Dict[str, str]] = []
    log.append({"step": "search", "detail": f"Searching DuckDuckGo for: {goal}"})
    results = search_duckduckgo(goal, max_results=5)
    log.append({"step": "search", "detail": f"Found {len(results)} results"})

    prompt = (
        f"You are an autonomous research assistant. Answer the goal using the provided web snippets.\n\n"
        f"Goal: {goal}\n\n"
        f"Web snippets:\n{_format_search_results(results)}\n\n"
        "Provide a concise report (max 300 words)."
    )

    log.append({"step": "gemini", "detail": "Calling Gemini"})
    if _SDK_AVAILABLE:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        report = response.text.strip()
    else:
        # Dummy fallback
        report = f"[Dummy Gemini response for prompt: {prompt[:60]}...]"
    log.append({"step": "gemini", "detail": "Gemini returned a report"})
    return {"report": report, "log": log}
