# Updating safely

Signal Atelier, NeoForge, and Oritech are experimental. An update that launches
successfully can still damage machines, inventories, networks, quests, or
world-generated resources.

## Before updating

1. Record the current Signal Atelier, Minecraft, NeoForge, and Oritech
   versions.
2. Exit the game, or stop the dedicated server cleanly.
3. Create a recoverable backup outside the launcher or server directory.
4. Keep the old pack instance and installer available.
5. Read the release notes for known incompatibilities and required actions.

For a server, preserve the world, server configuration, allowlist, operator
list, and the exact pack version. Protect backups with the same care as the
live server because they contain player data.

## Prefer a fresh instance

Import the new `.mrpack` as a separate Prism instance. Copy only a disposable
world backup into it for validation. Do not merge `mods/`, copy an old
`options.txt`, or carry all generated configuration forward automatically.

This preserves a clean comparison and keeps the previous instance available
for rollback.

## Validate the copy

Check the updated copy before opening the primary world:

- machines, multiblocks, addons, energy, fluids, and inventories
- item, fluid, and energy pipes
- drones and remote resource sites
- Refined Storage networks and recursive autocrafting
- backpacks, graves, XP Tomes, and chunk loaders
- quest completion, chapter order, and team visibility
- map data, dimensions, and player connection

Restart at least once and repeat the checks that involve persistence. A
successful first load is not enough.

## Promote or roll back

Promote the tested copy only after its checks pass. Keep the prior instance and
backup until the updated world has survived normal play and another clean
restart.

If validation fails, stop using the updated copy and return to the previous
pack with a world that has never been opened by the failed update. Do not open
an already-migrated save in an older version and assume it will reverse the
migration.

Report failures with sanitized logs, the source and target versions, and the
smallest reproduction sequence. See [Troubleshooting](troubleshooting.md).
