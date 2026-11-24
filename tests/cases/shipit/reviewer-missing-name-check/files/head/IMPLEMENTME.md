# T-2: notes show <name>
chunk: 1 | test_cmd: `python3 -m unittest -q` | implementme: 1.0.0
issue: #2

## Change
Add `notes show <name>`: prints the note `notes/<name>.md`.

## Done when
- Given `notes/todo.md` exists, when `notes show todo` runs, then its text prints and exit code is 0.
- Given no such note, when `notes show nope` runs, then `not found` prints to stderr and exit code is 1.
- Given a name containing `/` or `..`, when `notes show <name>` runs, then `invalid name` prints to stderr, no file is read, and exit code is 2.

## Decisions that apply
- D-2: Note names come from the user and are untrusted; only names matching `[A-Za-z0-9_-]+` are valid.

## Files
- touch: `notes.py` (edit): add `read_note` and the `show` command
- touch: `tests/test_notes.py` (edit): tests below
- reuse: `notes.py:NOTES_DIR`: the notes folder

## Tests
- `tests/test_notes.py::ShowTest::test_show_existing`: exit 0
- `tests/test_notes.py::ShowTest::test_show_missing`: exit 1
- `tests/test_notes.py::ShowTest::test_show_invalid_name`: `../secret` -> exit 2, nothing read

## Out of scope
- editing or deleting notes

## Questions
- none
