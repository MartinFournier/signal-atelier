import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
CONFIG = ROOT / "overrides/config"


def load_json(relative: str) -> dict:
    return json.loads((CONFIG / relative).read_text())


def load_toml(relative: str) -> dict:
    return tomllib.loads((CONFIG / relative).read_text())


class PackPolicyTests(unittest.TestCase):
    def test_chunk_loading_is_physically_limited(self):
        config = load_toml("chunkloaders.toml")
        limits = config["Limitations"]
        self.assertEqual(4, limits["maxLoadedChunksPerPlayer"])
        self.assertEqual(10080, limits["inactivityTimeout"])
        self.assertFalse(limits["allowLegacyLoadedChunks"])
        self.assertFalse(limits["canPlayersUseMap"])
        self.assertEqual(
            {1},
            {
                value
                for key, value in config["General"].items()
                if key.endswith("ChunkLoaderRadius")
            },
        )

    def test_backpacks_remain_bounded_field_storage(self):
        common = load_toml("travelersbackpack-common.toml")["common"]
        self.assertFalse(common["enableLoot"])
        self.assertFalse(common["enableVillagerTrade"])

        server = load_toml("travelersbackpack-server.toml")["server"]
        settings = server["backpackSettings"]
        self.assertFalse(settings["allowShulkerBoxes"])
        self.assertFalse(settings["allowToolSwapping"])
        self.assertTrue(settings["preventMultiplePlayersAccess"])
        self.assertTrue(settings["quickSleepingBag"])
        self.assertFalse(settings["enableSleepingBagSpawnPoint"])
        self.assertEqual(
            [9, 18, 27, 27, 27],
            [
                settings[f"{tier}TierBackpack"]["inventorySlotCount"]
                for tier in ("leather", "iron", "gold", "diamond", "netherite")
            ],
        )
        for tier in ("leather", "iron", "gold", "diamond", "netherite"):
            self.assertEqual(0, settings[f"{tier}TierBackpack"]["upgradeSlotCount"])

        upgrades = server["backpackUpgrades"]
        self.assertTrue(upgrades["enableSleepingBag"])
        self.assertTrue(upgrades["enableTanksUpgrade"])
        for key, value in upgrades.items():
            if key.startswith("enable") and key not in {
                "enableSleepingBag",
                "enableTanksUpgrade",
            }:
                self.assertFalse(value, key)
        for section, values in upgrades.items():
            if section.endswith("UpgradeSettings"):
                enable_key = next(key for key in values if key.startswith("enable"))
                self.assertFalse(values[enable_key], section)

        world = server["world"]
        self.assertFalse(world["spawnEntitiesWithBackpack"])
        self.assertEqual(0.0, world["chance"])
        self.assertFalse(server["backpackAbilities"]["enableBackpackAbilities"])

    def test_backpack_progression_and_jei_visibility_match_policy(self):
        recipes = CONFIG / "universaldatapack/data/travelersbackpack/recipe"
        self.assertFalse((recipes / "blank_upgrade.json").exists())
        for recipe in (
            "diamond_tier_upgrade.json",
            "netherite_tier_upgrade.json",
            "tanks_upgrade.json",
            "crafting_upgrade.json",
            "furnace_upgrade.json",
            "smoker_upgrade.json",
            "blast_furnace_upgrade.json",
            "pickup_upgrade.json",
            "magnet_upgrade.json",
            "feeding_upgrade.json",
            "refill_upgrade.json",
            "void_upgrade.json",
            "jukebox_upgrade.json",
            "lantern_upgrade.json",
        ):
            self.assertEqual({}, json.loads((recipes / recipe).read_text()))

        blacklist = load_json("defaultoptions/extra/config/jei/blacklist.json")
        self.assertEqual({"version": 2}, blacklist[0])
        hidden = {
            entry["ingredient"]["ingredient"]["id"] for entry in blacklist[1:]
        }
        self.assertNotIn("travelersbackpack:blank_upgrade", hidden)
        self.assertNotIn("travelersbackpack:iron_tier_upgrade", hidden)
        self.assertNotIn("travelersbackpack:gold_tier_upgrade", hidden)
        self.assertNotIn("travelersbackpack:backpack_tank", hidden)
        self.assertIn("travelersbackpack:diamond", hidden)
        self.assertIn("travelersbackpack:netherite", hidden)
        self.assertIn("travelersbackpack:diamond_tier_upgrade", hidden)
        self.assertIn("travelersbackpack:netherite_tier_upgrade", hidden)
        self.assertNotIn("chunkloaders:single_chunk_loader", hidden)
        self.assertTrue(
            {
                "chunkloaders:basic_chunk_loader",
                "chunkloaders:advanced_chunk_loader",
                "chunkloaders:ultimate_chunk_loader",
                "refinedstorage:constructor",
                "refinedstorage:destructor",
                "refinedstorage:network_receiver",
                "refinedstorage:network_transmitter",
                "refinedstorage:wireless_autocrafting_monitor",
                "refinedstorage:wireless_grid",
                "refinedstorage:wireless_transmitter",
            }.issubset(hidden)
        )

    def test_graves_remain_owner_restricted(self):
        config = tomllib.loads(
            (ROOT / "overrides/defaultconfigs/gravestone-server.toml").read_text()
        )
        self.assertTrue(config["only_owners_can_break"])
        self.assertFalse(config["sneak_pickup"])
        self.assertTrue(config["break_pickup"])
        self.assertFalse(config["spawn_ghost"])

    def test_xp_policy_keeps_the_vanilla_anvil_limit(self):
        config = load_json("taxfreelevels.json")
        self.assertEqual(0, config["levelBase"])
        self.assertFalse(config["removeAnvilLimit"])

    def test_dynamic_fps_disables_battery_tracking(self):
        config = load_json("dynamic_fps.json")
        self.assertTrue(config["enabled"])
        self.assertFalse(config["battery_tracker"]["enabled"])

    def test_structure_spacing_is_sparse(self):
        config = load_json("structurify.json")
        general = config["general"]
        self.assertFalse(general["disabled_all_structures"])
        self.assertTrue(general["enable_global_spacing_and_separation_modifier"])
        self.assertEqual(1.75, general["global_spacing_and_separation_modifier"])
        self.assertEqual([], config["structures"])
        self.assertEqual([], config["structure_sets"])

    def test_distant_horizons_uses_iris_compatible_renderer(self):
        config = tomllib.loads((CONFIG / "DistantHorizons.toml").read_text())
        graphics = config["client"]["advanced"]["graphics"]
        self.assertEqual("OPEN_GL", graphics["experimental"]["renderingEngine"])

    def test_first_install_defaults_are_narrow(self):
        config = tomllib.loads((CONFIG / "defaultoptions-common.toml").read_text())
        self.assertEqual("NORMAL", config["defaultDifficulty"])
        self.assertFalse(config["lockDifficulty"])
        self.assertEqual(
            ["Whimscape_26.1-26.2_r1.zip"],
            config["defaultResourcePacks"],
        )
        options = (CONFIG / "defaultoptions/options.txt").read_text().splitlines()
        self.assertEqual(["pauseOnLostFocus:false"], options)
        xaero = (CONFIG / "defaultoptions/extra/config/xaeroworldmap.txt").read_text()
        self.assertEqual("caveMapsAllowed:false\n", xaero)
        minimap = dict(
            line.split(":", 1)
            for line in (
                CONFIG / "defaultoptions/extra/config/xaerominimap.txt"
            ).read_text().splitlines()
        )
        self.assertEqual("true", minimap["minimap"])
        self.assertEqual("true", minimap["showWaypoints"])
        self.assertEqual("true", minimap["showIngameWaypoints"])
        self.assertEqual("0", minimap["caveMaps"])
        self.assertEqual("false", minimap["entityRadar"])
        self.assertEqual("false", minimap["allowWrongWorldTeleportation"])
        common = (CONFIG / "xaeroworldmap-common.txt").read_text()
        self.assertEqual("allowCaveModeOnServer:false\n", common)

    def test_betterf3_first_install_layout_is_compact(self):
        config = tomllib.loads(
            (
                CONFIG / "defaultoptions/extra/config/betterf3.toml"
            ).read_text()
        )
        self.assertEqual(0.8, config["general"]["fontScale"])
        self.assertTrue(config["general"]["performance_optimizations"])
        self.assertTrue(config["general"]["hide_bossbar"])
        self.assertEqual(
            ["minecraft", "fps", "coords", "graphics", "empty"],
            [module["name"] for module in config["modules_left"]],
        )
        self.assertEqual(
            ["system"],
            [module["name"] for module in config["modules_right"]],
        )

    def test_distant_horizons_uses_effective_client_defaults(self):
        config = tomllib.loads((CONFIG / "DistantHorizons.toml").read_text())
        self.assertFalse(config["client"]["advanced"]["autoUpdater"]["enableAutoUpdater"])
        self.assertEqual(
            "OPEN_GL",
            config["client"]["advanced"]["graphics"]["experimental"][
                "renderingEngine"
            ],
        )
        self.assertEqual(
            128,
            config["client"]["advanced"]["graphics"]["quality"][
                "lodChunkRenderDistanceRadius"
            ],
        )
        self.assertFalse(config["common"]["worldGenerator"]["enableDistantGeneration"])

    def test_minimap_starts_on_right(self):
        hud = (CONFIG / "defaultoptions/extra/config/xaerohud.txt").read_text()
        self.assertIn("id=xaerominimap:minimap", hud)
        self.assertIn("fromRight=true", hud)

    def test_jade_does_not_duplicate_item_provenance(self):
        jade = load_json("defaultoptions/extra/config/jade/jade.json")
        self.assertFalse(jade["general"]["itemModNameTooltip"])
        self.assertEqual("ON", jade["plugin"]["jade"]["mod_name"])

    def test_menu_keeps_required_controls_and_warning(self):
        config = load_json("simplemenu.json5")
        manifest = json.loads((ROOT / "modrinth.index.json").read_text())
        pack_version = manifest["versionId"].split(".")
        self.assertGreaterEqual(len(pack_version), 2)
        pack_line = ".".join(pack_version[:2])
        expected_title = (
            f"{manifest['name']} {pack_line} | "
            f"Minecraft {manifest['dependencies']['minecraft']}"
        )
        self.assertEqual(
            expected_title,
            config["customWindowTitle"],
        )
        self.assertTrue(config["setCustomWindowTitle"])
        self.assertTrue(config["setCustomWindowIcon"])
        self.assertTrue(config["replaceMainMenuLogo"])
        self.assertTrue(config["replaceMainMenuEditionLogo"])
        self.assertTrue(config["hideSplashText"])
        self.assertTrue((CONFIG / "simplemenu/logo/edition.png").is_file())
        self.assertFalse(config["setCustomBackground"])
        self.assertTrue(config["hideMinecraftRealmsButton"])
        self.assertFalse(config["enableServerPromoButton"])
        self.assertFalse(config["removeExperimentalModLoaderText"])


if __name__ == "__main__":
    unittest.main()
