# Progression test plan

Use a fresh world for the first complete pass. Record crashes, broken recipes,
missing documentation, and progression blockers before adding more mods.

## Smoke test

- Launch from a clean Prism import using Java 25.
- Create and re-enter a new survival world.
- Confirm Oritech world generation is present.
- Confirm JEI shows Oritech recipes and Oracle Index opens its documentation.
- Connect a second client or dedicated server before calling the pack
  multiplayer-capable.

## Progression test

- Establish basic power.
- Assemble the first processing machines.
- Produce steel and the principal intermediate alloys.
- Exercise item, fluid, and energy transport.
- Test machine addons and multiblock reconstruction after a restart.
- Process ores through each intended tier.
- Test oil, farming automation, lasers, drones, and remote resource handling.
- Reach the reactor, particle accelerator, and other endgame systems.
- Restart the game and server at meaningful milestones to expose persistence
  faults.

## Storage integration test

- Confirm locked Refined Storage devices have no survival recipes and are
  hidden from normal recipe discovery.
- Power Refined Storage exclusively through Oritech generation.
- Verify normal crafting and recursive request-based autocrafting.
- Feed an Oritech machine from an RS Autocrafter and return its products using
  Oritech pipes through a dedicated RS Interface.
- Confirm Oritech pipes and drones remain necessary for world interaction and
  remote sites.
- Verify backpack capacity stops at the configured iron tier.
- Confirm backpacks cannot contain backpacks or filled shulker boxes.
- Test backpack contents across death, logout, server restart, placement, and
  break-and-pickup cycles.

## Recovery and quality-of-life test

- Verify GraveStone recovery in lava, the void, Nether, End, and around
  Oritech machines.
- Confirm only the owner can initially open a grave and that ownership remains
  correct after a server restart.
- Confirm equipped backpacks and their contents move into and out of graves
  without duplication or loss.
- Verify Jade identifies Oritech machines without exposing unintended hidden
  information.
- Confirm AppleSkin, Mouse Tweaks, and Better Advancements remain client-side
  conveniences and do not alter progression.
- Confirm Xaero's World Map reveals only explored terrain.
- Verify entity tracking and map teleportation are disabled; test player
  markers separately if World Map supports them without the Minimap.

## XP and enchanting test

- Confirm an XP Tome stores no more than 1,395 XP and cannot duplicate XP
  through death, graves, logout, or server restart.
- Verify Tax Free Levels charges the same raw XP for an operation regardless
  of the player's starting level.
- Confirm the vanilla anvil ceiling remains enabled and item renaming costs one
  level.
- Verify Enchantment Descriptions works without requiring Prickle on a
  dedicated server.
- Confirm no installed feature extracts, selects, rerolls, or duplicates
  enchantments.

## Planned integration tests

- Benchmark Lithium and ImmediatelyFast separately before combining them with
  the existing performance stack.
- Confirm Dynamic FPS performs no runtime dependency download and resumes
  cleanly after the game regains focus.
- Test Iris and Complementary Reimagined around Oritech animations, emissive
  textures, transparent blocks, portals, and Xaero's map; shaders must remain
  disabled by default.
- Test LambDynamicLights with Oritech items and Sodium after resolving its
  NeoForge dependency metadata.
- Verify Rechiseled connected textures, stairs, slabs, recipes, and restart
  persistence without adding unintended storage or progression features.
- Test Sound Physics Remastered in factories and tunnels and confirm it can be
  disabled without affecting a world or server connection.
- Confirm only the single-chunk loader is craftable, respects placement limits,
  and behaves safely while owners are offline.
- Verify Simply Quests progress survives logout, server restart, pack update,
  team changes, and restoration from backup; quests must never gate recipes.
- Complete the provisional Signal Core production chain without relying on
  locked Refined Storage or chunk-loader features.
- Verify Simple Menu shows the Signal Atelier name and pack version in the
  window title and renders the custom icon correctly at 16x16 and 32x32.
- Confirm the title logo scales cleanly across GUI scales and window sizes.
- Confirm Realms is hidden while Singleplayer, Multiplayer, Mods, Options, and
  Quit remain accessible.
- Verify the NeoForge experimental warning remains visible and no promotional
  or external-link buttons appear.
- Confirm custom splash text loads while the vanilla panorama and loading
  screen remain unchanged.

## Upgrade test

- Copy the world before changing Oritech or NeoForge.
- Launch the copy and inspect machines, inventories, fluids, energy, pipes,
  drones, augmentations, and world-generated resource nodes.
- Keep the prior pack version available until the upgraded copy passes.
