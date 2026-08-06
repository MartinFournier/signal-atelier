# Security policy

Signal Atelier is an experimental modpack that downloads and executes code from
third-party projects. Report security problems privately so maintainers can
investigate without exposing players or repository infrastructure.

## Supported versions

Security fixes target the current `main` branch and the latest published test
candidate. Older candidates and locally modified packs may be asked to upgrade
or reproduce against the current manifest.

## Private reporting

Use [GitHub private vulnerability reporting](https://github.com/MartinFournier/signal-atelier/security/advisories/new).
Include the affected pack version or commit, impact, reproduction conditions,
and the smallest evidence required to understand the problem.

Do not include real credentials, access tokens, private keys, player data, or
unsanitized logs. Replace secrets with clearly labeled placeholders. Do not
upload a malicious executable or mod unless a maintainer explicitly arranges a
safe transfer method.

Please allow time for a best-effort investigation before public disclosure.
This is a small project and does not promise a fixed response or remediation
deadline.

## In scope

- Workflow, release, manifest, checksum, or update-pipeline vulnerabilities
- Pack configuration that exposes credentials or private player/server data
- A bundled or referenced artifact that creates a pack-specific security risk
- Documentation that directs users toward an unsafe installation or recovery
  procedure

General vulnerabilities in Minecraft, NeoForge, or an upstream mod should also
be reported to that upstream project through its security process. Report them
here privately when Signal Atelier is directly affected or needs mitigation.

## Public issues

Use public issues for ordinary bugs only. Sanitize logs and screenshots before
posting: remove tokens, server addresses, IP addresses, chat, player UUIDs,
personal paths, and unrelated system information.
