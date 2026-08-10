import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
QUEST_ROOT = ROOT / "overrides/config/simplyquests"
EXPECTED_SLUGS = {
    "orientation": ["read_the_brief", "survey_a_site", "mark_the_baseline"],
    "power": ["first_generation", "buffer_and_measure", "renewable_baseline"],
    "industry": [
        "processing_line",
        "principal_alloys",
        "fluids_and_oil",
        "rebuild_after_restart",
    ],
    "distributed_works": [
        "pipes_first",
        "remote_site",
        "drone_route",
        "one_loaded_chunk",
    ],
    "storage": [
        "storage_core",
        "external_boundaries",
        "first_pattern",
        "factory_request",
        "respect_the_locks",
    ],
    "supertech": [
        "nuclear_scale",
        "particle_products",
        "renewable_supertech",
        "survive_a_restart",
    ],
    "signal_core": [
        "project_charter",
        "production_cells",
        "interdimensional_supply",
        "continuous_run",
    ],
}


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

    def test_ids_remain_stable_for_saved_progress(self):
        expected = {
            f"simplyquests:signal_atelier/{chapter}/{slug}"
            for chapter, slugs in EXPECTED_SLUGS.items()
            for slug in slugs
        }
        self.assertEqual(expected, {quest["id"] for quest in self.quests})

    def test_graph_is_acyclic_and_reachable(self):
        dependencies = {
            quest["id"]: set(quest["dependencies"]) for quest in self.quests
        }
        visiting = set()
        visited = set()

        def visit(identifier):
            self.assertNotIn(identifier, visiting, f"quest dependency cycle at {identifier}")
            if identifier in visited:
                return
            visiting.add(identifier)
            for dependency in dependencies[identifier]:
                visit(dependency)
            visiting.remove(identifier)
            visited.add(identifier)

        for identifier in dependencies:
            visit(identifier)
        self.assertEqual(set(dependencies), visited)

    def test_dependencies_only_point_backward(self):
        chapters = {
            chapter["name"]: chapter["chapterOrder"] for chapter in self.chapters
        }
        positions = {
            quest["id"]: (chapters[quest["chapterName"]], quest["x"])
            for quest in self.quests
        }
        for quest in self.quests:
            for dependency in quest["dependencies"]:
                self.assertLess(positions[dependency], positions[quest["id"]])

    def test_each_chapter_has_one_entry_quest(self):
        for chapter in self.chapters:
            entries = []
            for quest in chapter["quests"]:
                external = [
                    dependency
                    for dependency in quest["dependencies"]
                    if f"/{chapter['name']}/" not in dependency
                ]
                if external or not quest["dependencies"]:
                    entries.append(quest["id"])
            self.assertEqual(1, len(entries), chapter["name"])

    def test_optional_quests_do_not_gate_required_quests(self):
        quests = {quest["id"]: quest for quest in self.quests}
        optional = {
            identifier
            for identifier, quest in quests.items()
            if quest["settings"]["isOptional"]
        }

        def ancestors(identifier):
            result = set()
            pending = list(quests[identifier]["dependencies"])
            while pending:
                dependency = pending.pop()
                if dependency not in result:
                    result.add(dependency)
                    pending.extend(quests[dependency]["dependencies"])
            return result

        for identifier in quests.keys() - optional:
            self.assertTrue(ancestors(identifier).isdisjoint(optional), identifier)

    def test_chain_is_non_gating_and_reward_free(self):
        for quest in self.quests:
            self.assertEqual([], quest["rewards"])
            self.assertFalse(quest["settings"]["isRepeatable"])
            self.assertEqual(1, len(quest["tasks"]))
            task = quest["tasks"][0]
            self.assertEqual("checkbox", task["type"])
            self.assertFalse(task["consume"])
            self.assertFalse(task["repeatable"])

    def test_milestones_use_curated_vanilla_icons(self):
        icons = [quest["logo"] for quest in self.quests]
        self.assertTrue(all(icon.startswith("minecraft:") for icon in icons))
        self.assertTrue(all(not quest["settings"]["useTaskIcon"] for quest in self.quests))
        self.assertNotIn("minecraft:paper", icons)
        self.assertGreaterEqual(len(set(icons)), 20)

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
