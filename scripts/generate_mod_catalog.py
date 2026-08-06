#!/usr/bin/env python3
"""Refresh pinned Modrinth metadata and generate the public mod catalog."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
API = "https://api.modrinth.com/v2"
USER_AGENT = "MartinFournier/signal-atelier (catalog generator)"
MANIFEST = ROOT / "modrinth.index.json"
METADATA = ROOT / "data/modrinth-metadata.json"
TSV = ROOT / "docs/reference/mods.tsv"
PAGE = ROOT / "docs/reference/mods.md"
LICENSE_PAGE = ROOT / "docs/reference/licenses.md"


def coordinates(entry: dict) -> tuple[str, str]:
    parts = urllib.parse.urlparse(entry["downloads"][0]).path.split("/")
    if len(parts) < 5 or parts[1] != "data" or parts[3] != "versions":
        raise ValueError(f"unexpected Modrinth URL: {entry['downloads'][0]}")
    return parts[2], parts[4]


def request_many(resource: str, identifiers: list[str]) -> list[dict]:
    query = urllib.parse.urlencode({"ids": json.dumps(identifiers)})
    request = urllib.request.Request(
        f"{API}/{resource}?{query}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def normalized_project(project: dict) -> dict:
    license_data = project.get("license") or {}
    return {
        "title": project["title"],
        "slug": project["slug"],
        "project_type": project["project_type"],
        "categories": sorted(project.get("categories", [])),
        "license": {
            "id": license_data.get("id", ""),
            "name": license_data.get("name", ""),
            "url": license_data.get("url") or "",
        },
    }


def normalized_version(version: dict) -> dict:
    dependencies = []
    for dependency in version.get("dependencies", []):
        dependencies.append(
            {
                "project_id": dependency.get("project_id"),
                "version_id": dependency.get("version_id"),
                "dependency_type": dependency["dependency_type"],
            }
        )
    return {
        "project_id": version["project_id"],
        "version_number": version["version_number"],
        "version_type": version["version_type"],
        "date_published": version["date_published"],
        "dependencies": dependencies,
    }


def refresh(manifest: dict) -> dict:
    pins = [coordinates(entry) for entry in manifest["files"]]
    project_ids = sorted({project_id for project_id, _ in pins})
    version_ids = sorted({version_id for _, version_id in pins})
    projects = request_many("projects", project_ids)
    versions = request_many("versions", version_ids)
    if len(projects) != len(project_ids) or len(versions) != len(version_ids):
        raise ValueError("Modrinth returned incomplete catalog metadata")
    return {
        "schema": 1,
        "projects": {
            project["id"]: normalized_project(project)
            for project in sorted(projects, key=lambda item: item["id"])
        },
        "versions": {
            version["id"]: normalized_version(version)
            for version in sorted(versions, key=lambda item: item["id"])
        },
    }


def project_url(project: dict) -> str:
    project_type = urllib.parse.quote(project["project_type"], safe="")
    slug = urllib.parse.quote(project["slug"], safe="")
    return f"https://modrinth.com/{project_type}/{slug}"


def dependency_parents(metadata: dict) -> dict[str, list[str]]:
    versions = metadata["versions"]
    version_projects = {
        version_id: version["project_id"] for version_id, version in versions.items()
    }
    parents = defaultdict(list)
    for version in versions.values():
        parent = metadata["projects"][version["project_id"]]["title"]
        for dependency in version["dependencies"]:
            project_id = dependency["project_id"]
            if not project_id and dependency["version_id"]:
                project_id = version_projects.get(dependency["version_id"])
            if project_id in metadata["projects"]:
                parents[project_id].append(
                    f"{parent} ({dependency['dependency_type']})"
                )
    return {key: sorted(set(value), key=str.casefold) for key, value in parents.items()}


def rows(manifest: dict, metadata: dict) -> list[dict[str, str]]:
    parents = dependency_parents(metadata)
    catalog = []
    for entry in manifest["files"]:
        project_id, version_id = coordinates(entry)
        if project_id not in metadata["projects"] or version_id not in metadata["versions"]:
            raise ValueError(f"metadata missing for {entry['path']}")
        project = metadata["projects"][project_id]
        version = metadata["versions"][version_id]
        if version["project_id"] != project_id:
            raise ValueError(f"project/version mismatch for {entry['path']}")
        license_data = project["license"]
        catalog.append(
            {
                "name": project["title"],
                "categories": "; ".join(project["categories"]),
                "project_id": project_id,
                "version": version["version_number"],
                "version_id": version_id,
                "project_url": project_url(project),
                "filename": Path(entry["path"]).name,
                "sha512": entry["hashes"]["sha512"],
                "client": entry.get("env", {}).get("client", "unspecified"),
                "server": entry.get("env", {}).get("server", "unspecified"),
                "release_channel": version["version_type"],
                "license": license_data["name"] or license_data["id"],
                "license_url": license_data["url"],
                "dependency_of": "; ".join(parents.get(project_id, [])),
                "published_at": version["date_published"],
            }
        )
    return sorted(catalog, key=lambda item: item["name"].casefold())


def render_tsv(catalog: list[dict[str, str]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output, fieldnames=list(catalog[0]), delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(catalog)
    return output.getvalue()


def markdown(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("`", "&#96;")
    )


def https_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    return value if parsed.scheme == "https" and parsed.hostname else ""


def render_page(catalog: list[dict[str, str]]) -> str:
    lines = [
        "# Mod catalog",
        "",
        "<!-- Generated by scripts/generate_mod_catalog.py; do not edit by hand. -->",
        "",
        "This player-facing table shows a subset of the tracked catalog.",
        "[Download the complete TSV](mods.tsv) for exact IDs, filenames, hashes,",
        "environments, release channels, publication dates, and dependency",
        "relationships. Select a column heading to sort the table.",
        "",
        "| Mod | Categories | Version | License |",
        "| --- | --- | --- | --- |",
    ]
    for item in catalog:
        name = f"[{markdown(item['name'])}]({item['project_url']})"
        license_name = markdown(item["license"] or "Not specified")
        license_url = https_url(item["license_url"])
        if license_url:
            license_name = f"[{license_name}]({license_url})"
        lines.append(
            f"| {name} | {markdown(item['categories'])} | "
            f"`{markdown(item['version'])}` | {license_name} |"
        )
    lines.extend(["", f"Total: **{len(catalog)} artifacts**.", ""])
    return "\n".join(lines)


def license_label(item: dict[str, str]) -> str:
    label = markdown(item["license"] or "Not specified")
    url = https_url(item["license_url"])
    return f"[{label}]({url})" if url else label


def render_license_page(catalog: list[dict[str, str]]) -> str:
    review_required = [
        item
        for item in catalog
        if item["license"].startswith("LicenseRef-") or not item["license"]
    ]
    lines = [
        "# Licenses and distribution",
        "",
        "<!-- Generated by scripts/generate_mod_catalog.py; do not edit by hand. -->",
        "",
        "Signal Atelier's `.mrpack` contains its manifest and pack-owned",
        "`overrides/`; it does not embed the mod JARs or shader archive listed",
        "below. Prism Launcher downloads those pinned artifacts directly from",
        "Modrinth, and every upstream project retains its own license.",
        "",
        "The repository's original scripts, documentation, configuration, quest",
        "definitions, and branding assets are distributed under the repository",
        "[MIT License](https://github.com/MartinFournier/signal-atelier/blob/main/LICENSE).",
        "That license does not replace or extend to",
        "third-party artifacts.",
        "",
        "## Terms requiring manual review",
        "",
        "These projects report custom, all-rights-reserved, or otherwise",
        "non-standard license identifiers. The current pack links to their",
        "Modrinth downloads rather than redistributing their files. Re-review",
        "their current terms before embedding, mirroring, or bundling them",
        "outside the normal Modrinth download flow.",
        "",
        "| Project | Version | Reported license |",
        "| --- | --- | --- |",
    ]
    for item in review_required:
        name = f"[{markdown(item['name'])}]({item['project_url']})"
        lines.append(
            f"| {name} | `{markdown(item['version'])}` | {license_label(item)} |"
        )

    lines.extend([
        "",
        "## Complete upstream attribution",
        "",
        "All entries are delivered as checksum-pinned Modrinth downloads, not as",
        "files embedded in the Signal Atelier archive.",
        "",
        "| Project | Version | Reported license | Delivery |",
        "| --- | --- | --- | --- |",
    ])
    for item in catalog:
        name = f"[{markdown(item['name'])}]({item['project_url']})"
        lines.append(
            f"| {name} | `{markdown(item['version'])}` | "
            f"{license_label(item)} | Modrinth download |"
        )
    lines.extend(["", f"Total: **{len(catalog)} external artifacts**.", ""])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="refresh metadata from Modrinth")
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(MANIFEST.read_text())
    if args.refresh:
        metadata = refresh(manifest)
        METADATA.parent.mkdir(parents=True, exist_ok=True)
        METADATA.write_text(json.dumps(metadata, indent=2) + "\n")
    elif not METADATA.exists():
        print("Catalog metadata missing; run with --refresh", file=sys.stderr)
        return 1
    else:
        metadata = json.loads(METADATA.read_text())

    catalog = rows(manifest, metadata)
    expected = {
        TSV: render_tsv(catalog),
        PAGE: render_page(catalog),
        LICENSE_PAGE: render_license_page(catalog),
    }
    if args.check:
        stale = [path for path, content in expected.items() if not path.exists() or path.read_text() != content]
        if stale:
            for path in stale:
                print(f"Generated catalog is stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        return 0
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
