#!/usr/bin/env bash
set -e

echo "=== 1. Creating pristine virtual environment ==="
python3 -m venv .venv_pristine
source .venv_pristine/bin/activate

echo "=== 2. Installing package and test dependencies ==="
pip install --upgrade pip
pip install . pytest pytest-asyncio

echo "=== 3. Running expanded test suite (Core + Middleware + Compliance) ==="
pytest tests/ -v

echo "=== 4. Running nominal rogue agent demo ==="
python rogue_demo.py

echo "=== 5. Running independent verification & tampering test ==="
set +e
python rogue_demo.py --verify
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -ne 0 ]; then
    echo "SUCCESS: Tamper detection correctly forced a non-zero exit code ($EXIT_CODE)."
    deactivate
    rm -rf .venv_pristine
    exit 0
else
    echo "ERROR: Tamper verification failed to exit non-zero!"
    deactivate
    rm -rf .venv_pristine
    exit 1
fi
