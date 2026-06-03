#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".env" ]; then
    python3 -m venv .env
fi

source .env/bin/activate
python -m pip install -U pip

pre-commit install
pre-commit install --hook-type pre-push  # optional
pre-commit autoupdate || true
pre-commit run --all-files

echo "✅ pre-commit installed."