import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "update_modrinth", Path(__file__).parents[1] / "scripts/update_modrinth.py"
)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


def version(version_id, number, channel="release", dependencies=None, changelog="Changes"):
    return {
        "id": version_id,
        "version_number": number,
        "version_type": channel,
        "loaders": ["neoforge"],
        "date_published": "2026-08-05T12:00:00Z",
        "dependencies": dependencies or [],
        "changelog": changelog,
        "files": [
            {
                "primary": True,
                "filename": f"example-{number}.jar",
                "url": f"https://cdn.modrinth.com/data/project/versions/{version_id}/example.jar",
                "hashes": {"sha1": "one", "sha512": "five-twelve"},
                "size": 42,
            }
        ],
    }


class UpdateModrinthTests(unittest.TestCase):
    def test_coordinates_rejects_ambiguous_downloads(self):
        self.assertIsNone(UPDATER.coordinates({"downloads": []}))
        self.assertIsNone(UPDATER.coordinates({"downloads": ["one", "two"]}))

    def test_release_channel_does_not_accept_beta(self):
        current = version("old", "1.0.0")
        beta = version("beta", "2.0.0-beta", "beta")
        release = version("new", "1.1.0")
        original = UPDATER.request_json
        UPDATER.request_json = lambda path, query=None: [beta, release]
        try:
            result = UPDATER.compatible_versions("project", current, "26.1.2")
        finally:
            UPDATER.request_json = original
        self.assertEqual([release], result)

    def test_updated_entry_preserves_environment_and_path_kind(self):
        entry = {
            "path": "shaderpacks/old.zip",
            "env": {"client": "required", "server": "unsupported"},
        }
        proposed = version("new", "2.0.0")
        proposed["files"][0]["filename"] = "new.zip"
        updated = UPDATER.updated_entry(entry, proposed)
        self.assertEqual("shaderpacks/new.zip", updated["path"])
        self.assertEqual(entry["env"], updated["env"])
        self.assertEqual(42, updated["fileSize"])

    def test_report_includes_ids_dates_dependencies_and_missing_changelog(self):
        old_dependency = {
            "project_id": "old-lib",
            "version_id": None,
            "dependency_type": "required",
        }
        new_dependency = {
            "project_id": "new-lib",
            "version_id": "lib-version",
            "dependency_type": "required",
        }
        current = version("old-id", "1.0.0", dependencies=[old_dependency])
        latest = version(
            "new-id", "2.0.0", dependencies=[new_dependency], changelog=None
        )
        project = {"title": "Example", "project_type": "mod", "slug": "example"}
        report = UPDATER.render_report([(project, current, latest)], "26.1.2")
        self.assertIn("`old-id`", report)
        self.assertIn("`new-id`", report)
        self.assertIn("2026-08-05 12:00:00 UTC", report)
        self.assertIn("Dependencies added: `new-lib`", report)
        self.assertIn("Dependencies removed: `old-lib`", report)
        self.assertIn("No changelog supplied", report)

    def test_dependency_order_does_not_create_delta(self):
        first = {"project_id": "a", "version_id": None, "dependency_type": "required"}
        second = {"project_id": "b", "version_id": None, "dependency_type": "optional"}
        current = version("old", "1", dependencies=[first, second])
        latest = version("new", "2", dependencies=[second, first])
        self.assertEqual(([], []), UPDATER.dependency_changes(current, latest))

    def test_main_updates_manifest_and_writes_review_report(self):
        current = version("old-id", "1.0.0")
        latest = version("new-id", "1.1.0")
        entry = {
            "path": "mods/example-1.0.0.jar",
            "hashes": {"sha1": "old", "sha512": "old"},
            "env": {"client": "required", "server": "required"},
            "downloads": [
                "https://cdn.modrinth.com/data/project/versions/old-id/example.jar"
            ],
            "fileSize": 1,
        }
        manifest = {
            "dependencies": {"minecraft": "26.1.2"},
            "files": [entry],
        }
        seen_query = {}

        def fake_request(path, query=None):
            if path == "versions":
                return [current]
            if path == "project/project/version":
                seen_query.update(query)
                return [latest]
            if path == "project/project":
                return {"title": "Example", "project_type": "mod", "slug": "example"}
            raise AssertionError(path)

        original_request = UPDATER.request_json
        original_argv = sys.argv
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            report_path = Path(directory) / "report.md"
            manifest_path.write_text(json.dumps(manifest))
            UPDATER.request_json = fake_request
            sys.argv = [
                "update_modrinth.py",
                "--manifest",
                str(manifest_path),
                "--report",
                str(report_path),
            ]
            try:
                self.assertEqual(0, UPDATER.main())
            finally:
                UPDATER.request_json = original_request
                sys.argv = original_argv

            updated = json.loads(manifest_path.read_text())
            self.assertEqual("mods/example-1.1.0.jar", updated["files"][0]["path"])
            self.assertIn("new-id", report_path.read_text())
            self.assertEqual('["neoforge"]', seen_query["loaders"])


if __name__ == "__main__":
    unittest.main()
