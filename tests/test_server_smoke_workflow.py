import fnmatch
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github/workflows/server-smoke.yml"
CLIENT_ONLY_OVERRIDES = {
    "overrides/config/defaultoptions-common.toml",
    "overrides/config/defaultoptions/extra/config/xaeroworldmap.txt",
    "overrides/config/defaultoptions/extra/config/xaerominimap.txt",
    "overrides/config/defaultoptions/options.txt",
    "overrides/config/distanthorizons.toml",
    "overrides/config/dynamic_fps.json",
    "overrides/config/simplemenu.json5",
    "overrides/config/simplemenu/icon/icon_16x16.png",
    "overrides/config/simplemenu/icon/icon_32x32.png",
    "overrides/config/simplemenu/logo/logo.png",
}


def trigger_paths() -> list[str]:
    paths = []
    reading = False
    for line in WORKFLOW.read_text().splitlines():
        if line == "    paths:":
            reading = True
            continue
        if reading and line.startswith("      - "):
            paths.append(line.removeprefix("      - "))
        elif reading and line.strip():
            break
    return paths


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


class ServerSmokeWorkflowTests(unittest.TestCase):
    def test_executes_only_after_merge_or_manual_dispatch(self):
        workflow = WORKFLOW.read_text()
        self.assertIn("  push:\n    branches:\n      - main", workflow)
        self.assertIn("  workflow_dispatch:", workflow)
        self.assertNotIn("pull_request:", workflow)

    def test_all_server_relevant_sources_trigger_smoke_test(self):
        patterns = trigger_paths()
        required = {
            ".github/workflows/server-smoke.yml",
            "modrinth.index.json",
            "scripts/smoke_server.py",
            "tests/test_smoke_server.py",
        }
        override_files = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "overrides").rglob("*")
            if path.is_file()
        }
        required.update(override_files - CLIENT_ONLY_OVERRIDES)
        uncovered = sorted(path for path in required if not matches(path, patterns))
        self.assertEqual([], uncovered)

    def test_client_only_overrides_do_not_trigger_downloaded_code(self):
        patterns = trigger_paths()
        covered = sorted(
            path for path in CLIENT_ONLY_OVERRIDES if matches(path, patterns)
        )
        self.assertEqual([], covered)


if __name__ == "__main__":
    unittest.main()
