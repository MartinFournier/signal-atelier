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
- Add Sound Physics Remastered as an independently disableable client feature.
- Keep world generation, structures, food, and farming otherwise close to
  vanilla; Oritech supplies the industrial building identity.
- Use a physical single-chunk loader from Chunk Loaders instead of map-based
  force loading. Disable the 3x3, 5x5, and 7x7 loader recipes and gate the
  single loader behind late-game Oritech materials.
- Use Simply Quests as a non-gating engineering notebook. Quests provide
  direction and documentation, not essential rewards or recipe permissions.
- Organize quests around orientation, power, industry, distributed works,
  storage, supertech, and the optional Signal Core megaproject.
- Ship 27 manual checklist milestones across those seven chapters. Keep the
  notebook reward-free and independent of recipes so experimental registry
  changes cannot block a world.
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
- Keep backups outside the instance and Git. Prefer host or filesystem
  snapshots over the immature 26.1 backup-mod ecosystem.
- Add Simple Menu as the lightweight client-side branding layer.
- Set the window title to `Signal Atelier`; keep version details in the
  manifest and launcher instance rather than crowding the title bar.
- Use a custom Signal Atelier icon and title logo built around a compact copper
  signal-wave glyph in a dark workshop frame.
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

## Pending validation and implementation

- Validate Traveler's Backpack nesting, sleeping-bag spawn behavior, tier
  locks, and GraveStone interaction in the first graphical playthrough.
- Capture Xaero's generated config and disable entity tracking and teleport;
  retain player markers only if independently supported.
- Validate the shipped Simply Quests chapter format and all cross-chapter
  dependencies in the first clean client and dedicated-server launches.
- Treat recipe removal as the initial enforcement layer. Confirm creative-tab
  visibility and every alternate acquisition path during the first launch,
  then add item hiding or stronger removal only where the running mods require
  it.
- Verify LambDynamicLights starts standalone on NeoForge despite its Modrinth
  version metadata declaring Fabric API as required.
- Confirm the configured Chunk Loaders ownership, offline timeout, random
  ticking, and per-player limits at runtime.
- Design the exact Signal Core recipe only after a complete Oritech playthrough
  establishes realistic production rates.
- Add and enable the curated splash-text resource pack after verifying the
  title logo and icons in-game.
- Capture every registered key translation and conflict from the first launch,
  then choose an update-safe first-install mechanism for the curated defaults.
  Leave optional shader, sound, overlay, and diagnostic toggles unbound unless
  testing shows a strong reason to expose them.

## Experimental policy

Oritech 2.0.0-exp3 and NeoForge 26.1 are prerelease software. Test worlds may
be reset. Pin every dependency, record upgrade results, and do not upgrade an
existing world without a recoverable backup.
