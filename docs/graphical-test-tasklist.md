# Graphical smoke checklist

Use this short checklist for a practical Prism Launcher test. A normal pass
should take about 30 minutes. The broader [test plan](test-plan.md) remains the
reference for release investigation and multiplayer validation; it is not a
required script for every candidate.

Test a newly imported `.mrpack` in a disposable world. Record the pack commit,
`.mrpack` SHA-256, Prism version, Java version, and whether shaders or Whimscape
were enabled. Do not publish account details, server addresses, personal paths,
coordinates, or unsanitized logs.

## Stop and report

Stop after a repeatable crash, corrupted world, lost or duplicated item, broken
recipe lock, or a Save & Quit process that does not exit. Keep the exact pack
and a short reproduction. For an exit hang, preserve only the sanitized tail of
the Prism console and `latest.log` before using Prism's Kill action.

## Import, launch, and exit

- [ ] Import the candidate into a clean Prism instance using Java 25 and 4–6
      GiB of memory.
- [ ] Reach the title screen; confirm Signal Atelier branding and the expected
      Minecraft, NeoForge, and modpack versions.
- [ ] Confirm Whimscape is enabled and Complementary Reimagined is installed but
      disabled.
- [ ] Create and enter a disposable survival world without a crash.
- [ ] Save and quit. Confirm Java exits without Prism's Kill action, then launch
      the same instance and reopen the world.

## Core experience

- [ ] Open JEI and inspect an Oritech recipe. Confirm the vanilla recipe book is
      absent and recipe-unlock/tutorial toasts do not duplicate JEI guidance.
- [ ] Open an ordinary chest. Sort it, stack matching items into existing
      stacks, and deliberately transfer items; confirm counts do not change.
- [ ] Open Simply Quests. Confirm seven chapters, 44 milestones, descriptive
      item icons, and manual checkboxes. Complete and claim one milestone;
      confirm its small item reward arrives once and does not auto-repeat.
- [ ] Open Xaero's World Map above ground and underground. Confirm unexplored
      terrain and caves are not revealed, and teleportation/entity radar are
      unavailable.
- [ ] Move focus to another window. Confirm Minecraft keeps running without
      opening the pause menu, then verify the player can change this preference.
- [ ] Explore new terrain briefly. Added landmarks should feel occasional, not
      clustered or constantly visible on Xaero's map.
- [ ] Open Oracle Index, a Traveler's Backpack, and the Controls screen. Confirm
      their interfaces work and important bindings do not conflict.
- [ ] Place or inspect an Oritech machine and a Rechiseled block. Confirm no
      missing textures, broken models, or unreadable GUI elements.

## Optional visuals

- [ ] Enable Whimscape. Recheck an Oritech machine beside vanilla and Rechiseled
      blocks, plus JEI, Simply Quests, and an inventory screen for visual fit and
      readable text.
- [ ] If shaders matter to you, enable Complementary Reimagined with Whimscape's
      documented Integrated PBR+ compatibility settings and inspect emissives,
      glass, portals, foliage, and weather.
- [ ] Disable each optional visual again and confirm the world still opens
      normally.

## Finish

- [ ] Play normally for the remainder of the session and record only noticeable
      crashes, severe visual problems, confusing controls, or progression
      blockers.
- [ ] Save and quit one final time; confirm the process exits and another launch
      is immediately available.

If this smoke pass succeeds, report it as a graphical smoke pass rather than
complete release validation. Dedicated-server and multiplayer checks remain
separate because they cannot be established by a short singleplayer session.
