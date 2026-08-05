# Install Signal Atelier

## Requirements

- A Minecraft Java Edition account
- Prism Launcher 11 or newer
- A 64-bit Java 25 runtime
- At least 4 GiB of memory available to Minecraft; 6 GiB is recommended
- A GPU that supports the base game on Minecraft 26.1.2

Shaders are optional and are not part of the minimum hardware target.

## Import the pack

1. Download `signal-atelier-0.3.0.mrpack` from a trusted project release or
   build it from the repository with `scripts/build.sh`.
2. Open Prism Launcher.
3. Choose **Add Instance**, then **Import**.
4. Select the `.mrpack` file and finish the import.
5. Open the instance settings and confirm that Prism selected Java 25.
6. Set maximum memory to 4096 MiB at minimum or 6144 MiB when the computer has
   enough free memory.

Prism downloads the pinned mod files from Modrinth during import. Do not copy
mods from unrelated instances or replace files based only on similar names.

## Before playing

Keep saves and backups outside the launcher instance. The 0.3.0 candidate uses
experimental Oritech and NeoForge versions, and existing worlds may not survive
an update.

Leave Complementary Reimagined disabled for the first launch. Establish a
working baseline before enabling shaders or changing graphics options.

Continue with the [first-launch checklist](first-launch.md).

## Building from source

From the repository root:

```sh
scripts/check.sh
```

The gate validates the manifest, curated configuration, recipe locks, branding
assets, and generated archive. The resulting pack is
`dist/signal-atelier-0.3.0.mrpack`.
