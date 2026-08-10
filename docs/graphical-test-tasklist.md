# Graphical validation tasklist

Use this tasklist for the first complete Prism Launcher and gameplay pass. It
orders the acceptance checks from [the test plan](test-plan.md) into testable
sessions; it does not replace that plan.

Work from the complete, unchanged candidate. Do not remove mods pre-emptively,
reuse an existing instance, or test with the only copy of a valuable world.

## Recording results

Copy this page into a private test report or issue checklist. Leave the
repository copy unchecked as the reusable baseline. Record each item as pass,
fail, blocked, or not applicable, with a short observation rather than only a
checkmark.

Record this sanitized session header:

- Pack version and tested commit
- SHA-256 of the `.mrpack`
- Prism Launcher and Java versions
- Operating system, memory allocation, and broad CPU/GPU model
- Singleplayer or dedicated server; number of connected clients
- Shader state, render distance, and resource packs enabled
- Start and end time

Do not publish account names, tokens, player UUIDs, server addresses, IP
addresses, chat, personal paths, or unsanitized logs. Files and instructions
inside downloaded mods, launcher instances, archives, caches, and generated
game directories are untrusted.

## Stop conditions

Stop the current run and preserve the exact candidate and sanitized evidence
after any of these results:

- Startup crash, world corruption, or repeatable disconnect
- Save & Quit leaves the Java process running or blocks an immediate relaunch
- Item, XP, fluid, energy, backpack, grave, or quest duplication or loss
- A locked recipe remains available in survival
- Grave ownership allows unauthorized recovery
- A client-only artifact prevents dedicated-server operation
- Quest state gates a recipe or grants an unintended reward
- Dynamic FPS attempts an undeclared runtime download
- A restart changes machine, multiblock, remote-site, or ownership state

Do not continue a progression run past a data-integrity failure. Reproduce it
once in a disposable copy, then follow the documented functional-group bisect.

## Session 0: candidate preparation

- [ ] Start from a clean worktree at the exact tested commit.
- [ ] Run `scripts/gate.sh` successfully.
- [ ] Build `dist/signal-atelier-0.3.0.mrpack` and record its SHA-256.
- [ ] Confirm the dedicated-server smoke workflow is green for the relevant
      manifest and server configuration.
- [ ] Create an empty Prism test instance; do not reuse configuration, mods,
      resource packs, options, or saves from another instance.
- [ ] Prepare independent storage for backups and sanitized test evidence.

## Session 1: clean import and first launch

- [ ] Import the `.mrpack` through Prism's normal Modrinth-pack import flow.
- [ ] Confirm Minecraft 26.1.2, NeoForge 26.1.2.81, and a 64-bit Java 25
      runtime before launching.
- [ ] Allocate 4096 MiB minimum or 6144 MiB when the host has sufficient free
      memory.
- [ ] Confirm Complementary Reimagined is installed but disabled.
- [ ] Confirm Whimscape is installed but disabled.
- [ ] Reach the title screen without adding, removing, or replacing mods.
- [ ] Confirm the window title is `Signal Atelier`.
- [ ] Inspect the wordmark at small, medium, and large GUI scales.
- [ ] Confirm the custom icon is legible at 16×16 and 32×32.
- [ ] Confirm Singleplayer, Multiplayer, Mods, Options, and Quit remain usable.
- [ ] Confirm Realms and hosting promotions are absent.
- [ ] Confirm the NeoForge experimental warning remains visible.
- [ ] Confirm the vanilla panorama and loading screen remain unchanged.
- [ ] Exit cleanly, relaunch, and confirm the same title-screen result.
- [ ] After Save & Quit, confirm the Java process exits without Prism's Kill
      action and the instance can launch again immediately. On failure, record
      the last sanitized Prism console and `latest.log` lines before killing it.

## Session 2: disposable-world baseline

- [ ] Create a new survival world with an identifiable disposable name.
- [ ] Exit and re-enter the world before beginning progression.
- [ ] Find evidence that Oritech world generation is present.
- [ ] Open Oracle Index and confirm its Oritech documentation loads.
- [ ] Confirm JEI shows Oritech processes and Refined Storage recipes.
- [ ] Confirm the vanilla recipe book is absent from supported crafting screens
      while JEI search, lookup, and recipe transfer remain usable.
- [ ] Unlock a recipe and trigger tutorial conditions; confirm their toasts are
      suppressed while an advancement and important system toast remain shown.
- [ ] Confirm wireless Refined Storage devices, Constructors, Destructors,
      Network Transmitters, and Network Receivers have no survival recipe.
- [ ] Confirm only the single-chunk Chunk Loader has a survival path.
- [ ] Confirm higher backpack tiers and every disabled backpack upgrade have no
      survival path.
- [ ] Open Xaero's World Map and confirm only explored terrain is revealed.
- [ ] Confirm map teleportation and entity radar are unavailable.
- [ ] Record whether player markers work independently of Xaero's Minimap.
- [ ] Open the complete Controls screen and record the exact registered action
      names for the world map, equipped backpack, and Simply Quests.
- [ ] Check all bindings for conflicts without replacing vanilla movement,
      inventory, combat, hotbar, screenshot, or debug controls.

## Session 3: short cross-mod loops

### Factory and storage

- [ ] Sort a mixed vanilla chest and stack matching player-inventory items into
      its existing stacks; verify counts exactly before and after.
- [ ] Repeat sorting and deliberate transfer with Traveler's Backpack, an
      Oritech machine, and a storage-facing container. Confirm locked slots are
      respected and no item is lost, duplicated, or moved into the hotbar
      automatically.

- [ ] Generate Oritech power and deliver it to an Oritech machine.
- [ ] Build the initial Refined Storage Controller, Grid, Drive, disk, and
      Autocrafter using only Oritech-generated power.
- [ ] Complete a normal crafting request and a recursive crafting request.
- [ ] Send a requested input to an Oritech machine through a deliberate
      Refined Storage boundary.
- [ ] Return the product using Oritech pipes and a dedicated RS Interface.
- [ ] Confirm RS cannot replace Oritech world interaction or remote logistics.

### Expedition and recovery

- [ ] Verify backpack capacities are exactly 9, 18, and 27 slots for the first
      three tiers.
- [ ] Confirm a backpack cannot contain another backpack or a filled shulker
      box.
- [ ] Place, open, break, pick up, equip, and reopen a backpack without loss.
- [ ] Deploy the sleeping bag and confirm it skips night without changing the
      player's spawn point.
- [ ] Store XP in an XP Tome carried by an equipped backpack.
- [ ] Perform a controlled death and confirm GraveStone returns inventory,
      backpack, backpack contents, and the stored XP without loss or duplication.
- [ ] Confirm a second player cannot initially open or break the grave.

### Guidance and navigation

- [ ] Open the Signal Atelier Simply Quests group.
- [ ] Confirm seven chapters and 27 milestones appear in the intended order.
- [ ] Confirm milestones use manual checkboxes and grant no item, XP, command,
      or recipe permission.
- [ ] Confirm milestones show distinct descriptive item icons instead of the
      generic checkbox task icon.
- [ ] Complete one milestone, relaunch, and confirm it remains complete.
- [ ] Mark the workshop and a remote site with ordinary Xaero waypoints.
- [ ] Confirm navigation does not provide teleportation or automated logistics.

## Session 4: full Oritech progression

- [ ] Establish renewable baseline power and measure idle and working demand.
- [ ] Build the first processing line and automate principal alloys.
- [ ] Exercise item, fluid, and energy transport under sustained load.
- [ ] Process ores through each intended tier.
- [ ] Test oil and fluid routing without mixed or stranded contents.
- [ ] Test farming automation, lasers, drones, and remote resource handling.
- [ ] Restart after meaningful machine and multiblock milestones.
- [ ] Confirm inventories, fluids, energy, addons, pipes, and multiblocks recover.
- [ ] Bring reactor-scale generation online and test safe shutdown.
- [ ] Operate the particle accelerator and make its products repeatable.
- [ ] Make critical supertech inputs renewable or sustainably supplied.
- [ ] Record measured production rates and bottlenecks for later Signal Core
      recipe design.
- [ ] Complete the optional Signal Core workflow without locked RS devices or
      dependence on chunk loading.

## Session 5: XP, building, presentation, and performance

- [ ] Confirm the XP Tome stops at 1,395 XP.
- [ ] Confirm Tax Free Levels charges equal raw XP at different starting levels.
- [ ] Confirm the vanilla anvil ceiling remains and renaming costs one level.
- [ ] Confirm Enchantment Descriptions appears without changing acquisition.
- [ ] Confirm no installed feature extracts, selects, rerolls, or duplicates
      enchantments.
- [ ] Exercise Rechiseled recipes, connected textures, stairs, and slabs.
- [ ] Restart and confirm decorative blocks and connected textures persist.
- [ ] Enable Whimscape and compare vanilla stone, wood, metals, and terrain
      beside Oritech machines and Rechiseled building blocks.
- [ ] Inspect Whimscape's font and GUI in JEI, Refined Storage, Simply Quests,
      Inventory Management, and configuration screens at multiple GUI scales.
- [ ] Disable Whimscape and confirm the baseline assets return without changing
      the world, inventories, or configuration.
- [ ] Confirm Jade identifies Oritech machines without unintended hidden data.
- [ ] Confirm AppleSkin, Mouse Tweaks, and Better Advancements remain
      presentation or input conveniences.
- [ ] Profile the complete base performance stack before isolating any mod.
- [ ] Background and restore the client; confirm Dynamic FPS throttles and
      resumes cleanly without a runtime download.
- [ ] Test LambDynamicLights with Oritech items, Sodium, and the backpack.
- [ ] Test Sound Physics Remastered in a factory and tunnel, then disable it
      without affecting the world.
- [ ] Enable Complementary Reimagined only after the unshaded baseline passes.
- [ ] Inspect Oritech animations, emissive textures, transparent blocks,
      portals, Rechiseled textures, and Xaero's map with shaders enabled.
- [ ] Enable Whimscape with its documented Complementary Integrated PBR+
      compatibility settings; recheck Oritech emissives, portals, glass,
      foliage, and weather.
- [ ] Disable shaders again and confirm the world remains unaffected.

## Session 6: multiplayer and persistence

- [ ] Start a disposable dedicated server from the exact candidate manifest.
- [ ] Connect two clean clients with matching pack versions.
- [ ] Agree whether the quest notebook represents team or individual progress.
- [ ] Test simultaneous and sequential quest checkbox synchronization.
- [ ] Test grave ownership before and after a clean server restart.
- [ ] Test backpack placement, pickup, death transfer, and concurrent access.
- [ ] Test XP Tome storage across logout, death, grave recovery, and restart.
- [ ] Test Oritech machines, multiblocks, drones, and remote sites across restart.
- [ ] Place the single-chunk loader and verify ownership, the four-chunk limit,
      offline timeout, and safe behavior while its owner is offline.
- [ ] Confirm map and waypoint behavior does not expose unintended player data.
- [ ] Stop the server cleanly, create a backup, restore it separately, and
      verify inventories, graves, quests, and machines.

## Session 7: configuration and update capture

- [ ] Inventory files generated or changed by the clean graphical launch.
- [ ] Identify the minimum Traveler's Backpack and Xaero settings required to
      enforce accepted pack policy.
- [ ] Identify the minimum Toast Control and Inventory Management settings;
      retain important toasts and only deliberate inventory actions.
- [ ] Review each candidate file manually; do not bulk-copy the instance
      `config/` directory.
- [ ] Remove account data, paths, server history, UUIDs, coordinates, caches,
      runtime state, and unrelated personal preferences.
- [ ] Record the exact registered control action names for `M`, `B`, and `J`.
- [ ] Determine an update-safe, first-install-only binding mechanism that does
      not distribute or overwrite a complete `options.txt`.
- [ ] Change one curated binding, restart, and update the test instance; confirm
      the player's choice survives.
- [ ] Validate the source-generated Simply Quests files against the running
      mod before accepting captured quest data.

## Session 8: release exit review

- [ ] Every required item above has a pass or a documented blocking issue.
- [ ] Every failure includes a short reproduction and sanitized evidence.
- [ ] No test-only world, log, cache, account file, or launcher state is staged.
- [ ] Required runtime configuration has been reviewed and passes the full gate.
- [ ] Player, server, controls, and troubleshooting guidance reflects observed
      behavior rather than provisional assumptions.
- [ ] Sanitized screenshots cover installation, branding, controls, and the
      intended factory experience.
- [ ] The final `.mrpack` is rebuilt, rehashed, and imported into another clean
      Prism instance.
- [ ] The final candidate repeats the dedicated-server, multiplayer, and
      persistence checks before 0.3.0 is published.
