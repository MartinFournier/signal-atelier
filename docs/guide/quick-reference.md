# Quick reference

This page summarizes intended pack behavior. Items marked **pending runtime
validation** may change after the first graphical gameplay pass.

## Technology and storage

- **Oritech 2** owns power, processing, transport, automation, remote work, and
  the principal endgame.
- **Refined Storage** provides centralized storage and request-based
  autocrafting.
- Refined Storage wireless devices, Constructors, Destructors, and remote
  network links have no intended survival recipe.
- Use Oritech pipes and drones for machine logistics and remote sites.
- **JEI** is the recipe reference; the redundant vanilla recipe book and its
  recipe-unlock toasts are intentionally suppressed.

## Travel and inventory

- **Inventory Management** provides player-initiated sorting, stacking into
  existing stacks, and container transfer. Broader automatic behavior is
  pending runtime configuration and validation.

- **Traveler's Backpack** is limited to restrained capacities of 9, 18, and 27
  slots; higher tiers and most automation-style upgrades are locked.
- Its sleeping bag is temporary and should not change the player's respawn
  point.
- **Xaero's World Map** records explored terrain without teleportation or
  entity radar. Player-marker behavior is pending runtime validation.
- Oritech's late-game transport is the intended alternative to a general
  Waystones network.
- Explorify and Thun's Structures add occasional landmarks in new chunks. A
  pack-wide 1.75 spacing multiplier keeps vanilla and added structures sparse.

## Recovery and experience

- **GraveStone** stores inventory at death and initially restricts access to
  the owner.
- **XP Tome** stores at most 1,395 XP, equivalent to reaching level 30 from
  zero.
- **Tax Free Levels** makes anvil work charge consistent raw XP while keeping
  the vanilla anvil ceiling.

## Chunk loading and quests

- Only the physical single-chunk loader is intended to be craftable.
- **Simply Quests** is an engineering notebook, not a progression gate.
- Quest milestones are manual checkboxes and grant no items, XP, or commands.

## Optional presentation

- Whimscape, Complementary Reimagined, dynamic lights, and Sound Physics
  Remastered are optional and can be disabled without affecting progression.
- Whimscape is enabled on first install but remains user-disableable. It changes
  vanilla textures, models, font, and GUI; Oritech and Rechiseled retain their
  own assets.
- Shaders are disabled for the first validation launch and are never part of
  the minimum hardware target.

## Controls

The planned bindings are:

| Action | Planned key | Status |
| --- | --- | --- |
| World map | `M` | Pending runtime validation |
| Equipped backpack | `B` | Pending runtime validation |
| Engineering notebook | `J` | Pending runtime validation |

These defaults are not packaged yet. Use **Options → Controls → Key Binds** to
find each action and resolve conflicts without displacing a vanilla control.

Fresh installs also default to unlocked Normal difficulty, keep running when
the window loses focus, and disable Xaero cave mapping. Later player choices are
preserved.
