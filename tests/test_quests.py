import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
QUEST_ROOT = ROOT / "overrides/config/simplyquests"


class QuestChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.groups = json.loads((QUEST_ROOT / "groups.json").read_text())
        cls.chapters = [
            json.loads(path.read_text())
            for path in sorted((QUEST_ROOT / "chapters").glob("*.json"))
        ]
        cls.quests = [quest for chapter in cls.chapters for quest in chapter["quests"]]

    def test_expected_chapters_and_quest_count(self):
        expected = [
            "orientation",
            "power",
            "industry",
            "distributed_works",
            "storage",
            "supertech",
            "signal_core",
        ]
        group = self.groups["groups"][0]
        self.assertEqual(expected, group["chapters"])
        self.assertEqual(27, len(self.quests))
        self.assertEqual(expected, [
            chapter["name"]
            for chapter in sorted(self.chapters, key=lambda item: item["chapterOrder"])
        ])

    def test_ids_and_dependencies_are_valid(self):
        quest_ids = [quest["id"] for quest in self.quests]
        self.assertEqual(len(quest_ids), len(set(quest_ids)))
        task_ids = [task["id"] for quest in self.quests for task in quest["tasks"]]
        self.assertEqual(len(task_ids), len(set(task_ids)))
        known = set(quest_ids)
        for quest in self.quests:
            self.assertTrue(set(quest["dependencies"]).issubset(known))

    def test_chain_is_non_gating_and_reward_free(self):
        for quest in self.quests:
            self.assertEqual([], quest["rewards"])
            self.assertFalse(quest["settings"]["isRepeatable"])
            self.assertEqual(1, len(quest["tasks"]))
            task = quest["tasks"][0]
            self.assertEqual("checkbox", task["type"])
            self.assertFalse(task["consume"])
            self.assertFalse(task["repeatable"])

    def test_optional_projects_and_supertech_dependencies(self):
        quests = {quest["id"]: quest for quest in self.quests}
        optional = {
            identifier
            for identifier, quest in quests.items()
            if quest["settings"]["isOptional"]
        }
        self.assertEqual(
            {
                "simplyquests:signal_atelier/distributed_works/one_loaded_chunk",
                "simplyquests:signal_atelier/signal_core/project_charter",
                "simplyquests:signal_atelier/signal_core/production_cells",
                "simplyquests:signal_atelier/signal_core/interdimensional_supply",
                "simplyquests:signal_atelier/signal_core/continuous_run",
            },
            optional,
        )
        nuclear = quests["simplyquests:signal_atelier/supertech/nuclear_scale"]
        self.assertEqual(
            {
                "simplyquests:signal_atelier/storage/respect_the_locks",
                "simplyquests:signal_atelier/distributed_works/drone_route",
            },
            set(nuclear["dependencies"]),
        )

    def test_descriptions_teach_cross_mod_boundaries(self):
        descriptions = {
            quest["id"]: quest["description"] for quest in self.quests
        }
        expected_terms = {
            "simplyquests:signal_atelier/distributed_works/remote_site": (
                "XP Tome",
                "Traveler's Backpack",
                "GraveStone",
                "Xaero waypoint",
            ),
            "simplyquests:signal_atelier/storage/external_boundaries": (
                "Refined Storage owns storage and requests",
                "Oritech pipes own machine-side movement",
            ),
            "simplyquests:signal_atelier/storage/factory_request": (
                "Refined Storage",
                "Oritech machine",
                "dedicated Interface",
            ),
            "simplyquests:signal_atelier/signal_core/production_cells": (
                "Oritech-and-Rechiseled",
            ),
        }
        for identifier, terms in expected_terms.items():
            for term in terms:
                self.assertIn(term, descriptions[identifier])

    def test_chapter_schema_basics(self):
        for chapter in self.chapters:
            self.assertEqual("signal_atelier", chapter["group"])
            self.assertEqual([], chapter["canvasImages"])
            self.assertEqual([], chapter["canvasTexts"])
            self.assertGreater(chapter["zoom"], 0)


if __name__ == "__main__":
    unittest.main()
