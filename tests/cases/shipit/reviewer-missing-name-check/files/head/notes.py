"""Tiny notes CLI."""
import sys
from pathlib import Path

NOTES_DIR = Path("notes")


def list_notes() -> list[str]:
    return sorted(p.stem for p in NOTES_DIR.glob("*.md"))


def read_note(name: str) -> str | None:
    path = NOTES_DIR / f"{name}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def main(argv: list[str]) -> int:
    if argv[:1] == ["list"]:
        for name in list_notes():
            print(name)
        return 0
    if argv[:1] == ["show"] and len(argv) == 2:
        text = read_note(argv[1])
        if text is None:
            print("not found", file=sys.stderr)
            return 1
        print(text)
        return 0
    print("usage: notes list | notes show <name>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
