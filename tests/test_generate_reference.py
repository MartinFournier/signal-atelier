import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generate_reference", ROOT / "scripts/generate_reference.py"
)
REFERENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFERENCE)


class GenerateReferenceTests(unittest.TestCase):
    def test_reference_matches_tracked_sources(self):
        manifest = json.loads((ROOT / "modrinth.index.json").read_text())
        chapters, quest_count = REFERENCE.quest_summary(ROOT)
        output = REFERENCE.render(ROOT)
        self.assertIn(f"| Artifacts | {len(manifest['files'])} |", output)
        self.assertIn(f"| Minecraft | {manifest['dependencies']['minecraft']} |", output)
        self.assertIn(f"| NeoForge | {manifest['dependencies']['neoforge']} |", output)
        self.assertIn(f"| Quest chapters | {len(chapters)} |", output)
        self.assertIn(f"| Quest milestones | {quest_count} |", output)

    def test_every_artifact_has_a_modrinth_project(self):
        manifest = json.loads((ROOT / "modrinth.index.json").read_text())
        identifiers = [REFERENCE.project_id(entry) for entry in manifest["files"]]
        self.assertEqual(len(manifest["files"]), len(identifiers))
        self.assertTrue(all(identifiers))

    def test_recipe_locks_are_empty_objects(self):
        data_root = ROOT / "overrides/config/universaldatapack/data"
        for relative in REFERENCE.recipe_locks(ROOT):
            self.assertEqual({}, json.loads((data_root / relative).read_text()))


if __name__ == "__main__":
    unittest.main()
