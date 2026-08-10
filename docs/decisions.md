# Pack decisions

## Accepted

- Use Modrinth as the catalog and distribution format.
- Target Minecraft 26.1.2 with NeoForge 26.1.2.81 and Java 25.
- Use Oritech 2 as the only broad technology mod.
- Keep world generation close to vanilla.
- Support solo play and a small private server.
- Aim for moderate progression without expert recipe changes.
- Avoid overlapping machine, power, pipe, and ore-processing systems.
- Add Refined Storage for centralized storage and request-based autocrafting.
- Allow Refined Storage to store, request, and route resources while keeping
  world interaction and remote logistics in Oritech.
- Recipe lock Refined Storage wireless access, Constructors, Destructors,
  Network Transmitters and Receivers, and equivalent remote or direct-world
  features.
- Keep Refined Storage Controllers, cables, disks, drives, Grids, Pattern
  Grids, Autocrafters, Monitors, Importers, Exporters, Interfaces, External
  Storage, Detectors, and required upgrades.
- Add Traveler's Backpack for modest expedition storage. Retain its sleeping
  bag because it skips the night without changing the player's spawn point.
- Target 9, 18, and 27 storage slots across the first three tiers. Disable
  higher tiers, backpack nesting, tanks, crafting, furnace, feeding, magnet,
  pickup, void, lantern, special abilities, and generated backpack loot.
- Add GraveStone Mod as the sole death-recovery system with no grave expiry or
  teleport-to-grave feature.
- Keep graves owner-restricted initially and verify multiplayer ownership and
  persistence after server restarts.
- Add Jade, AppleSkin, Mouse Tweaks, and Better Advancements as the initial
  quality-of-life set.
- Use JEI as the sole recipe-discovery interface. Remove the redundant vanilla
  recipe book with Not Enough Recipe Book and suppress recipe-unlock and
  tutorial toasts with Toast Control; retain advancement and system feedback.
- Add Inventory Management for deliberate inventory sorting, stacking into
  existing stacks, and container transfer. Keep automatic replacement,
  unsolicited hotbar changes, and other automation disabled until its clean
  runtime configuration is captured and validated.
- Add Xaero's World Map without Xaero's Minimap.
- Limit mapping to explored terrain and ordinary waypoints. Disable entity
  tracking and map teleportation; allow player markers only if World Map
  supports them independently.
- Use Lithium on both client and server, and ImmediatelyFast on the client.
- Add Dynamic FPS for background resource savings with optional runtime
  battery-library downloads disabled.
- Add Iris and bundle Complementary Reimagined as an optional shader that is
  disabled by default.
- Add LambDynamicLights with conservative update quality.
- Add Rechiseled as the sole general-purpose decorative block expansion.
- Bundle Whimscape as the default visual overhaul while keeping it optional and
  user-disableable. Apply it only on first install through Default Options,
  preserve later player choices, keep pack branding above it, and do not require
  its optional OptiFine-equivalent features.
- Add Sound Physics Remastered as an independently disableable client feature.
- Keep terrain generation, food, and farming otherwise close to vanilla;
  Oritech supplies the industrial building identity.
- Add Explorify and Thun's Structures for a restrained set of discoverable
  landmarks. Use Structurify to multiply spacing and separation for all
  structure sets by 1.75 so the combined catalog remains uncommon and does not
  crowd the world map.
- Use a physical single-chunk loader from Chunk Loaders instead of map-based
  force loading. Disable the 3x3, 5x5, and 7x7 loader recipes and gate the
  single loader behind late-game Oritech materials.
- Use Simply Quests as a non-gating engineering notebook. Quests provide
  direction and documentation, not essential rewards or recipe permissions.
- Organize quests around orientation, power, industry, distributed works,
  storage, supertech, and the optional Signal Core megaproject.
- Ship 44 manual checklist milestones across those seven chapters. Use the
  additional steps for meaningful system guidance rather than individual
  recipes. Keep small, one-time vanilla utility rewards on major milestones,
  with no machinery, ores, XP, commands, recipe permissions, or
  progression-critical materials.
- Give each milestone a curated vanilla item icon instead of displaying its
  identical checkbox task icon.
- Add XP Tome with its default 1,395 XP capacity, equivalent to level 30.
- Add Tax Free Levels for level-independent XP accounting while retaining the
  vanilla anvil limit.
- Add Enchantment Descriptions for client-side tooltip documentation.
- Keep vanilla enchantment acquisition: no extraction tables, arbitrary
  selection, cheap rerolls, or additional enchantment families.
- Treat the Signal Core as a provisional post-supertech objective requiring
  renewable remote resources, nuclear-scale power, particle-accelerator
  products, autocrafting, and interdimensional logistics.
- Target solo play and small cooperative servers at 4 GiB minimum and 6 GiB
  recommended memory allocation. Shaders are never part of the minimum target.
- Pin every mod version and update in tested batches without grind multipliers.
- Keep balance and server configuration pack-controlled while leaving cosmetic
  client settings user-controlled.
- Ship a small, conflict-free default keybind layout for major pack interfaces
  without replacing movement, inventory, combat, hotbar, screenshot, or debug
  controls. Target `M` for the world map, `B` for the equipped backpack, and
  `J` for the engineering notebook if those exact actions exist.
- Preserve player keybind changes across pack updates. Do not distribute a
  complete `options.txt` that resets unrelated video, audio, accessibility, or
  control preferences.
- Use Default Options for narrow first-install defaults: enable Whimscape,
  disable pause-on-lost-focus, and default new worlds to unlocked Normal
  difficulty. Do not initialize hardware-dependent or accessibility settings.
- Disable Xaero cave maps by default and prohibit cave mode through the
  server-capable World Map common configuration. Retain surface mapping of only
  chunks received by the client.
- Keep backups outside the instance and Git. Prefer host or filesystem
  snapshots over the immature 26.1 backup-mod ecosystem.
- Add Simple Menu as the lightweight client-side branding layer.
- Set the window title to `Signal Atelier 0.3 | Minecraft 26.1.2` so screenshots
  and support reports identify both the pack line and Minecraft version.
- Use a custom Signal Atelier icon and title wordmark built around a pixel-art
  pickaxe emitting signal waves from its head.
- Keep the vanilla panorama and loading screen initially.
- Hide Realms, but retain the standard Singleplayer, Multiplayer, Mods,
  Options, and Quit controls.
- Keep NeoForge's experimental warning visible and include no hosting
  advertisements or custom external-link buttons.
- Ship a small built-in resource pack with curated Signal Atelier splash text.
- Build Signal Atelier 0.3.0 as one complete candidate containing every
  accepted mod and its enforcement configuration before the first gameplay
  test.
- Test the complete intended experience first. If it fails, bisect by the
  documented functional groups without publishing partial integration builds.

## Deferred

- Voice chat, land claims, and public-server administration.
- Xaero's Minimap and live entity radar.
- Polymorph unless an actual recipe conflict is found.
- Entity Culling unless profiling finds a remaining entity-render bottleneck
  after Sodium's asynchronous occlusion culling.
- Aggressive asynchronous chunk, world-threading, redstone, and entity-ticking
  optimizers until profiling justifies their compatibility risk.
- FramedBlocks, Effortless Building, broad furniture packs, and extra particle
  or foliage systems.
- FancyMenu and custom loading-screen mods unless the lightweight branding
  proves insufficient.
- Resource Backpacks remains excluded because its current loader constraints
  conflict with Oritech and JEI.
- A permanent world and release designation while Oritech 2 remains
  experimental.

## Validation

Accepted decisions are not considered runtime-proven until they pass the
[test plan](test-plan.md). Remaining implementation work is tracked in the
[roadmap](roadmap.md), and the latest verified baseline is recorded in
[project status](status.md).

## Experimental policy

Oritech 2.0.0-exp3 and NeoForge 26.1 are prerelease software. Test worlds may
be reset. Pin every dependency, record upgrade results, and do not upgrade an
existing world without a recoverable backup.
