# AgentDesk – Autonomous Research Agent

AgentDesk is a FastAPI-based autonomous research assistant that takes a research goal, searches DuckDuckGo, feeds the top results to Google Gemini, and returns a concise report with a step-by-step log.

## Features
- POST `/research` – accepts `{ "goal": "string" }` and returns report + log
- GET `/health` – health check
- Static front-end at `/` with dark UI
- Dockerized with multi-stage build, non-root user
- Docker Compose for local dev with live reload

## Project Structure
```
ProStackhub_AgentDesk/
├── main.py
├── agent.py
├── utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── run.sh
├── health_check.sh
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Setup

### Local
```bash
cd ~/Documents/ProStackhub_AgentDesk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
./run.sh
```

### Docker
```bash
docker compose up --build
```

Health check:
```bash
./health_check.sh
```

## API
**POST /research**
```json
{
  "goal": "what is HTML?"
}
```
Response:
```json
{
  "goal": "what is HTML?",
  "report": "...",
  "log": [
    {"step": "search", "detail": "..."},
    {"step": "gemini", "detail": "..."}
  ]
}
```

## Difficulties Encountered

1. **DuckDuckGo redirect 302**
   - Initial requests to `https://duckduckgo.com/html/` returned 302 to `html.duckduckgo.com`.
   - Fix: Added realistic `User-Agent` header and explicit `follow_redirects=True` with httpx.

2. **Google GenAI SDK import differences**
   - Early attempts used `google.generativeai` which is deprecated for new projects.
   - Switched to `google-genai` SDK and `client.models.generate_content`.

3. **FastAPI static file serving**
   - Needed to mount `StaticFiles` and add a root `FileResponse` to serve `index.html`.
   - Initial import path issues with `from .agent import run_research` in a non-package layout.

4. **Docker non-root user**
   - Ensured pip installs go to user directory in builder stage and copied to runtime.
   - Set `USER bruce` to avoid running as root.

5. **Environment loading**
   - `.env` must be loaded before importing modules that need `GEMINI_API_KEY`.
   - Used `python-dotenv` with explicit path.

6. **Front-end CORS / API errors**
   - Initially tested from wrong directory, hitting a different service on port 8000.
   - Restarted Uvicorn after code changes to pick up new `utils.py`.

## Tech Stack
- FastAPI, Uvicorn
- Google Gemini `gemini-2.5-flash`
- DuckDuckGo HTML search + BeautifulSoup
- Docker, Docker Compose
- Vanilla HTML/CSS/JS

## License
MIT
