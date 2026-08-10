#!/usr/bin/env python3
"""Generate the curated, non-gating Simply Quests engineering notebook."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


GROUP = "signal_atelier"
GROUP_COLOR = -3704262  # ARGB FFC77A3A, stored as a signed Java integer.
ROOT = Path(__file__).parents[1]
OUTPUT = ROOT / "overrides/config/simplyquests"
OPTIONAL_QUESTS = {
    "distributed_works/one_loaded_chunk",
    "signal_core/project_charter",
    "signal_core/production_cells",
    "signal_core/interdimensional_supply",
    "signal_core/continuous_run",
}
QUEST_ICONS = {
    "orientation/read_the_brief": "minecraft:book",
    "orientation/survey_a_site": "minecraft:compass",
    "orientation/mark_the_baseline": "minecraft:chest",
    "power/first_generation": "minecraft:redstone_torch",
    "power/buffer_and_measure": "minecraft:comparator",
    "power/renewable_baseline": "minecraft:daylight_detector",
    "industry/processing_line": "minecraft:furnace",
    "industry/principal_alloys": "minecraft:iron_ingot",
    "industry/fluids_and_oil": "minecraft:bucket",
    "industry/rebuild_after_restart": "minecraft:observer",
    "distributed_works/pipes_first": "minecraft:hopper",
    "distributed_works/remote_site": "minecraft:minecart",
    "distributed_works/drone_route": "minecraft:phantom_membrane",
    "distributed_works/one_loaded_chunk": "minecraft:lodestone",
    "storage/storage_core": "minecraft:chest",
    "storage/external_boundaries": "minecraft:barrel",
    "storage/first_pattern": "minecraft:crafting_table",
    "storage/factory_request": "minecraft:hopper",
    "storage/respect_the_locks": "minecraft:barrier",
    "supertech/nuclear_scale": "minecraft:beacon",
    "supertech/particle_products": "minecraft:end_crystal",
    "supertech/renewable_supertech": "minecraft:blaze_powder",
    "supertech/survive_a_restart": "minecraft:clock",
    "signal_core/project_charter": "minecraft:writable_book",
    "signal_core/production_cells": "minecraft:copper_block",
    "signal_core/interdimensional_supply": "minecraft:ender_eye",
    "signal_core/continuous_run": "minecraft:nether_star",
}

CHAPTERS = [
    (
        "orientation",
        "Orientation",
        "minecraft:compass",
        [
            ("read_the_brief", "Read the Brief", "Know the workshop", "Read this notebook and the Oracle Index. Signal Atelier is built around Oritech; Refined Storage is intentionally limited to storage and autocrafting.", None),
            ("survey_a_site", "Survey a Site", "Leave room to grow", "Choose a workshop site with expansion space, safe cable routes, and room for noisy or hazardous late-game machinery. Mark it with an ordinary Xaero waypoint; mapping is for navigation, not teleportation or radar.", "read_the_brief"),
            ("mark_the_baseline", "Mark the Baseline", "Protect the experiment", "Treat this world as disposable while Oritech 2 and NeoForge remain experimental. Confirm that a recoverable backup exists outside the instance.", "survey_a_site"),
        ],
    ),
    (
        "power",
        "Power",
        "minecraft:redstone",
        [
            ("first_generation", "First Generation", "Make power visible", "Build an Oritech generator and verify that energy reaches a machine. Prefer a measured, expandable layout over a temporary cable tangle.", "orientation/mark_the_baseline"),
            ("buffer_and_measure", "Buffer and Measure", "Understand demand", "Add energy storage or monitoring, then observe idle and working demand. Leave capacity for the next processing line.", "first_generation"),
            ("renewable_baseline", "Renewable Baseline", "Keep the workshop alive", "Establish a renewable or continuously supplied generation path before scaling automation.", "buffer_and_measure"),
        ],
    ),
    (
        "industry",
        "Industry",
        "minecraft:blast_furnace",
        [
            ("processing_line", "Processing Line", "From input to product", "Build a repeatable Oritech processing line with explicit inputs, outputs, and overflow handling.", "power/renewable_baseline"),
            ("principal_alloys", "Principal Alloys", "Stock the intermediates", "Use the Oracle Index and JEI to identify Oritech's recurring alloys and components, then automate them instead of crafting each machine ad hoc.", "processing_line"),
            ("fluids_and_oil", "Fluids and Oil", "Separate the networks", "Process fluids through dedicated, labeled routes. Confirm that shutdown and restart do not strand or mix contents.", "principal_alloys"),
            ("rebuild_after_restart", "Rebuild After Restart", "Persistence is part of the machine", "Restart the game or server and verify that multiblocks, inventories, fluids, and energy reconnect correctly.", "fluids_and_oil"),
        ],
    ),
    (
        "distributed_works",
        "Distributed Works",
        "minecraft:rail",
        [
            ("pipes_first", "Pipes First", "Local logistics belong to Oritech", "Move items, fluids, and energy with Oritech infrastructure before introducing centralized storage.", "industry/rebuild_after_restart"),
            ("remote_site", "Remote Site", "Build beyond the workshop", "Before supplying a remote site, prove the field kit: store XP in an XP Tome carried by an equipped Traveler's Backpack, confirm GraveStone returns both without loss, and mark the site with an ordinary Xaero waypoint.", "pipes_first"),
            ("drone_route", "Drone Route", "Cross the difficult gap", "Use Oritech drones or another Oritech-native solution for world interaction and long-distance logistics; Refined Storage must not replace the route.", "remote_site"),
            ("one_loaded_chunk", "One Loaded Chunk", "Spend persistence carefully", "Optionally place only the single-chunk loader at a proven remote site. Confirm ownership, the offline timeout, and the four-chunk-per-player limit; no factory should require it to remain safe.", "drone_route"),
        ],
    ),
    (
        "storage",
        "Storage and Requests",
        "minecraft:chest",
        [
            ("storage_core", "Storage Core", "Centralize without replacing the factory", "Build a Refined Storage Controller, Grid, Drive, and initial disk. Power the network from Oritech.", "distributed_works/pipes_first"),
            ("external_boundaries", "External Boundaries", "Interfaces are contracts", "Connect an existing inventory through External Storage or an Interface. Refined Storage owns storage and requests; Oritech pipes own machine-side movement.", "storage_core"),
            ("first_pattern", "First Pattern", "Request, do not handcraft", "Encode and successfully request a simple crafting pattern through an Autocrafter.", "external_boundaries"),
            ("factory_request", "Factory Request", "Let Oritech do the processing", "Request a component through Refined Storage, process it in an Oritech machine, and return it through Oritech pipes and a dedicated Interface.", "first_pattern"),
            ("respect_the_locks", "Respect the Locks", "Convenience has edges", "Confirm that wireless access, Constructors, Destructors, and remote network links remain unavailable in survival.", "factory_request"),
        ],
    ),
    (
        "supertech",
        "Supertech",
        "minecraft:nether_star",
        [
            ("nuclear_scale", "Nuclear Scale", "Power for the final workshop", "Bring Oritech's reactor-scale generation online with safe inputs, outputs, shutdown behavior, and restart recovery.", ("storage/respect_the_locks", "distributed_works/drone_route")),
            ("particle_products", "Particle Products", "Make the rare repeatable", "Operate the particle accelerator and turn its products into a documented, repeatable production chain.", "nuclear_scale"),
            ("renewable_supertech", "Renewable Supertech", "Remove the heroic hand-feed", "Make the critical supertech inputs renewable or sustainably supplied from distributed works.", "particle_products"),
            ("survive_a_restart", "Survive a Restart", "Prove the whole factory", "Restart at full scale and verify power, processing, storage requests, drones, and remote sites without duplication or loss.", "renewable_supertech"),
        ],
    ),
    (
        "signal_core",
        "The Signal Core",
        "minecraft:beacon",
        [
            ("project_charter", "Project Charter", "Define the megaproject", "Choose a visible site and define the optional Signal Core as a demonstration of renewable supply, nuclear-scale power, particle products, autocrafting, and interdimensional logistics.", "supertech/survive_a_restart"),
            ("production_cells", "Production Cells", "Build for continuous operation", "Dedicate production cells to the Core's major material families. Give each cell monitoring, buffers, a safe stopped state, and a coherent Oritech-and-Rechiseled industrial identity.", "project_charter"),
            ("interdimensional_supply", "Interdimensional Supply", "Tune every signal", "Supply the project from more than one dimension without Refined Storage wireless or remote-network devices.", "production_cells"),
            ("continuous_run", "Continuous Run", "The atelier answers", "Run the complete Signal Core supply chain through a full operating cycle and restart. Record bottlenecks before calling the workshop complete.", "interdimensional_supply"),
        ],
    ),
]


def quest_id(chapter: str, slug: str) -> str:
    return f"simplyquests:{GROUP}/{chapter}/{slug}"


def dependency_id(chapter: str, dependency: str) -> str:
    if "/" in dependency:
        dependency_chapter, dependency_slug = dependency.split("/", 1)
    else:
        dependency_chapter, dependency_slug = chapter, dependency
    return quest_id(dependency_chapter, dependency_slug)


def dependency_ids(chapter: str, dependencies: str | tuple[str, ...] | None) -> list[str]:
    if dependencies is None:
        return []
    if isinstance(dependencies, str):
        dependencies = (dependencies,)
    return [dependency_id(chapter, dependency) for dependency in dependencies]


def make_quest(chapter: str, index: int, data: tuple) -> dict:
    slug, title, subtitle, description, dependency = data
    identifier = quest_id(chapter, slug)
    return {
        "id": identifier,
        "chapterName": chapter,
        "title": title,
        "subTitle": subtitle,
        "description": description,
        "x": float(index * 128),
        "y": float(32 if index % 2 else 0),
        "shape": "GEAR",
        "size": 24.0,
        "settings": {
            "isOptional": f"{chapter}/{slug}" in OPTIONAL_QUESTS,
            "isRepeatable": False,
            "useTaskIcon": False,
        },
        "dependencies": dependency_ids(chapter, dependency),
        "tasks": [
            {
                "id": f"{identifier}/acknowledge",
                "type": "checkbox",
                "targetId": "",
                "name": f"Mark complete: {title}",
                "requiredAmount": 1,
                "optional": False,
                "repeatable": False,
                "consume": False,
                "targetX": 0,
                "targetY": 0,
                "targetZ": 0,
                "isIcon": True,
            }
        ],
        "rewards": [],
        "lockedBy": "",
        "logo": QUEST_ICONS[f"{chapter}/{slug}"],
    }


def render() -> dict[Path, str]:
    chapters_dir = OUTPUT / "chapters"
    outputs = {}
    chapter_names = []
    for order, (name, title, icon, quests) in enumerate(CHAPTERS):
        chapter_names.append(name)
        chapter = {
            "group": GROUP,
            "groupOrder": 0,
            "groupColor": GROUP_COLOR,
            "name": name,
            "title": title,
            "chapterOrder": order,
            "icon": icon,
            "quests": [make_quest(name, index, quest) for index, quest in enumerate(quests)],
            "canvasTexts": [],
            "canvasImages": [],
            "offsetX": 0.0,
            "offsetY": 0.0,
            "zoom": 0.85,
        }
        outputs[chapters_dir / f"{name}.json"] = json.dumps(chapter, indent=2) + "\n"

    groups = {
        "groups": [
            {
                "name": GROUP,
                "title": "Signal Atelier",
                "color": GROUP_COLOR,
                "order": 0,
                "expanded": True,
                "chapters": chapter_names,
            }
        ],
        "rootChapters": [],
    }
    outputs[OUTPUT / "groups.json"] = json.dumps(groups, indent=2) + "\n"
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if quest JSON is stale")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    outputs = render()
    if args.check:
        existing = set(OUTPUT.glob("*.json")) | set((OUTPUT / "chapters").glob("*.json"))
        stale = [
            path
            for path, expected in outputs.items()
            if not path.exists() or path.read_text() != expected
        ]
        stale.extend(sorted(existing - outputs.keys()))
        if stale:
            for path in stale:
                print(f"Generated quest file is stale: {path.relative_to(ROOT)}", file=sys.stderr)
            print("Run scripts/build_quests.py", file=sys.stderr)
            return 1
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
