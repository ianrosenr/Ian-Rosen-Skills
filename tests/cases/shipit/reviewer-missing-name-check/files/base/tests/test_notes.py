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
