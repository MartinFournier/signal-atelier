#!/usr/bin/env python3
"""Build a deterministic Modrinth pack from tracked source files."""

from __future__ import annotations

import argparse
import os
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
DEFAULT_OUTPUT = ROOT / "dist/signal-atelier-0.3.0.mrpack"
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def pack_files(root: Path) -> list[tuple[Path, str]]:
    manifest = root / "modrinth.index.json"
    overrides = root / "overrides"
    if not manifest.is_file() or manifest.is_symlink():
        raise ValueError("modrinth.index.json must be a regular file")
    if not overrides.is_dir() or overrides.is_symlink():
        raise ValueError("overrides must be a regular directory")

    paths = list(overrides.rglob("*"))
    unsafe = [path for path in paths if path.is_symlink()]
    if unsafe:
        relative = unsafe[0].relative_to(root)
        raise ValueError(f"refusing to package symbolic link: {relative}")
    special = [path for path in paths if not path.is_file() and not path.is_dir()]
    if special:
        relative = special[0].relative_to(root)
        raise ValueError(f"refusing to package special file: {relative}")

    files = [(manifest, "modrinth.index.json")]
    files.extend(
        (path, path.relative_to(root).as_posix())
        for path in paths
        if path.is_file()
    )
    return [files[0], *sorted(files[1:], key=lambda item: item[1])]


def build(root: Path, output: Path) -> None:
    files = pack_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for source, archive_name in files:
                info = zipfile.ZipInfo(archive_name, ARCHIVE_TIMESTAMP)
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, source.read_bytes())
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        build(ROOT, args.output.resolve())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
