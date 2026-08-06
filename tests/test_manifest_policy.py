import json
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).parents[1]
MANIFEST = json.loads((ROOT / "modrinth.index.json").read_text())
METADATA = json.loads((ROOT / "data/modrinth-metadata.json").read_text())
ENVIRONMENTS = {"required", "optional", "unsupported"}


def coordinates(entry: dict) -> tuple[str, str]:
    parsed = urlparse(entry["downloads"][0])
    parts = parsed.path.split("/")
    if len(parts) < 6 or parts[1] != "data" or parts[3] != "versions":
        raise ValueError(entry["downloads"][0])
    return parts[2], parts[4]


class ManifestPolicyTests(unittest.TestCase):
    def test_manifest_identity_and_dependencies_are_complete(self):
        self.assertEqual(1, MANIFEST["formatVersion"])
        self.assertEqual("minecraft", MANIFEST["game"])
        self.assertTrue(MANIFEST["name"])
        self.assertTrue(MANIFEST["versionId"])
        self.assertTrue(MANIFEST["summary"])
        self.assertEqual({"minecraft", "neoforge"}, set(MANIFEST["dependencies"]))

    def test_artifact_paths_urls_and_coordinates_are_unique(self):
        paths = [entry["path"] for entry in MANIFEST["files"]]
        downloads = [entry["downloads"][0] for entry in MANIFEST["files"]]
        pins = [coordinates(entry) for entry in MANIFEST["files"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(len(downloads), len(set(downloads)))
        self.assertEqual(len(pins), len(set(pins)))

        for entry in MANIFEST["files"]:
            self.assertEqual(1, len(entry["downloads"]))
            parsed = urlparse(entry["downloads"][0])
            self.assertEqual("https", parsed.scheme)
            self.assertEqual("cdn.modrinth.com", parsed.hostname)
            self.assertIn(Path(entry["path"]).parts[0], {"mods", "shaderpacks"})
            self.assertEqual(Path(entry["path"]).name, Path(unquote(parsed.path)).name)
            self.assertGreater(entry["fileSize"], 0)

    def test_artifact_hashes_and_environments_are_explicit(self):
        for entry in MANIFEST["files"]:
            self.assertRegex(entry["hashes"]["sha1"], r"^[0-9a-f]{40}$")
            self.assertRegex(entry["hashes"]["sha512"], r"^[0-9a-f]{128}$")
            self.assertEqual({"client", "server"}, set(entry["env"]))
            self.assertIn(entry["env"]["client"], ENVIRONMENTS)
            self.assertIn(entry["env"]["server"], ENVIRONMENTS)

    def test_cached_metadata_exactly_covers_manifest_pins(self):
        pins = {coordinates(entry) for entry in MANIFEST["files"]}
        project_ids = {project_id for project_id, _ in pins}
        version_ids = {version_id for _, version_id in pins}
        self.assertEqual(project_ids, set(METADATA["projects"]))
        self.assertEqual(version_ids, set(METADATA["versions"]))

        for project_id, version_id in pins:
            project = METADATA["projects"][project_id]
            version = METADATA["versions"][version_id]
            self.assertEqual(project_id, version["project_id"])
            self.assertTrue(project["title"])
            self.assertTrue(project["slug"])
            self.assertIn(project["project_type"], {"mod", "shader"})
            self.assertTrue(project["license"]["id"] or project["license"]["name"])
            self.assertTrue(version["version_number"])
            self.assertIn(version["version_type"], {"release", "beta", "alpha"})
            self.assertRegex(version["date_published"], r"^\d{4}-\d{2}-\d{2}T")


if __name__ == "__main__":
    unittest.main()
