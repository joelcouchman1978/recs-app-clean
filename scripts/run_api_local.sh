#!/usr/bin/env bash
set -euo pipefail
if [ -f .venv/bin/activate ]; then . .venv/bin/activate; fi
export USE_SQLITE="${USE_SQLITE:-1}"
export DISABLE_REDIS="${DISABLE_REDIS:-1}"
export PYTHONPATH="${PYTHONPATH:-$(pwd)}"
exec python -m uvicorn apps.api.app.main:app --host 0.0.0.0 --port 8000
