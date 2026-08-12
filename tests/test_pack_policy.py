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
        self.assertFalse(config["setCustomBackground"])
        self.assertTrue(config["hideMinecraftRealmsButton"])
        self.assertFalse(config["enableServerPromoButton"])
        self.assertFalse(config["removeExperimentalModLoaderText"])


if __name__ == "__main__":
    unittest.main()
