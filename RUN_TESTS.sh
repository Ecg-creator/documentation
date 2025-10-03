#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements.tests.txt
# The server must be running in another terminal at http://localhost:8080
pytest -q
