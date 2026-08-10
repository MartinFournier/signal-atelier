import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
DEPLOY = ROOT / "deploy/server"
COMPOSE = (DEPLOY / "compose.yaml").read_text()
GITIGNORE = (ROOT / ".gitignore").read_text()


class DockerServerTests(unittest.TestCase):
    def test_images_and_pack_are_pinned(self):
        self.assertIn("itzg/minecraft-server:2026.8.0-java25", COMPOSE)
        self.assertEqual(2, COMPOSE.count("itzg/mc-backup:2026.8.0"))
        self.assertIn("TYPE: MODRINTH", COMPOSE)
        self.assertIn("MODRINTH_FORCE_SYNCHRONIZE: \"true\"", COMPOSE)
        self.assertIn("signal-atelier-0.3.0.mrpack", COMPOSE)
        self.assertNotIn(":latest", COMPOSE)

    def test_rcon_is_internal_and_secret_backed(self):
        self.assertNotIn("25575:25575", COMPOSE)
        self.assertNotIn("RCON_PASSWORD:", COMPOSE)
        self.assertEqual(2, COMPOSE.count("RCON_PASSWORD_FILE:"))
        self.assertIn("internal: true", COMPOSE)
        self.assertIn("BROADCAST_RCON_TO_OPS: \"false\"", COMPOSE)

    def test_private_server_defaults_are_bounded(self):
        self.assertIn("ENABLE_WHITELIST: \"true\"", COMPOSE)
        self.assertIn("ENFORCE_WHITELIST: \"true\"", COMPOSE)
        self.assertIn("ONLINE_MODE: \"true\"", COMPOSE)
        self.assertIn("stop_grace_period: 2m", COMPOSE)
        self.assertIn("MEMORY: \"${MEMORY:-6G}\"", COMPOSE)

    def test_backup_is_coordinated_and_cannot_write_live_data(self):
        self.assertIn("condition: service_healthy", COMPOSE)
        self.assertIn("BACKUP_INTERVAL: \"6h\"", COMPOSE)
        self.assertIn("PRUNE_BACKUPS_DAYS: \"14\"", COMPOSE)
        self.assertIn("./server-data:/data:ro", COMPOSE)
        self.assertIn("entrypoint: restore-tar-backup", COMPOSE)
        self.assertIn("profiles:\n      - restore", COMPOSE)

    def test_runtime_and_secrets_are_ignored(self):
        for path in (
            "/deploy/server/.env",
            "/deploy/server/server-data/",
            "/deploy/server/backups/",
            "/deploy/server/secrets/*.txt",
        ):
            self.assertIn(path, GITIGNORE)
        self.assertIn("!/deploy/server/secrets/*.example", GITIGNORE)


if __name__ == "__main__":
    unittest.main()
