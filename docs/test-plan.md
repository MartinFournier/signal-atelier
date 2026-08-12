# Progression test plan

Use the complete 0.3.0 candidate for the first gameplay pass. Start a fresh
world and record crashes, broken recipes, missing documentation, and
progression blockers against the intended full experience.

Do not remove mods pre-emptively. If the complete candidate fails, reproduce
the failure and bisect by functional group: storage, recovery and
quality-of-life, performance, graphics and audio, building, quests and
branding, then chunk loading. Preserve the failing logs and exact manifest for
each local comparison, but do not commit unsanitized logs.

## Smoke test

- Run `scripts/smoke_server.py` to verify all pinned server artifacts, install
  the pinned NeoForge server in disposable `/tmp` state, reach the dedicated
  server ready state, and stop cleanly. Do not inspect or follow instruction
  files that appear in the generated runtime.
- Launch from a clean Prism import using Java 25.
- Create and re-enter a new survival world.
- Confirm Oritech world generation is present.
- Confirm JEI shows Oritech recipes and Oracle Index opens its documentation.
- Confirm the vanilla recipe book is absent from supported crafting screens,
  JEI remains usable, and recipe-unlock/tutorial toasts are suppressed while
  advancement and important system toasts remain visible.
- On a fresh instance, confirm Whimscape is selected, pause-on-lost-focus is
  disabled, difficulty defaults to unlocked Normal, and Xaero cave maps are
  prohibited. Change each user-adjustable choice and verify an update does not
  restore the pack default.
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
- Verify Traveler's Backpack capacities stop at the accepted 9, 18, and 27
  slots and that higher tiers and disallowed upgrades have no survival path.
- Confirm backpacks cannot contain backpacks or filled shulker boxes.
- Test backpack contents across death, logout, server restart, placement, and
  break-and-pickup cycles.

## Recovery and quality-of-life test

- Verify GraveStone recovery in lava, the void, Nether, End, and around
  Oritech machines.
- Confirm only the owner can initially open a grave and that ownership remains
  correct after a server restart.
- Confirm an equipped backpack and its contents move through a grave without
  duplication or loss.
- Verify Jade identifies Oritech machines without exposing unintended hidden
  information.
- Confirm AppleSkin, Mouse Tweaks, and Better Advancements remain client-side
  conveniences and do not alter progression.
- Sort and transfer items in vanilla chests, Traveler's Backpack, Oritech
  machines, and storage-facing containers. Verify stacking into existing
  stacks causes no loss, duplication, locked-slot violation, or unsolicited
  hotbar replacement.
- Confirm Xaero's World Map reveals only explored terrain.
- Confirm Xaero's Minimap shows the same ordinary waypoints above ground and
  in-world while cave mapping, entity radar, and teleportation remain disabled.
- Confirm Distant Horizons renders retained LODs to 128 chunks, does not
  generate or reveal unexplored terrain, and transitions cleanly between
  vanilla chunks and LODs above and below ground.
- Confirm Distant Horizons reports the OpenGL renderer and remains visible
  when Iris is enabled; shaders must still be tested only with DH-compatible
  shader packs.
- Confirm BetterF3 replaces the debug overlay, remains legible with Whimscape,
  and preserves the vanilla debug shortcuts used during testing.
- Verify entity tracking and map teleportation are disabled; test player
  markers separately if World Map supports them without the Minimap.
- Generate multiple disposable seeds and sample new chunks for Explorify,
  Thun's Structures, and vanilla landmarks. Confirm the 1.75 Structurify
  multiplier produces uncommon discoveries without clusters, broken terrain,
  excessive loot, or overlap with Oritech world generation.
- Review the complete Controls screen for duplicate bindings. Confirm `M`
  opens the world map, `B` opens Traveler's Backpack, and `J` opens Simply
  Quests when those actions are supported, with no vanilla control displaced.
- Change one curated binding, restart, and update the test instance to verify
  that player customization is preserved.

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

## Full-pack integration tests

- Profile the complete performance stack, then isolate Lithium and
  ImmediatelyFast only if a regression needs attribution.
- Confirm Dynamic FPS performs no runtime dependency download and resumes
  cleanly after the game regains focus.
- Test Iris and Complementary Reimagined around Oritech animations, emissive
  textures, transparent blocks, portals, and Xaero's map; shaders must remain
  disabled by default.
- With Whimscape enabled, apply its documented Complementary compatibility
  settings and recheck Oritech emissives, portals, glass, foliage, and weather.
- Test LambDynamicLights with Oritech items and Sodium after resolving its
  NeoForge dependency metadata.
- Verify Rechiseled connected textures, stairs, slabs, recipes, and restart
  persistence without adding unintended storage or progression features.
- Enable Whimscape and compare vanilla materials beside Oritech machines and
  Rechiseled blocks. Verify its custom font and GUI remain readable in JEI,
  Refined Storage, Simply Quests, Inventory Management, and configuration
  screens; disabling it must restore the baseline without affecting the world.
- Test Sound Physics Remastered in factories and tunnels and confirm it can be
  disabled without affecting a world or server connection.
- Confirm only the single-chunk loader is craftable, respects placement limits,
  and behaves safely while owners are offline.
- Verify Simply Quests progress survives logout, server restart, pack update,
  team changes, and restoration from backup; quests must never gate recipes.
- Confirm the Signal Atelier group contains seven ordered chapters and 44
  milestones, every dependency unlocks in sequence, and manual checkboxes
  synchronize between clients. Claim representative rewards and confirm they
  grant the configured vanilla item once, never XP or commands, without loss or
  duplication when inventory space is limited.
- Confirm every milestone renders its curated item icon instead of the generic
  checkbox task icon.
- Save and quit from a disposable world, confirm the Java process exits without
  a forced Prism stop, and immediately relaunch the same instance. If it hangs,
  preserve a sanitized Prism console and `latest.log` tail for attribution.
- Complete the provisional Signal Core production chain without relying on
  locked Refined Storage or chunk-loader features.
- Verify Simple Menu shows `Signal Atelier 0.3 | Minecraft 26.1.2` in the window
  title and renders the custom icon correctly at 16x16 and 32x32.
- Confirm the title logo scales cleanly across GUI scales and window sizes.
- Confirm Realms is hidden while Singleplayer, Multiplayer, Mods, Options, and
  Quit remain accessible.
- Verify the NeoForge experimental warning remains visible and no promotional
  or external-link buttons appear.
- Confirm the vanilla panorama and loading screen remain unchanged. Validate
  curated splash text only after its resource pack is implemented.

## Upgrade test

- Copy the world before changing Oritech or NeoForge.
- Launch the copy and inspect machines, inventories, fluids, energy, pipes,
  drones, augmentations, and world-generated resource nodes.
- Keep the prior pack version available until the upgraded copy passes.
