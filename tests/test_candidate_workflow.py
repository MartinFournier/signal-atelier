import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github/workflows/candidate.yml"


class CandidateWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text()

    def test_is_manual_and_read_only(self):
        self.assertIn("  workflow_dispatch:", self.workflow)
        self.assertNotIn("  push:", self.workflow)
        self.assertNotIn("  pull_request:", self.workflow)
        self.assertIn("permissions:\n  contents: read", self.workflow)
        self.assertNotIn("secrets.", self.workflow)

    def test_validates_checksum_and_uploads_both_files(self):
        self.assertIn("run: scripts/check.sh", self.workflow)
        self.assertIn("run: scripts/check-docs.sh", self.workflow)
        self.assertIn("sha256sum --check", self.workflow)
        self.assertIn("dist/signal-atelier-0.3.0.mrpack\n", self.workflow)
        self.assertIn("dist/signal-atelier-0.3.0.mrpack.sha256\n", self.workflow)
        self.assertIn("actions/upload-artifact@", self.workflow)

    def test_does_not_contain_release_or_modrinth_steps(self):
        lowered = self.workflow.lower()
        self.assertNotIn("gh release", lowered)
        self.assertNotIn("modrinth", lowered)
        self.assertNotIn("actions/create-release", lowered)


if __name__ == "__main__":
    unittest.main()
