import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables (including GEMINI_API_KEY)
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

app = FastAPI(
    title="AgentDesk",
    version="1.0.0",
    description="A research‑assistant that can browse, scrape, and summarize across several sources, then output a structured report.",
)

class ResearchRequest(BaseModel):
    goal: str

# Import the orchestration function (after FastAPI init)
from agent import run_research

@app.post("/research")
async def research_endpoint(req: ResearchRequest):
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Goal must not be empty")
    try:
        result = run_research(req.goal)
        return {"goal": req.goal, "report": result["report"], "log": result["log"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AgentDesk"}
