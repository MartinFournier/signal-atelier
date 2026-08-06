# Server guide

Signal Atelier targets solo play and small private cooperative servers. The
dedicated-server smoke test passes, but 0.3.0 remains a test candidate and has
not completed multiplayer progression or long-term persistence testing.

## Current support level

The repository verifies that the pinned server-side artifacts and NeoForge
26.1.2.81 start under Java 25 and reach ready state. This proves basic startup;
it does not yet prove production deployment, upgrades, backups, permissions,
network security, or complete multiplayer gameplay.

There is no supported production server bundle yet. The repository's
`scripts/smoke_server.py` creates disposable test state and must not be used as
a persistent server installer.

## Host requirements

- A 64-bit Java 25 runtime
- At least 4 GiB available to the server; 6 GiB is the safer starting point
- Storage for the server, world, logs, and independent backups
- A private or access-controlled network while the pack is experimental

Do not expose a test server publicly without normal host hardening, firewall
rules, authentication, access control, monitoring, and an incident-recovery
plan. Those concerns are outside this pack's scope.

## Before inviting players

1. Complete a clean graphical client import and disposable-world pass.
2. Confirm every player uses the same 0.3.0 manifest and Java 25.
3. Start a new disposable server world and connect at least two clients.
4. Exercise graves, backpacks, quests, chunk loading, maps, and Oritech machine
   persistence across a clean restart.
5. Agree whether Simply Quests records team or individual progress.

Never construct a server by copying the complete client `mods/` directory.
Client-only artifacts must remain client-only, and every server artifact must
come from the pinned manifest and pass its recorded checksum.

## Operations

- Stop with the server console's `stop` command and wait for shutdown to
  finish before copying or snapshotting data.
- Back up persistent state outside the live server directory.
- Keep at least one known-good backup from before every pack, loader, or mod
  update.
- Test restores regularly in a separate directory.
- Preserve the exact pack version alongside each backup.

A directory copy taken while the server is running is not automatically a
consistent backup. Prefer host or filesystem snapshots with a documented
restore procedure.

## Updating

Treat every Minecraft, NeoForge, Oritech, quest, and pack update as a possible
world migration. Follow the [safe update procedure](updating.md) using a copy
of the server and world. Do not update the only live instance in place.

Before calling server support ready for 0.3.0, complete the multiplayer and
upgrade sections of the [test plan](../test-plan.md).
