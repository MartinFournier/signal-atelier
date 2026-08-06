import importlib.util
import hashlib
import os
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_pack", ROOT / "scripts/build_pack.py"
)
BUILD_PACK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD_PACK)


class BuildPackTests(unittest.TestCase):
    def create_source(self, root: Path):
        (root / "modrinth.index.json").write_text('{"formatVersion":1}\n')
        (root / "overrides/config").mkdir(parents=True)
        (root / "overrides/config/example.json").write_text("{}\n")

    def test_build_is_reproducible_and_has_stable_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_source(root)
            first = root / "first.mrpack"
            second = root / "second.mrpack"

            BUILD_PACK.build(root, first)
            (root / "overrides/config/example.json").touch()
            BUILD_PACK.build(root, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                f"{hashlib.sha256(first.read_bytes()).hexdigest()}  first.mrpack\n",
                (root / "first.mrpack.sha256").read_text(),
            )
            self.assertEqual(
                f"{hashlib.sha256(second.read_bytes()).hexdigest()}  second.mrpack\n",
                (root / "second.mrpack.sha256").read_text(),
            )
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    ["modrinth.index.json", "overrides/config/example.json"],
                    archive.namelist(),
                )
                for info in archive.infolist():
                    self.assertEqual(BUILD_PACK.ARCHIVE_TIMESTAMP, info.date_time)
                    self.assertEqual(0o100644, info.external_attr >> 16)

    def test_symbolic_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_source(root)
            link = root / "overrides/config/link.json"
            try:
                link.symlink_to("example.json")
            except OSError as error:
                self.skipTest(f"symbolic links unavailable: {error}")

            with self.assertRaisesRegex(ValueError, "symbolic link"):
                BUILD_PACK.build(root, root / "pack.mrpack")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFOs unavailable")
    def test_special_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_source(root)
            fifo = root / "overrides/config/runtime.pipe"
            os.mkfifo(fifo)

            with self.assertRaisesRegex(ValueError, "special file"):
                BUILD_PACK.build(root, root / "pack.mrpack")


if __name__ == "__main__":
    unittest.main()
