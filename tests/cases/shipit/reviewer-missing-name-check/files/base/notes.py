"""Tiny notes CLI."""
import sys
from pathlib import Path

NOTES_DIR = Path("notes")


def list_notes() -> list[str]:
    return sorted(p.stem for p in NOTES_DIR.glob("*.md"))


def main(argv: list[str]) -> int:
    if argv[:1] == ["list"]:
        for name in list_notes():
            print(name)
        return 0
    print("usage: notes list", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
