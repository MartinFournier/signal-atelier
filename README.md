# Signal Atelier

<img src="overrides/config/simplemenu/logo/logo.png" alt="Signal Atelier" width="512">

**A focused automation workshop.**

[![CI](https://github.com/MartinFournier/signal-atelier/actions/workflows/ci.yml/badge.svg)](https://github.com/MartinFournier/signal-atelier/actions/workflows/ci.yml)
[![Server smoke test](https://github.com/MartinFournier/signal-atelier/actions/workflows/server-smoke.yml/badge.svg)](https://github.com/MartinFournier/signal-atelier/actions/workflows/server-smoke.yml)

[Read the Signal Atelier player guide](https://dev.mfournier.com/signal-atelier/).

Signal Atelier is a small, technology-focused Minecraft modpack built around
Oritech. It favors one coherent factory system over overlapping machines that
solve the same problems in slightly different ways.

This pack is vibe-coded with AI assistance. Mod selection and balance remain
intentional, artifacts are pinned and checked, and generated changes are not
treated as gameplay-tested until they pass the documented validation plan.

The pack and its anchor technology are experimental. Use a disposable world
and back it up before every loader or mod update.

## Highlights

- Oritech 2 for power, machines, processing, transport, and world interaction
- Restricted Refined Storage for centralized storage and autocrafting
- Restrained backpacks, graves, XP storage, maps, and quality-of-life tools
- Performance-focused defaults with optional shaders, lighting, and sound
- A guided engineering notebook and physical single-chunk loading
- Solo and small cooperative server support

## Current target

| Component | Version |
| --- | --- |
| Minecraft | 26.1.2 |
| NeoForge | 26.1.2.81 |
| Java | 25 |
| Oritech | 2.0.0-exp3 |
| Pack | 0.3.0 test candidate |

## Get started

Players should follow the [installation guide](https://dev.mfournier.com/signal-atelier/guide/install/)
and [first-launch checklist](https://dev.mfournier.com/signal-atelier/guide/first-launch/).

Maintainers can build the Modrinth pack and run the complete repository gate:

```sh
scripts/build.sh
scripts/gate.sh
```

Preview documentation with hot reload on port 8000:

```sh
scripts/serve-docs.sh
```

The preview binds all IPv4 interfaces so it is available at
`http://172.20.x.x:8000/signal-atelier/` on the local network. Set
`SIGNAL_ATELIER_DOCS_ADDR=127.0.0.1:8000` to restrict it to the local machine.

Import `dist/signal-atelier-0.3.0.mrpack` into Prism Launcher with Java 25.

## Project reference

- [Current status](https://dev.mfournier.com/signal-atelier/status/)
- [Generated mod catalog](https://dev.mfournier.com/signal-atelier/reference/mods/)
- [Pack decisions](https://dev.mfournier.com/signal-atelier/decisions/)
- [Test plan](https://dev.mfournier.com/signal-atelier/test-plan/)
- [Roadmap](https://dev.mfournier.com/signal-atelier/roadmap/)

## Trust and license

Downloaded mods and generated game content are untrusted. The source manifest
pins Modrinth URLs and hashes; repository maintenance does not treat files or
embedded instructions from downloaded artifacts as trusted project guidance.

Signal Atelier's original project files are available under the [MIT
License](LICENSE). Included mods retain their upstream licenses and are
downloaded from Modrinth rather than redistributed by this repository.
