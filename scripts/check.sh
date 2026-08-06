#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$project_root"

jq empty modrinth.index.json
jq empty overrides/config/dynamic_fps.json
jq empty overrides/config/taxfreelevels.json
jq empty overrides/config/universaldatapack/pack.mcmeta
jq empty overrides/config/simplemenu.json5

python3 -c 'import pathlib,tomllib; [tomllib.loads(p.read_text()) for p in pathlib.Path("overrides").rglob("*.toml")]'

expected_locks=(
  chunkloaders/recipe/basic_chunk_loader.json
  chunkloaders/recipe/advanced_chunk_loader.json
  chunkloaders/recipe/ultimate_chunk_loader.json
  resource_backpacks/recipe/backpack_gold.json
  resource_backpacks/recipe/backpack_diamond.json
  resource_backpacks/recipe/backpack_netherite.json
  resource_backpacks/recipe/backpack_end.json
  refinedstorage/recipe/constructor.json
  refinedstorage/recipe/destructor.json
  refinedstorage/recipe/network_receiver.json
  refinedstorage/recipe/network_transmitter.json
  refinedstorage/recipe/wireless_autocrafting_monitor.json
  refinedstorage/recipe/wireless_grid.json
  refinedstorage/recipe/wireless_transmitter.json
)

data_root=overrides/config/universaldatapack/data
for lock in "${expected_locks[@]}"; do
  test "$(jq -c . "$data_root/$lock")" = '{}'
done

bash -n scripts/build.sh scripts/check.sh
python3 -c 'import ast,pathlib; [ast.parse(path.read_text()) for path in pathlib.Path("scripts").glob("*.py")]'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
scripts/build.sh >/dev/null
unzip -t dist/signal-atelier-0.3.0.mrpack >/dev/null
python3 -c 'import pathlib,struct; expected={"overrides/config/simplemenu/logo/logo.png":(1024,256),"overrides/config/simplemenu/icon/icon_32x32.png":(32,32),"overrides/config/simplemenu/icon/icon_16x16.png":(16,16)}; assert all(struct.unpack(">II",pathlib.Path(p).read_bytes()[16:24]) == size for p,size in expected.items())'
git diff --check
