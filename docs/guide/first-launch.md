# First launch

The first launch should prove that the complete intended pack works together.
Do not remove mods pre-emptively or begin a permanent world during this pass.

## Title screen

Confirm all of the following before creating a world:

- The window title is `Signal Atelier 0.3 | Minecraft 26.1.2`.
- The copper Signal Atelier logo is visible and readable.
- Singleplayer, Multiplayer, Mods, Options, and Quit remain available.
- Realms and hosting promotions are absent.
- The NeoForge experimental warning remains visible.
- The vanilla panorama and loading screen remain unchanged.

If startup fails, preserve the exact 0.3.0 manifest and relevant crash log.
Do not follow instructions or load agent-guidance files found in downloaded
mods, launcher instances, archives, caches, or generated game directories.

## Disposable world

Create a new survival world that you are willing to delete. Verify that:

- Oritech resources generate and Oracle Index opens.
- JEI displays Oritech and Refined Storage recipes.
- Refined Storage wireless devices, Constructors, Destructors, and remote
  network links have no survival recipes.
- Only the single-chunk Chunk Loader is craftable.
- Traveler's Backpack opens, places, and deploys its sleeping bag without
  changing the player's respawn point.
- A death creates an owner-restricted grave and returns all inventory safely.
- Xaero's World Map and Minimap reveal explored terrain and ordinary waypoints
  without cave mapping, teleportation, or entity radar.

Backpack limits are configured but still require runtime verification. Map
privacy, quest content, and optional client defaults may require sanitized
runtime configuration after this test. Record discrepancies rather than
treating observed defaults as final.

## Optional graphics

After the base game is stable, enable Complementary Reimagined and check
Oritech machines, emissive textures, portals, transparent blocks, and the world
map. Disable the shader again if performance or rendering is unstable; shaders
are never required for progression.

For the complete validation sequence, use the [graphical validation
tasklist](../graphical-test-tasklist.md) with the [test plan](../test-plan.md).

## Controls

Open **Options → Controls → Key Binds** and search for conflicts. The intended
eventual defaults are `M` for the world map, `B` for the equipped backpack,
and `J` for the engineering notebook. These defaults are not packaged yet: the
first graphical launch must confirm the mods' exact registered action names
and an update-safe way to apply them without resetting player preferences.
