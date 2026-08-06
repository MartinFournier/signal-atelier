#!/usr/bin/env python3
"""Update pinned Modrinth files while preserving compatibility policy."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


API = "https://api.modrinth.com/v2"
USER_AGENT = "MartinFournier/signal-atelier (scheduled update checker)"
DOWNLOAD_RE = re.compile(r"/data/([^/]+)/versions/([^/]+)/")
ALLOWED_CHANNELS = {
    "release": {"release"},
    "beta": {"release", "beta"},
    "alpha": {"release", "beta", "alpha"},
}


def request_json(path: str, query: dict[str, str] | None = None):
    url = f"{API}/{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def coordinates(entry: dict) -> tuple[str, str] | None:
    downloads = entry.get("downloads", [])
    if len(downloads) != 1:
        return None
    match = DOWNLOAD_RE.search(downloads[0])
    if not match:
        return None
    return match.group(1), match.group(2)


def primary_file(version: dict) -> dict | None:
    files = version.get("files", [])
    return next((file for file in files if file.get("primary")), None) or (
        files[0] if files else None
    )


def compatible_versions(project_id: str, current: dict, game_version: str) -> list[dict]:
    loaders = current.get("loaders", [])
    query = {"game_versions": json.dumps([game_version])}
    if loaders:
        query["loaders"] = json.dumps(loaders)
    versions = request_json(f"project/{project_id}/version", query)
    allowed = ALLOWED_CHANNELS[current["version_type"]]
    return [version for version in versions if version.get("version_type") in allowed]


def updated_entry(entry: dict, version: dict) -> dict:
    file = primary_file(version)
    if file is None:
        raise ValueError(f"Version {version['id']} has no downloadable file")
    path_root = "shaderpacks" if entry["path"].startswith("shaderpacks/") else "mods"
    return {
        "path": f"{path_root}/{file['filename']}",
        "hashes": file["hashes"],
        "env": entry["env"],
        "downloads": [file["url"]],
        "fileSize": file["size"],
    }


def changelog_summary(text: str | None, limit: int = 600) -> str:
    if not text:
        return "⚠️ No changelog supplied. Manual release-page review required."
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def current_versions(version_ids: list[str]) -> dict[str, dict]:
    versions = request_json("versions", {"ids": json.dumps(version_ids)})
    return {version["id"]: version for version in versions}


def dependency_key(dependency: dict) -> tuple[str, str, str]:
    target = dependency.get("project_id") or dependency.get("file_name") or "unknown"
    return target, dependency.get("version_id") or "any", dependency["dependency_type"]


def dependency_changes(current: dict, latest: dict) -> tuple[list[tuple], list[tuple]]:
    before = {dependency_key(item) for item in current.get("dependencies", [])}
    after = {dependency_key(item) for item in latest.get("dependencies", [])}
    return sorted(after - before), sorted(before - after)


def format_dependency(dependency: tuple[str, str, str]) -> str:
    target, version, kind = dependency
    return f"`{target}` (`{kind}`, version `{version}`)"


def render_report(changes: list[tuple], game_version: str) -> str:
    report = [
        "## Modrinth updates",
        "",
        f"Compatibility target: Minecraft `{game_version}` with each artifact's current loader set.",
        "",
        "| Project | Current | Proposed | Published | Channel |",
        "| --- | --- | --- | --- | --- |",
    ]
    for project, current, latest in changes:
        published = latest.get("date_published", "unknown").replace("T", " ").replace("Z", " UTC")
        report.append(
            f"| [{project['title']}](https://modrinth.com/{project['project_type']}/{project['slug']}) "
            f"| `{current['version_number']}` (`{current['id']}`) "
            f"| `{latest['version_number']}` (`{latest['id']}`) "
            f"| {published} | `{current['version_type']}` → `{latest['version_type']}` |"
        )
    report.extend(["", "## Changelogs and dependency changes", ""])
    for project, current, latest in changes:
        added, removed = dependency_changes(current, latest)
        dependency_lines = ["Dependencies: unchanged."]
        if added or removed:
            dependency_lines = []
            if added:
                dependency_lines.append(
                    "Dependencies added: " + ", ".join(map(format_dependency, added)) + "."
                )
            if removed:
                dependency_lines.append(
                    "Dependencies removed: " + ", ".join(map(format_dependency, removed)) + "."
                )
        report.extend(
            [
                f"### {project['title']}",
                "",
                f"[{current['version_number']} → {latest['version_number']}]"
                f"(https://modrinth.com/{project['project_type']}/{project['slug']}/version/{latest['id']})",
                "",
                *dependency_lines,
                "",
                changelog_summary(latest.get("changelog")),
                "",
            ]
        )
    report.extend(
        [
            "## Review requirements",
            "",
            "- Review dependency, environment, license, and release-channel changes.",
            "- Inspect experimental Oritech and Oracle Index updates manually.",
            "- Merge only after CI passes; gameplay testing remains separate.",
            "",
        ]
    )
    return "\n".join(report)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("modrinth.index.json"))
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    game_version = manifest["dependencies"]["minecraft"]
    changes = []

    pinned = []
    for index, entry in enumerate(manifest["files"]):
        coords = coordinates(entry)
        if coords is None:
            print(f"Skipping non-Modrinth entry: {entry['path']}", file=sys.stderr)
            continue
        pinned.append((index, entry, *coords))

    versions_by_id = current_versions([version_id for _, _, _, version_id in pinned])

    def resolve(pin):
        index, entry, project_id, version_id = pin
        current = versions_by_id[version_id]
        candidates = compatible_versions(project_id, current, game_version)
        if not candidates or candidates[0]["id"] == version_id:
            return index, entry, current, None
        return index, entry, current, candidates[0]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        resolved = list(executor.map(resolve, pinned))

    for index, entry, current, latest in resolved:
        if latest is None:
            continue
        project_id, _ = coordinates(entry)
        project = request_json(f"project/{project_id}")
        manifest["files"][index] = updated_entry(entry, latest)
        changes.append((project, current, latest))

    if not changes:
        args.report.write_text(
            "## Modrinth metadata refresh\n\n"
            "No compatible artifact version changes were found. The generated "
            "catalog may still include upstream category or license metadata changes.\n"
        )
        print("All pinned Modrinth artifacts are current.")
        return 0

    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    args.report.write_text(render_report(changes, game_version))
    print(f"Prepared {len(changes)} update(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
