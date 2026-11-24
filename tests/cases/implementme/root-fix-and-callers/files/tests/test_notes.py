import tempfile
import unittest
from pathlib import Path

import export
import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        notes.NOTES_DIR = self.dir
        (self.dir / "b.md").write_text("bee")
        (self.dir / "a.md").write_text("ay")

    def test_list_sorted(self):
        self.assertEqual(notes.list_notes(), ["a", "b"])

    def test_export_all(self):
        out = self.dir / "out.txt"
        export.export(out)
        self.assertEqual(out.read_text(), "# a\nay\n\n# b\nbee")
