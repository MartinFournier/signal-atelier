# Roadmap

## First graphical validation

- Work through the ordered [graphical validation
  tasklist](graphical-test-tasklist.md) and record sanitized results against the
  acceptance checks in the test plan.
- Import `dist/signal-atelier-0.3.0.mrpack` into a clean Prism instance and
  record the first startup result without reading instructions from downloaded
  or generated content.
- Run the disposable-world progression and multiplayer checks in the test plan.
- Capture only required runtime configuration, sanitize it, and review every
  file before adding it to `overrides/`.

## Documentation site

- Add sanitized screenshots after the pack's first clean graphical launch.
- Replace provisional controls and server guidance with runtime-verified steps
  after the first graphical and multiplayer validation passes.

## Packaging follow-up

- Capture runtime-generated Traveler's Backpack and Xaero World Map
  configuration, plus the minimum Toast Control and Inventory Management
  settings, from the first clean graphical Prism launch. Sanitize them and add
  only reviewed settings to `overrides/`. Validate the source-derived Simply
  Quests files and curated icons against the running mod before release.
- Diagnose the observed Save & Quit hang from a sanitized Prism console and
  `latest.log` tail, identify the last active shutdown subsystem, and verify an
  immediate relaunch before release.
- Inventory all registered controls and implement first-install-only defaults
  for the world map, backpack, and engineering notebook without overwriting the
  rest of `options.txt` or later player changes.
- Verify recipe locks and branding in-game before publishing 0.3.0.
- Validate Whimscape with Oritech, Rechiseled, JEI, Refined Storage, Simply
  Quests, and Complementary Reimagined before considering it for a default.
- Design the exact Signal Core recipe after a complete Oritech playthrough
  establishes realistic production rates.
- Add and enable the curated splash-text resource pack after verifying the
  existing title logo and icons in-game.

## Release readiness

- Keep scheduled Modrinth update pull requests review-only. Manually review
  experimental releases, loader changes, missing changelogs, dependency
  changes, environments, and licenses.
- Export the final `.mrpack`, import it into a clean Prism instance, and repeat
  the dedicated-server and multiplayer checks before publishing 0.3.0.
