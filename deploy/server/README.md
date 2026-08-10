# Docker server

This Compose deployment runs the locally built Signal Atelier `.mrpack` on a
Java 25 NeoForge server and coordinates world-consistent backups through an
internal RCON connection. It is intended for a small private server.

## Requirements

- Docker Engine with Docker Compose v2
- enough storage for the server plus roughly 56 compressed backups at the
  default six-hour interval and 14-day retention
- TCP port 25565 reachable only from the intended network or players

The images are pinned to the `2026.8.0` releases. Review their upstream release
notes and update both tags deliberately rather than switching to `latest`.

## Prepare

From the repository root, validate and build the current pack:

```sh
scripts/gate.sh
```

Then prepare local deployment state:

```sh
cd deploy/server
cp .env.example .env
mkdir -p server-data backups secrets
cp secrets/rcon-password.example secrets/rcon-password.txt
chmod 600 secrets/rcon-password.txt
```

Replace the example password with a long random value. The real `.env`, RCON
secret, live server, and backups are ignored by Git. Do not place credentials,
player data, world data, or backup archives in the repository.

Review `.env` before starting. `PACK_PATH` must resolve to the built `.mrpack`.
Set `SERVER_BIND_ADDRESS` to a private interface address when the server should
not listen on every host interface. Only Minecraft port 25565 is published;
RCON remains on the internal backup network.

## Start and operate

```sh
docker compose up -d
docker compose logs -f minecraft
```

The server starts with an empty enforced whitelist. Add players through the
internal RCON client:

```sh
docker compose exec minecraft rcon-cli whitelist add PLAYER_NAME
docker compose exec minecraft rcon-cli whitelist list
```

Open an interactive console with:

```sh
docker compose exec -it minecraft rcon-cli
```

Stop cleanly with a two-minute grace period:

```sh
docker compose down --timeout 120
```

## Backups

The `backups` sidecar waits for the Minecraft health check, then uses RCON to
save and pause world writes before archiving `/data`. It resumes saves after
the archive completes. Backups run at startup and every six hours; archives
older than 14 days are pruned. Live data is mounted read-only in the backup
container, and archives are written under `backups/` on the host.

Create an on-demand backup before maintenance:

```sh
docker compose exec backups backup now
docker compose logs --tail 100 backups
```

A backup on the same host is not sufficient disaster recovery. Replicate the
`backups/` directory to separately protected storage and periodically test a
restore.

## Restore

The restore profile uses the newest tar archive and deliberately refuses to
restore over non-empty `server-data/`.

1. Stop the server and backup services.
2. Preserve the current `server-data/` directory under a different name.
3. Create a new, empty `server-data/` directory with the configured UID/GID.
4. Run the restore profile.
5. Start the server and validate the restored world before deleting anything.

```sh
docker compose stop minecraft backups
docker compose --profile restore run --rm restore-backup
docker compose up -d
docker compose logs -f minecraft
```

Never open a restored world with an older pack after it has been migrated by a
newer Minecraft, NeoForge, Oritech, or modpack version.

## Update the pack

Build the new `.mrpack`, make an on-demand backup, stop the deployment, and
retain the previous pack file. Replace `PACK_PATH` only after reviewing the
pack changes, then start again. Forced Modrinth synchronization removes files
that no longer belong to the mounted pack without deleting world data.

Keep the prior server data and pack available until the updated copy has
started, stopped cleanly, restarted, and passed the relevant integration tests.
