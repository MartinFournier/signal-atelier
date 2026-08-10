# Project status

Signal Atelier 0.3.0 is a full-pack test candidate for Minecraft 26.1.2,
NeoForge 26.1.2.81, and Java 25. Oritech 2.0.0-exp3 is the anchor technology
mod, so worlds remain disposable while the loader and anchor mod are
experimental.

## Verified

- Static manifest, configuration, recipe-lock, branding, archive, reference,
  documentation, workflow, whitespace, and secret checks pass.
- The headless dedicated server verifies 23 pinned server artifacts, installs
  the checksum-verified NeoForge server, reaches ready state, and stops cleanly.
- Both cold and fully restored content-addressed download caches pass the same
  server smoke test; every restored artifact is rehashed before execution.
- Because the smoke test executes downloaded artifacts, it runs only after
  relevant changes reach trusted `main` or through intentional manual dispatch;
  pull requests receive static validation instead.
- The first headless run exposed incompatible NeoForge constraints. Resource
  Backpacks and its libraries were removed, and NeoForge was raised to
  26.1.2.81 before the successful run.

## Still required

- Clean graphical Prism import and first launch
- Disposable-world gameplay and progression pass
- Runtime configuration capture and sanitization
- Multiplayer connection and persistence testing
- In-game recipe-lock, quest, control, map, backpack, and branding validation
- Runtime validation of recipe-book suppression, toast filtering, inventory
  management, and curated quest icons
- Diagnosis of the observed Save & Quit process hang and clean relaunch proof

See the [test plan](test-plan.md) for acceptance checks and the
[roadmap](roadmap.md) for implementation follow-up.
