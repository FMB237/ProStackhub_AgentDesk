# Architecture Overview

## High‑level design

AgentDesk is a **FastAPI** micro‑service that exposes a single public endpoint `/research`. The endpoint accepts a natural‑language goal, performs a web search on DuckDuckGo, feeds the top snippets to **Google Gemini** (via the `google-genai` SDK), and returns a concise report together with a step‑by‑step log.

```
┌───────────────────────┐
│  Client (browser)    │
└───────┬──────────────┘
        │ HTTP
        ▼
┌───────────────────────┐
│  FastAPI app (main.py)│
│  ├─ /research         │
│  ├─ /health           │
│  └─ static files      │
└───────┬──────────────┘
        │ Python imports
        ▼
┌───────────────────────┐
│  agent.py (orchestration)│
│  ├─ search_duckduckgo   │
│  └─ run_research        │
└───────┬──────────────┘
        │ HTTPX + BeautifulSoup
        ▼
┌───────────────────────┐
│  DuckDuckGo HTML API  │
└───────┬──────────────┘
        │ Gemini SDK
        ▼
┌───────────────────────┐
│  Google Gemini (LLM)  │
└───────────────────────┘
```

## Core components

| Component | Responsibility | Key libraries |
|-----------|---------------|----------------|
| **FastAPI** | HTTP server, routing, validation | `fastapi`, `pydantic` |
| **Uvicorn** | ASGI server | `uvicorn` |
| **google-genai** | Gemini client | `google-genai` |
| **httpx** | DuckDuckGo HTTP client | `httpx` |
| **BeautifulSoup** | HTML parsing | `beautifulsoup4` |
| **dotenv** | Load `.env` | `python-dotenv` |
| **Docker** | Containerization | Dockerfile, docker‑compose |

## Design decisions

1. **Single‑service architecture** – Keeps the codebase small and easy to ship. All logic lives in `agent.py` and `utils.py`.
2. **Stateless API** – No database or session state; the service is fully stateless, which simplifies scaling and CI.
3. **Non‑root Docker user** – The image creates a `bruce` user (UID 1000) to avoid running as root.
4. **Local dev with live reload** – Docker‑Compose mounts source files so changes are reflected instantly.
5. **Graceful fallbacks** – If the Gemini SDK is missing, a dummy client is used so the service still returns a stub report.
6. **Environment isolation** – `.env` is loaded before any imports that need `GEMINI_API_KEY`.
7. **Testing strategy** – `pytest` + `fastapi.testclient` with monkey‑patching of `run_research` to avoid external calls.

## Challenges & solutions

| Challenge | Solution |
|-----------|----------|
| DuckDuckGo 302 redirects | Added realistic `User‑Agent` header and `follow_redirects=True` in `httpx.get`. |
| Gemini SDK import differences | Switched to the new `google-genai` package and wrapped it in a dummy fallback for local dev. |
| Static file serving | Mounted `/static` and added a root route that returns `index.html`. |
| CI directory layout | Removed `working-directory` override and added a debug step to confirm the checkout path. |
| Docker non‑root user | Created `bruce` user and copied pip‑installed packages from the builder stage. |

## Future improvements

* Add **OpenAI** fallback for Gemini.
* Cache DuckDuckGo results to reduce API calls.
* Expose a WebSocket endpoint for streaming Gemini responses.
* Add a simple front‑end SPA with Tailwind for better UX.

---

**Author**: Bruce – DevOps & Network Automation Engineer
**Date**: 2026‑09‑04
