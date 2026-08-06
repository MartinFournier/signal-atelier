import json
import re
import unittest
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).parents[1]
INTEGRATION = ROOT / "docs/reference/integration.md"


def project_id(entry: dict) -> str:
    parts = urlparse(entry["downloads"][0]).path.split("/")
    return parts[2]


class IntegrationReferenceTests(unittest.TestCase):
    def test_every_manifest_project_has_one_integration_entry(self):
        manifest = json.loads((ROOT / "modrinth.index.json").read_text())
        expected = Counter(project_id(entry) for entry in manifest["files"])
        documented = Counter(
            re.findall(
                r"https://modrinth\.com/project/([A-Za-z0-9]+)",
                INTEGRATION.read_text(),
            )
        )
        self.assertEqual(expected, documented)


if __name__ == "__main__":
    unittest.main()
