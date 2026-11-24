import tempfile
import unittest
from pathlib import Path

import notes


class ListTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        notes.NOTES_DIR = self.dir

    def test_list_sorted(self):
        (self.dir / "b.md").write_text("b")
        (self.dir / "a.md").write_text("a")
        self.assertEqual(notes.list_notes(), ["a", "b"])


class ShowTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        notes.NOTES_DIR = self.dir

    def test_show_existing(self):
        (self.dir / "todo.md").write_text("buy milk")
        self.assertEqual(notes.main(["show", "todo"]), 0)

    def test_show_missing(self):
        self.assertEqual(notes.main(["show", "nope"]), 1)

    def test_show_invalid_name(self):
        (self.dir.parent / "secret.md").write_text("s")
        self.assertEqual(notes.main(["show", "../secret"]), 2)
