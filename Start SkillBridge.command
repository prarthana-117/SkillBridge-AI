#!/bin/bash
# Double-click to run SkillBridge AI on macOS (first run installs the Claude SDK).
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
  echo "First run: setting up Python environment..."
  python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
fi
[ -f .env ] || cp .env.example .env
( sleep 2; open "http://localhost:${PORT:-8010}" ) &
exec .venv/bin/python server.py
