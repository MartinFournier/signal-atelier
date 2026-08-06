import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "smoke_server", ROOT / "scripts/smoke_server.py"
)
SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SMOKE)


class SmokeServerTests(unittest.TestCase):
    def test_server_files_exclude_client_only_entries(self):
        manifest = {
            "files": [
                {"path": "mods/both.jar", "env": {"server": "required"}},
                {"path": "mods/client.jar", "env": {"server": "unsupported"}},
                {"path": "mods/unspecified.jar"},
            ]
        }
        self.assertEqual(
            ["mods/both.jar", "mods/unspecified.jar"],
            [entry["path"] for entry in SMOKE.server_files(manifest)],
        )

    def test_safe_target_rejects_escape(self):
        root = Path("/tmp/signal-atelier-test-root")
        self.assertEqual(root / "mods/example.jar", SMOKE.safe_target(root, "mods/example.jar"))
        with self.assertRaises(ValueError):
            SMOKE.safe_target(root, "../example.jar")

    def test_download_hosts_are_fixed(self):
        SMOKE.require_url("https://cdn.modrinth.com/data/example.jar", SMOKE.MODRINTH_HOST)
        with self.assertRaises(ValueError):
            SMOKE.require_url("http://cdn.modrinth.com/data/example.jar", SMOKE.MODRINTH_HOST)
        with self.assertRaises(ValueError):
            SMOKE.require_url("https://example.com/example.jar", SMOKE.MODRINTH_HOST)


if __name__ == "__main__":
    unittest.main()
