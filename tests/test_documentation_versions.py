import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).parents[1]
CURRENT_DOCS = [
    ROOT / "README.md",
    ROOT / "docs/index.md",
    ROOT / "docs/status.md",
    ROOT / "docs/roadmap.md",
    ROOT / "docs/test-plan.md",
    ROOT / "docs/graphical-test-tasklist.md",
    *sorted((ROOT / "docs/guide").glob("*.md")),
]
ARCHIVE_REFERENCES = [
    *CURRENT_DOCS,
    ROOT / ".github/workflows/ci.yml",
    ROOT / "scripts/build_pack.py",
    ROOT / "scripts/check.sh",
]
ORITECH_PROJECT_ID = "4sYI62kA"


def manifest_facts() -> dict[str, str]:
    manifest = json.loads((ROOT / "modrinth.index.json").read_text())
    metadata = json.loads((ROOT / "data/modrinth-metadata.json").read_text())
    oritech = next(
        entry
        for entry in manifest["files"]
        if f"/data/{ORITECH_PROJECT_ID}/" in entry["downloads"][0]
    )
    url_parts = urlparse(unquote(oritech["downloads"][0])).path.split("/")
    version_id = url_parts[url_parts.index("versions") + 1]
    java_workflow = (ROOT / ".github/workflows/server-smoke.yml").read_text()
    java = re.search(r'^\s+java-version: "(\d+)"$', java_workflow, re.MULTILINE)
    if java is None:
        raise ValueError("server smoke workflow has no Java version")
    return {
        "pack": manifest["versionId"],
        "minecraft": manifest["dependencies"]["minecraft"],
        "neoforge": manifest["dependencies"]["neoforge"],
        "oritech": metadata["versions"][version_id]["version_number"],
        "java": java.group(1),
    }


class DocumentationVersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = manifest_facts()

    def assert_references_match(self, files, pattern, expected, label):
        found = []
        stale = []
        for path in files:
            for match in re.findall(pattern, path.read_text()):
                found.append((path, match))
                if match != expected:
                    stale.append(f"{path.relative_to(ROOT)}: {match}")
        self.assertTrue(found, f"no {label} references found")
        self.assertEqual([], stale, f"stale {label} references: {stale}")

    def test_current_documentation_versions_match_tracked_sources(self):
        self.assert_references_match(
            CURRENT_DOCS,
            r"Minecraft (\d+\.\d+\.\d+)",
            self.facts["minecraft"],
            "Minecraft version",
        )
        self.assert_references_match(
            CURRENT_DOCS,
            r"NeoForge (\d+\.\d+\.\d+\.\d+)",
            self.facts["neoforge"],
            "NeoForge version",
        )
        self.assert_references_match(
            CURRENT_DOCS,
            r"Java (\d+)",
            self.facts["java"],
            "Java version",
        )
        self.assert_references_match(
            CURRENT_DOCS,
            r"Oritech (\d+\.\d+\.\d+(?:-[A-Za-z0-9]+)?)",
            self.facts["oritech"],
            "Oritech version",
        )
        self.assert_references_match(
            CURRENT_DOCS,
            r"Signal Atelier (\d+\.\d+\.\d+)",
            self.facts["pack"],
            "pack version",
        )

    def test_archive_names_match_the_manifest_version(self):
        self.assert_references_match(
            ARCHIVE_REFERENCES,
            r"signal-atelier-(\d+\.\d+\.\d+)\.mrpack",
            self.facts["pack"],
            "archive version",
        )


if __name__ == "__main__":
    unittest.main()
