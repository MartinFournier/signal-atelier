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

## Upgrade test

- Copy the world before changing Oritech or NeoForge.
- Launch the copy and inspect machines, inventories, fluids, energy, pipes,
  drones, augmentations, and world-generated resource nodes.
- Keep the prior pack version available until the upgraded copy passes.
