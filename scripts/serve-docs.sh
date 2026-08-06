#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$project_root"

docs_address=${SIGNAL_ATELIER_DOCS_ADDR:-0.0.0.0:8000}
exec uv run \
  --with-requirements requirements-docs.txt \
  mkdocs serve \
  --dev-addr "$docs_address" \
  "$@"
