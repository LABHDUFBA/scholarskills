from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.scaffold_project import create_scaffold, scaffold_files


class ScaffoldProjectTests(unittest.TestCase):
    def test_creates_minimal_documentation_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo-project"
            result = create_scaffold(target, "Synthetic Example")
            self.assertEqual(result, target.resolve())
            for relative in scaffold_files("Synthetic Example"):
                self.assertTrue((target / relative).is_file(), relative)
            self.assertIn("# Synthetic Example", (target / "README.md").read_text())
            self.assertFalse((target / ".git").exists())
            self.assertFalse((target / "data").exists())

    def test_refuses_existing_empty_directory_without_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "already-here"
            target.mkdir()
            with self.assertRaises(FileExistsError):
                create_scaffold(target, "Example")
            self.assertEqual(list(target.iterdir()), [])

    def test_refuses_existing_nonempty_directory_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            sentinel = target / "README.md"
            sentinel.write_text("keep this", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                create_scaffold(target, "Replacement")
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep this")
            self.assertEqual(sorted(p.name for p in target.iterdir()), ["README.md"])

    def test_rejects_blank_title_without_creating_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "not-created"
            with self.assertRaises(ValueError):
                create_scaffold(target, "  \n")
            self.assertFalse(target.exists())

    def test_refuses_current_working_directory(self) -> None:
        with self.assertRaises(ValueError):
            create_scaffold(Path.cwd(), "Unsafe")

    def test_refuses_filesystem_root(self) -> None:
        with self.assertRaises(ValueError):
            create_scaffold(Path(Path.cwd().anchor), "Unsafe")


if __name__ == "__main__":
    unittest.main()
