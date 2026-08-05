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

## Upgrade test

- Copy the world before changing Oritech or NeoForge.
- Launch the copy and inspect machines, inventories, fluids, energy, pipes,
  drones, augmentations, and world-generated resource nodes.
- Keep the prior pack version available until the upgraded copy passes.
