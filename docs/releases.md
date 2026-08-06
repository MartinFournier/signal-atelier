# Release notes

Signal Atelier has not reached a stable release. Test candidates may require a
new disposable world and should never be applied to the only copy of a save.

## 0.3.0 test candidate

Target: Minecraft 26.1.2, NeoForge 26.1.2.81, Java 25, and Oritech
2.0.0-exp3.

### Pack direction

- Establish Oritech 2 as the broad technology and endgame system.
- Add bounded Refined Storage for centralized storage and request-based
  autocrafting without wireless or world-interaction shortcuts.
- Add restrained backpacks, graves, XP storage, a privacy-conscious world map,
  physical single-chunk loading, and an optional engineering notebook.
- Add a focused performance stack with optional shaders, dynamic lighting, and
  sound simulation.

### Presentation and documentation

- Add Signal Atelier window branding, project icon, and title-screen wordmark.
- Publish installation, first-launch, progression, troubleshooting, server,
  safe-update, and quick-reference documentation.
- Publish generated pack and Modrinth artifact references.

### Validation status

- Static repository, manifest, generated-data, archive, documentation,
  workflow, whitespace, and secret checks pass.
- The dedicated server reaches ready state with checksum-verified artifacts
  and passes both cold-cache and restored-cache runs.
- Graphical import, gameplay progression, multiplayer persistence, runtime
  configuration, controls, and in-game branding still require validation.

See [Project status](status.md) for the current evidence and [Updating
safely](guide/updating.md) before testing a later candidate against a world.
