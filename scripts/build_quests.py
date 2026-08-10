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
    "signal_core/monitor_the_core",
    "signal_core/interdimensional_supply",
    "signal_core/continuous_run",
}
QUEST_ICONS = {
    "orientation/read_the_brief": "minecraft:book",
    "orientation/survey_a_site": "minecraft:compass",
    "orientation/mark_the_baseline": "minecraft:chest",
    "power/first_generation": "minecraft:redstone_torch",
    "power/distribution_bus": "minecraft:redstone",
    "power/buffer_and_measure": "minecraft:comparator",
    "power/safe_shutdown": "minecraft:lever",
    "power/renewable_baseline": "minecraft:daylight_detector",
    "industry/first_machine": "minecraft:blast_furnace",
    "industry/ore_processing": "minecraft:raw_iron",
    "industry/processing_line": "minecraft:furnace",
    "industry/principal_alloys": "minecraft:iron_ingot",
    "industry/machine_addons": "minecraft:piston",
    "industry/fluids_and_oil": "minecraft:bucket",
    "industry/byproducts_and_overflow": "minecraft:barrel",
    "industry/automated_harvest": "minecraft:hay_block",
    "industry/rebuild_after_restart": "minecraft:observer",
    "distributed_works/pipes_first": "minecraft:hopper",
    "distributed_works/separate_networks": "minecraft:glass_bottle",
    "distributed_works/route_control": "minecraft:lever",
    "distributed_works/laser_workcell": "minecraft:target",
    "distributed_works/field_recovery_drill": "minecraft:recovery_compass",
    "distributed_works/remote_site": "minecraft:minecart",
    "distributed_works/drone_route": "minecraft:phantom_membrane",
    "distributed_works/one_loaded_chunk": "minecraft:lodestone",
    "storage/storage_core": "minecraft:chest",
    "storage/first_disk": "minecraft:map",
    "storage/external_boundaries": "minecraft:barrel",
    "storage/first_pattern": "minecraft:crafting_table",
    "storage/crafting_capacity": "minecraft:repeater",
    "storage/factory_request": "minecraft:hopper",
    "storage/respect_the_locks": "minecraft:barrier",
    "supertech/reactor_supply": "minecraft:hopper",
    "supertech/reactor_safety": "minecraft:shield",
    "supertech/nuclear_scale": "minecraft:beacon",
    "supertech/accelerator_inputs": "minecraft:blaze_rod",
    "supertech/particle_products": "minecraft:end_crystal",
    "supertech/renewable_supertech": "minecraft:blaze_powder",
    "supertech/survive_a_restart": "minecraft:clock",
    "signal_core/project_charter": "minecraft:writable_book",
    "signal_core/production_cells": "minecraft:copper_block",
    "signal_core/monitor_the_core": "minecraft:comparator",
    "signal_core/interdimensional_supply": "minecraft:ender_eye",
    "signal_core/continuous_run": "minecraft:nether_star",
}
QUEST_REWARDS = {
    "orientation/read_the_brief": ("minecraft:paper", 4),
    "orientation/survey_a_site": ("minecraft:torch", 8),
    "orientation/mark_the_baseline": ("minecraft:bread", 4),
    "power/first_generation": ("minecraft:lantern", 2),
    "power/buffer_and_measure": ("minecraft:oak_sign", 4),
    "power/renewable_baseline": ("minecraft:baked_potato", 6),
    "industry/processing_line": ("minecraft:scaffolding", 8),
    "industry/principal_alloys": ("minecraft:chest", 2),
    "industry/fluids_and_oil": ("minecraft:glass", 8),
    "industry/rebuild_after_restart": ("minecraft:clock", 1),
    "distributed_works/pipes_first": ("minecraft:ladder", 8),
    "distributed_works/remote_site": ("minecraft:cooked_beef", 4),
    "distributed_works/drone_route": ("minecraft:rail", 8),
    "distributed_works/one_loaded_chunk": ("minecraft:compass", 1),
    "storage/storage_core": ("minecraft:barrel", 2),
    "storage/external_boundaries": ("minecraft:item_frame", 4),
    "storage/first_pattern": ("minecraft:crafting_table", 1),
    "storage/factory_request": ("minecraft:firework_rocket", 4),
    "storage/respect_the_locks": ("minecraft:iron_bars", 8),
    "supertech/nuclear_scale": ("minecraft:redstone_lamp", 2),
    "supertech/particle_products": ("minecraft:tinted_glass", 4),
    "supertech/renewable_supertech": ("minecraft:honey_bottle", 4),
    "supertech/survive_a_restart": ("minecraft:firework_rocket", 8),
    "signal_core/project_charter": ("minecraft:writable_book", 1),
    "signal_core/production_cells": ("minecraft:copper_grate", 8),
    "signal_core/interdimensional_supply": ("minecraft:ender_chest", 1),
    "signal_core/continuous_run": ("minecraft:cake", 1),
}

CHAPTERS = [
    (
        "orientation",
        "Orientation",
        "minecraft:compass",
        [
            ("read_the_brief", "Workshop Brief", "Know the tools and their boundaries", "Use JEI for recipes and the Oracle Index for Oritech details; this notebook explains how the pack fits together. Oritech owns power, processing, transport, and world interaction. Refined Storage is deliberately limited to storage, requests, and autocrafting. Quests offer minor workshop supplies, never recipe gates or progression-critical rewards.", None),
            ("survey_a_site", "Survey a Site", "Explore, then leave room to grow", "Explore with Xaero's surface map and mark an expandable workshop using an ordinary waypoint. The map records chunks loaded by your client; cave maps, teleportation, and entity radar are disabled. Explorify and Thun's Structures provide occasional landmarks, not a checklist to clear.", "read_the_brief"),
            ("mark_the_baseline", "Mark the Baseline", "Protect the experiment", "Before building, confirm Java 25, 4–6 GiB of memory, and a recoverable backup outside the Prism instance. Treat the world as disposable while Oritech 2 and NeoForge remain experimental. Save and quit once; the Java process must exit cleanly before you trust the instance.", "survey_a_site"),
        ],
    ),
    (
        "power",
        "Power",
        "minecraft:redstone",
        [
            ("first_generation", "First Generation", "Make power visible", "Use the Oracle Index and JEI to choose an Oritech generator, then verify energy reaches a machine. Prefer a measured, expandable layout over a temporary cable tangle.", "orientation/mark_the_baseline"),
            ("distribution_bus", "Distribution Bus", "Build a legible power backbone", "Route Oritech energy through a deliberate main line with room for branches. Label generation, storage, and machine connections so later faults can be isolated.", "first_generation"),
            ("buffer_and_measure", "Buffer and Measure", "Understand demand", "Add energy storage or monitoring, then observe idle and working demand. Leave capacity for the next processing line.", "distribution_bus"),
            ("safe_shutdown", "Safe Shutdown", "A stopped factory must stay safe", "Test a controlled shutdown under load. Machines should stop without losing inputs, spilling outputs, or requiring cables to be broken.", "buffer_and_measure"),
            ("renewable_baseline", "Renewable Baseline", "Keep the workshop alive", "Establish a renewable or continuously supplied generation path before scaling automation.", "safe_shutdown"),
        ],
    ),
    (
        "industry",
        "Industry",
        "minecraft:blast_furnace",
        [
            ("first_machine", "First Machine", "Learn one process end to end", "Build and power a basic Oritech processing machine. Use JEI and the Oracle Index to identify its recipe, energy demand, inputs, and outputs before connecting automation.", "power/renewable_baseline"),
            ("ore_processing", "Ore Processing", "Choose a repeatable resource path", "Process a batch of raw ore through Oritech and compare input, output, energy use, and time with the vanilla route. Keep the result measurable rather than chasing every possible multiplier immediately.", "first_machine"),
            ("processing_line", "Processing Line", "From input to product", "Build a repeatable Oritech processing line with explicit inputs, outputs, and overflow handling. Inventory Management may sort and transfer deliberately, but it must not become hidden factory automation.", "ore_processing"),
            ("principal_alloys", "Principal Alloys", "Stock the intermediates", "Use the Oracle Index and JEI to identify Oritech's recurring alloys and components, then automate them instead of crafting each machine ad hoc.", "processing_line"),
            ("machine_addons", "Machine Addons", "Tune a measured process", "Install an Oritech machine addon or upgrade and compare throughput, energy demand, and operating behavior before and after. Keep the change only if the surrounding power and logistics can support it.", "principal_alloys"),
            ("fluids_and_oil", "Fluids and Oil", "Separate the networks", "Process fluids through dedicated, labeled routes. Confirm that shutdown and restart do not strand or mix contents.", "machine_addons"),
            ("byproducts_and_overflow", "Byproducts and Overflow", "Plan for the output you did not request", "Give secondary outputs and full inventories an explicit destination. Test the line with its preferred output blocked and confirm it stalls safely without voiding or scattering materials.", "fluids_and_oil"),
            ("automated_harvest", "Automated Harvest", "Make one renewable input dependable", "Build an Oritech farming loop with a renewable source, controlled working area, collection, and overflow handling. Confirm it can stop safely when storage fills.", "byproducts_and_overflow"),
            ("rebuild_after_restart", "Rebuild After Restart", "Persistence is part of the machine", "Save and quit, confirm Java exits cleanly, then restart the game or server. Verify that multiblocks, inventories, fluids, and energy reconnect without loss or duplication.", "automated_harvest"),
        ],
    ),
    (
        "distributed_works",
        "Distributed Works",
        "minecraft:rail",
        [
            ("pipes_first", "Pipes First", "Local logistics belong to Oritech", "Move items, fluids, and energy with Oritech infrastructure before introducing centralized storage.", "industry/rebuild_after_restart"),
            ("separate_networks", "Separate the Networks", "Items, fluids, and energy have different jobs", "Build and label separate Oritech routes for items, fluids, and energy. Verify each route moves only its intended resource and remains understandable at crossings.", "pipes_first"),
            ("route_control", "Route Control", "Direct traffic deliberately", "Use Oritech filtering or routing controls to send one input to the correct destination and prevent outputs from feeding backward. Test both normal flow and a full destination.", "separate_networks"),
            ("laser_workcell", "Laser Workcell", "Control world interaction", "Build a contained Oritech laser or world-interaction workcell. Mark its operating area, test its stop control, and confirm it cannot reach unrelated machines, storage, or player routes.", "route_control"),
            ("field_recovery_drill", "Field Recovery Drill", "Prove the expedition kit before relying on it", "Store XP in an XP Tome carried by an equipped Traveler's Backpack. In a disposable death test, confirm GraveStone returns the backpack, contents, and XP without loss or duplication.", "laser_workcell"),
            ("remote_site", "Remote Site", "Establish a recoverable outpost", "Carry the proven field kit to an outpost beyond the workshop, mark it with an ordinary Xaero waypoint, and provide labeled storage plus a safe stopped state before adding automation.", "field_recovery_drill"),
            ("drone_route", "Drone Route", "Cross the difficult gap", "Use Oritech drones or another Oritech-native solution for world interaction and long-distance logistics; Refined Storage must not replace the route.", "remote_site"),
            ("one_loaded_chunk", "One Loaded Chunk", "Spend persistence carefully", "Optionally place only the single-chunk loader at a proven remote site. Confirm ownership, the offline timeout, and the four-chunk-per-player limit; no factory should require it to remain safe.", "drone_route"),
        ],
    ),
    (
        "storage",
        "Storage and Requests",
        "minecraft:chest",
        [
            ("storage_core", "Storage Core", "Centralize without replacing the factory", "Build a Refined Storage Controller, Grid, Drive, and initial disk, powered by Oritech. Use Inventory Management only for deliberate chest cleanup; Refined Storage becomes the searchable request layer.", "distributed_works/pipes_first"),
            ("first_disk", "First Disk", "Move storage without losing the inventory model", "Install an initial storage disk and move a controlled sample into the network. Confirm the Grid reports the expected counts before migrating bulk materials.", "storage_core"),
            ("external_boundaries", "External Boundaries", "Interfaces are contracts", "Connect an existing inventory through External Storage or an Interface. Refined Storage owns storage and requests; Oritech pipes own machine-side movement.", "first_disk"),
            ("first_pattern", "First Pattern", "Request, do not handcraft", "Encode and successfully request a simple crafting pattern through an Autocrafter.", "external_boundaries"),
            ("crafting_capacity", "Crafting Capacity", "Scale one proven request path", "Add patterns and crafting capacity gradually. Test missing ingredients and nested requests, then confirm a failed request leaves stored materials intact.", "first_pattern"),
            ("factory_request", "Factory Request", "Let Oritech do the processing", "Request a component through Refined Storage, process it in an Oritech machine, and return it through Oritech pipes and a dedicated Interface.", "crafting_capacity"),
            ("respect_the_locks", "Respect the Locks", "Convenience has edges", "Confirm that Refined Storage wireless access, Constructors, Destructors, and remote network links remain unavailable in survival. If JEI shows a locked recipe or another path bypasses the boundary, stop and report it.", "factory_request"),
        ],
    ),
    (
        "supertech",
        "Supertech",
        "minecraft:nether_star",
        [
            ("reactor_supply", "Reactor Supply", "Prepare before producing power", "Build repeatable input and output routes for reactor operation before starting it. Buffers must expose shortages without making the rest of the factory unsafe.", ("storage/respect_the_locks", "distributed_works/drone_route")),
            ("reactor_safety", "Reactor Safety", "Design the stopped state first", "Establish monitoring, exclusion space, and a tested shutdown procedure. Confirm the reactor can remain stopped indefinitely without manual rescue work.", "reactor_supply"),
            ("nuclear_scale", "Nuclear Scale", "Power for the final workshop", "Bring Oritech's reactor-scale generation online with safe inputs, outputs, shutdown behavior, and restart recovery.", "reactor_safety"),
            ("accelerator_inputs", "Accelerator Inputs", "Stage the expensive experiment", "Prepare the particle accelerator's power, consumables, and output storage before its first run. Keep this supply chain independent of manual inventory shuffling.", "nuclear_scale"),
            ("particle_products", "Particle Products", "Make the rare repeatable", "Operate the particle accelerator and turn its products into a documented, repeatable production chain.", "accelerator_inputs"),
            ("renewable_supertech", "Renewable Supertech", "Remove the heroic hand-feed", "Make the critical supertech inputs renewable or sustainably supplied from distributed works.", "particle_products"),
            ("survive_a_restart", "Survive a Restart", "Prove the whole factory", "Restart at full scale and verify power, processing, storage requests, drones, and remote sites without duplication or loss.", "renewable_supertech"),
        ],
    ),
    (
        "signal_core",
        "The Signal Core",
        "minecraft:beacon",
        [
            ("project_charter", "Project Charter", "Define the optional megaproject", "Only continue if a larger project sounds fun. Choose a visible site and define the optional Signal Core as a demonstration of renewable supply, nuclear-scale power, particle products, autocrafting, and interdimensional Oritech logistics.", "supertech/survive_a_restart"),
            ("production_cells", "Production Cells", "Build for continuous operation", "Dedicate production cells to the Core's major material families. Give each cell monitoring, buffers, a safe stopped state, and a coherent Oritech-and-Rechiseled industrial identity.", "project_charter"),
            ("monitor_the_core", "Monitor the Core", "Make bottlenecks visible", "Create a central status view for power, input buffers, blocked outputs, and stopped production cells. A problem should be diagnosable without opening every machine.", "production_cells"),
            ("interdimensional_supply", "Interdimensional Supply", "Tune every signal", "Supply the project from more than one dimension without Refined Storage wireless or remote-network devices.", "monitor_the_core"),
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
    reward = QUEST_REWARDS.get(f"{chapter}/{slug}")
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
        "rewards": [] if reward is None else [
            {
                "id": f"{identifier}/reward_item",
                "type": "item",
                "item": reward[0],
                "count": reward[1],
            }
        ],
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
