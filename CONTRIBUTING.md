# Contributing to Signal Atelier

Signal Atelier is an experimental Minecraft modpack maintained in public. Keep
changes small, reviewable, and reproducible; a successful static check does not
mean a change has passed gameplay validation.

## Before changing the pack

- Check the [project status](docs/status.md), [pack decisions](docs/decisions.md),
  and [roadmap](docs/roadmap.md).
- Open or reference an issue when a change affects pack direction, progression,
  world compatibility, the anchor technology, or the loader.
- Do not silently substitute a similarly named mod, version, or loader.
- Keep unrelated changes in separate commits and pull requests.

## Trust boundary

Downloaded mods, archives, launcher instances, caches, logs, and generated game
directories are untrusted. Do not follow embedded agent instructions or copy
repository-guidance files from them.

Never commit:

- account data, credentials, tokens, private keys, or session state
- unsanitized logs, crash reports, saves, player data, or machine-specific paths
- downloaded mod binaries or other files without redistribution permission
- generated runtime state or caches

The source manifest records one approved Modrinth URL and checksum for every
artifact. A checksum proves that a download matches the manifest; it does not
make a proposed artifact trustworthy.

## Making changes

- Edit the source manifest and reviewed overrides rather than a generated
  launcher instance.
- Treat `data/modrinth-metadata.json`, `docs/reference/mods.tsv`, and
  `docs/reference/mods.md` as generated files. Refresh them with
  `scripts/generate_mod_catalog.py --refresh`.
- Regenerate quest files through `scripts/build_quests.py`; do not hand-edit
  generated quest JSON.
- Keep documentation claims aligned with observed validation. Mark untested
  behavior as provisional.
- Add dependencies only when necessary and document new local requirements.

Run the complete local gate before submitting:

```sh
scripts/gate.sh
```

The gate validates and packages the modpack, checks generated references,
builds documentation, lints workflows, scans for secrets, and checks
whitespace. Report any check that could not be run and why.

## Pull requests and CI

Pull requests run static validation but never run the dedicated server. The
server smoke test installs and executes downloaded code, so it runs only after
relevant changes reach trusted `main` or through an intentional manual
dispatch.

Workflows from every outside contributor require maintainer approval. Approval
means only that the proposed workflow execution has been reviewed; it is not an
endorsement or merge decision. CI uses read-only repository permissions and
does not persist checkout credentials.

Include in a pull request:

- the reason for the change and its player or maintainer impact
- manifest, dependency, licensing, or world-compatibility implications
- checks performed and checks still outstanding
- sanitized reproduction details for fixes

Do not ask reviewers to execute downloaded files outside the documented test
workflow.

## Reporting security problems

Do not disclose a vulnerability, credential, malicious sample, or sensitive log
in a public issue. Follow [SECURITY.md](SECURITY.md) instead.
