from pathlib import Path

import notes


def export(out: Path) -> None:
    parts = [f"# {name}\n{(notes.NOTES_DIR / f'{name}.md').read_text(encoding='utf-8')}" for name in notes.list_notes()]
    out.write_text("\n\n".join(parts), encoding="utf-8")
