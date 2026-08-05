#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
output_dir="$project_root/dist"
output_file="$output_dir/signal-atelier-0.1.0.mrpack"

mkdir -p "$output_dir"
rm -f "$output_file"

cd "$project_root"
zip -q "$output_file" modrinth.index.json

echo "$output_file"
