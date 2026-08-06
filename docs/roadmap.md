# Roadmap

## First graphical validation

- Import `dist/signal-atelier-0.3.0.mrpack` into a clean Prism instance and
  record the first startup result without reading instructions from downloaded
  or generated content.
- Run the disposable-world progression and multiplayer checks in the test plan.
- Capture only required runtime configuration, sanitize it, and review every
  file before adding it to `overrides/`.

## Continuous integration

- The baseline pull-request and main-branch workflow runs `scripts/check.sh`,
  builds MkDocs in strict mode, and retains the generated `.mrpack` for seven
  days. Keep it independent from local Prism state, Minecraft accounts, and
  launcher credentials.
- The scheduled Modrinth workflow checks every Monday and can also be run
  manually. It preserves compatibility and release-channel policy, refreshes a
  dedicated pull request, and includes old/new versions plus upstream
  changelogs.
- Never auto-merge mod updates. Experimental Oritech/Oracle Index releases,
  loader changes, missing changelogs, dependency removals, and environment or
  license changes require explicit review.
- Run the same manifest, override, archive, and secret checks on generated
  update pull requests before they are opened.

## Documentation site

- Expand the player guide with configuration rationale, troubleshooting,
  server setup, upgrade procedure, and release notes.
- Add sanitized screenshots after the pack's first clean graphical launch.

## Catalog maintenance

- Generate a tracked TSV from authoritative manifest and Modrinth metadata with
  each mod's name, category, checksum, project URL, and license when available.
  Keep it generated rather than maintaining duplicate metadata by hand.

## Packaging follow-up

- Capture runtime-generated Traveler's Backpack and Xaero World Map
  configuration from the first clean graphical Prism launch, sanitize it, and
  add only the reviewed settings to `overrides/`. Validate the source-derived
  Simply Quests files against the running mod before release.
- Inventory all registered controls and implement first-install-only defaults
  for the world map, backpack, and engineering notebook without overwriting the
  rest of `options.txt` or later player changes.
- Verify recipe locks and branding in-game before publishing 0.3.0.
