# Pack decisions

## Accepted

- Use Modrinth as the catalog and distribution format.
- Target Minecraft 26.1.2 with NeoForge and Java 25.
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
- Add Resource Backpacks for modest expedition storage.
- Limit backpacks to leather, copper, and iron progression with 18–27 slots.
- Disable higher-tier and ender backpacks, backpack nesting, and filled
  shulker storage inside backpacks.
- Add GraveStone Mod as the sole death-recovery system with no grave expiry or
  teleport-to-grave feature.
- Keep graves owner-restricted initially and verify multiplayer ownership,
  backpack preservation, and persistence after server restarts.
- Add Jade, AppleSkin, Mouse Tweaks, and Better Advancements as the initial
  quality-of-life set.
- Add Xaero's World Map without Xaero's Minimap.
- Limit mapping to explored terrain and ordinary waypoints. Disable entity
  tracking and map teleportation; allow player markers only if World Map
  supports them independently.

## Deferred

- Shaders, voice chat, claims, and server administration.
- Xaero's Minimap and live entity radar.
- Polymorph unless an actual recipe conflict is found.
- A permanent world and release designation.

## Pending implementation

- Select a 26.1.2-compatible recipe-locking mechanism that does not require
  unregistering content from existing worlds.
- Pin Refined Storage, Resource Backpacks, and all required dependencies only
  after the restrictions can ship in the same test build.
- Verify whether Resource Backpacks can reject filled shulker boxes through
  configuration; otherwise enforce the restriction with the pack layer.
- Confirm exact NeoForge 26.1.2 artifacts for the selected quality-of-life
  mods and whether player-only markers are available in World Map alone.

## Experimental policy

Oritech 2.0.0-exp3 and NeoForge 26.1 are prerelease software. Test worlds may
be reset. Pin every dependency, record upgrade results, and do not upgrade an
existing world without a recoverable backup.
