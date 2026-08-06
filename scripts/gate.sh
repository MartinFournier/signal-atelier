#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$project_root"

scripts/check.sh
scripts/check-docs.sh
actionlint
gitleaks dir --redact --no-banner .
git diff --check
