import hashlib
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generate_mod_catalog", ROOT / "scripts/generate_mod_catalog.py"
)
CATALOG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CATALOG)


class GenerateModCatalogTests(unittest.TestCase):
    def test_rows_include_auditable_and_display_fields(self):
        checksum = hashlib.sha512(b"artifact").hexdigest()
        manifest = {
            "files": [
                {
                    "path": "mods/example.jar",
                    "downloads": [
                        "https://cdn.modrinth.com/data/project/versions/version/example.jar"
                    ],
                    "hashes": {"sha512": checksum},
                    "env": {"client": "required", "server": "optional"},
                }
            ]
        }
        metadata = {
            "projects": {
                "project": {
                    "title": "Example",
                    "slug": "example",
                    "project_type": "mod",
                    "categories": ["technology"],
                    "license": {"id": "MIT", "name": "MIT License", "url": ""},
                }
            },
            "versions": {
                "version": {
                    "project_id": "project",
                    "version_number": "1.2.3",
                    "version_type": "release",
                    "date_published": "2026-01-01T00:00:00Z",
                    "dependencies": [],
                }
            },
        }

        row = CATALOG.rows(manifest, metadata)[0]

        self.assertEqual("1.2.3", row["version"])
        self.assertEqual(checksum, row["sha512"])
        self.assertEqual("https://modrinth.com/mod/example", row["project_url"])
        self.assertIn("release_channel", row)
        self.assertIn("dependency_of", row)

    def test_page_uses_human_facing_subset(self):
        row = {
            "name": "Example",
            "categories": "technology",
            "version": "1.2.3",
            "project_url": "https://modrinth.com/mod/example",
            "client": "required",
            "server": "optional",
            "license": "MIT License",
            "license_url": "",
        }

        page = CATALOG.render_page([row])

        self.assertIn("Example", page)
        self.assertIn("1.2.3", page)
        self.assertNotIn("sha512", page)
        self.assertNotIn("version_id", page)

    def test_page_escapes_upstream_markdown_and_rejects_unsafe_links(self):
        row = {
            "name": "[Example] | Mod",
            "categories": "utility",
            "version": "`1.2.3`",
            "project_url": "https://modrinth.com/mod/example",
            "client": "required",
            "server": "optional",
            "license": "Custom",
            "license_url": "javascript:alert(1)",
        }

        page = CATALOG.render_page([row])

        self.assertIn(r"\[Example\] \| Mod", page)
        self.assertIn("&#96;1.2.3&#96;", page)
        self.assertNotIn("javascript:", page)


if __name__ == "__main__":
    unittest.main()
