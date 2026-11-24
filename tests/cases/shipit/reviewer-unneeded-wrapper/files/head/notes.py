"""Tiny notes CLI."""
import re
import sys
from pathlib import Path

NOTES_DIR = Path("notes")
VALID_NAME = re.compile(r"[A-Za-z0-9_-]+")


def list_notes() -> list[str]:
    return sorted(p.stem for p in NOTES_DIR.glob("*.md"))


class NoteStore:
    """Access to notes on disk."""

    def __init__(self, root: Path, suffix: str = ".md", encoding: str = "utf-8") -> None:
        self.root = root
        self.suffix = suffix
        self.encoding = encoding

    def path_for(self, name: str) -> Path:
        return self.root / f"{name}{self.suffix}"

    def read(self, name: str) -> str | None:
        path = self.path_for(name)
        if not path.exists():
            return None
        return path.read_text(encoding=self.encoding)


def main(argv: list[str]) -> int:
    if argv[:1] == ["list"]:
        for name in list_notes():
            print(name)
        return 0
    if argv[:1] == ["show"] and len(argv) == 2:
        if not VALID_NAME.fullmatch(argv[1]):
            print("invalid name", file=sys.stderr)
            return 2
        text = NoteStore(NOTES_DIR).read(argv[1])
        if text is None:
            print("not found", file=sys.stderr)
            return 1
        print(text)
        return 0
    print("usage: notes list | notes show <name>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
