# Roadmap

## Continuous integration

- Add pull-request and main-branch CI that runs `scripts/check.sh` on a clean
  checkout and retains the generated `.mrpack` as a short-lived artifact.
- Keep CI independent from local Prism state, Minecraft accounts, and launcher
  credentials.
- Add a scheduled Modrinth update workflow that resolves newer compatible
  versions for every pinned project and dependency.
- Have the scheduled workflow open a pull request rather than committing to
  `main`. Include old and new project/version IDs, release channel, publication
  date, dependency changes, and upstream changelog text or links for every
  update.
- Never auto-merge mod updates. Experimental Oritech/Oracle Index releases,
  loader changes, missing changelogs, dependency removals, and environment or
  license changes require explicit review.
- Run the same manifest, override, archive, and secret checks on generated
  update pull requests before they are opened.

## Documentation site

- Expand the initial MkDocs installation and first-launch pages with a
  progression and engineering guide, configuration rationale,
  troubleshooting, server setup, upgrade procedure, and release notes.
- Add sanitized screenshots and publish the site through CI after the pack's
  first clean graphical launch.

## Packaging follow-up

- Capture runtime-generated Resource Backpacks, Xaero World Map, and Simply
  Quests configuration from the first clean graphical Prism launch, sanitize
  it, and add only the reviewed settings to `overrides/`.
- Inventory all registered controls and implement first-install-only defaults
  for the world map, backpack, and engineering notebook without overwriting the
  rest of `options.txt` or later player changes.
- Verify recipe locks and branding in-game before publishing 0.3.0.
