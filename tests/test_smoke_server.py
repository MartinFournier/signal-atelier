import importlib.util
import hashlib
import io
import tempfile
import unittest
from unittest import mock
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

    def test_verified_download_rehashes_cached_content(self):
        content = b"pinned artifact"
        expected = hashlib.sha512(content).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache_file = root / "cache" / "sha512" / expected
            cache_file.parent.mkdir(parents=True)
            cache_file.write_bytes(content)

            with mock.patch.object(SMOKE, "download") as download:
                cached = SMOKE.download_verified(
                    "https://cdn.modrinth.com/data/example.jar",
                    root / "runtime" / "mods" / "example.jar",
                    SMOKE.MODRINTH_HOST,
                    "sha512",
                    expected,
                    root / "cache",
                )

            self.assertTrue(cached)
            download.assert_not_called()
            self.assertEqual(content, (root / "runtime/mods/example.jar").read_bytes())

    def test_verified_download_replaces_corrupt_cache_entry(self):
        content = b"pinned artifact"
        expected = hashlib.sha512(content).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache_file = root / "cache" / "sha512" / expected
            cache_file.parent.mkdir(parents=True)
            cache_file.write_bytes(b"corrupt")

            def fake_download(url, target, host):
                target.write_bytes(content)

            with mock.patch.object(SMOKE, "download", side_effect=fake_download):
                cached = SMOKE.download_verified(
                    "https://cdn.modrinth.com/data/example.jar",
                    root / "runtime" / "mods" / "example.jar",
                    SMOKE.MODRINTH_HOST,
                    "sha512",
                    expected,
                    root / "cache",
                )

            self.assertFalse(cached)
            self.assertEqual(content, cache_file.read_bytes())

    def test_digest_must_be_lowercase_hex(self):
        with self.assertRaises(ValueError):
            SMOKE.require_digest("not-a-digest", "sha256")

    def test_failure_log_tail_is_bounded_and_sanitized(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            home = Path.home()
            log = runtime / "server-smoke.log"
            log.write_text(
                "discarded\n"
                f"\x1b[31merror in {runtime}/mods/example.jar\x1b[0m\n"
                f"home path: {home}/.cache/example\x00 hidden\n"
            )

            lines = SMOKE.sanitized_log_tail(
                log,
                runtime,
                max_lines=2,
                max_characters=80,
            )

        self.assertEqual(
            [
                "error in <runtime>/mods/example.jar",
                "home path: <home>/.cache/example hidden",
            ],
            lines,
        )

    def test_missing_failure_log_is_reported_without_runtime_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            output = io.StringIO()
            with mock.patch("sys.stderr", output):
                SMOKE.print_failure_log(runtime)

        self.assertIn("<log unavailable>", output.getvalue())
        self.assertNotIn(str(runtime), output.getvalue())


if __name__ == "__main__":
    unittest.main()
