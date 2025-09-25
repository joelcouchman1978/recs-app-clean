# Contributing
Flow: branch → PR → CI → merge (squash). Required check: CI / test-and-health.
Local API: cd apps/api && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && uvicorn apps.api.app.main:app --reload
Health: curl -fsS http://127.0.0.1:8000/readyz
