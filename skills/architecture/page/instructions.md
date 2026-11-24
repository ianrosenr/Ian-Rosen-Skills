# Architecture page: instructions

For the line item "Architecture page, diagram and video for chunk N". Output lives in the app repo at `docs/architecture/`:

| File | What it is |
|---|---|
| `index.html` | The page. Opens straight from disk: `open docs/architecture/index.html`. |
| `architecture.d2` -> `architecture.svg` | The diagram, written in D2 (a text-to-diagram language), rendered to SVG. Both committed. |
| `video/scenes.py` -> `architecture.mp4` | The video, written as a Manim scene with Kokoro narration. Both committed; `video/media/` is not. |
| `video/narrate.py`, `build.sh`, `README.md` | Copied from the templates; change only if broken. |

First time (folder missing): copy every file from this directory's `templates/` into `docs/architecture/` keeping the layout, add a `docs/` line to AGENTS.md Layout if missing, then fill them in.

## The reader knows nothing
Write for someone who has never written code. This rule beats brevity.
- Spell out every acronym the first time it appears in each section, and in the video narration: "API (Application Programming Interface)". Every acronym also gets a glossary entry. No exceptions: HTTP, URL, JSON, SQL, CLI, CI, DNS, VM, OS, all of them.
- Explain every technical term in plain words before using it: server, database, request, endpoint, queue, cache, container, deploy, and so on. Each one gets a glossary entry.
- One analogy family for the whole app, chosen once and reused in the page and the video (e.g. a restaurant: the browser is the customer, the server the waiter, the database the pantry). Every component and every step gets its analogy from that family. Keep the analogy in the page's first section so later chunks reuse it.
- Short sentences. One idea each. No "simply", "just", "obviously".

## Content (follow the template's sections, in order)
1. What the app does: 2-4 plain sentences. Who uses it and what they get.
2. The big picture: the diagram, then the analogy that maps onto it.
3. The video.
4. Step by step: one real user action, numbered from start to finish (e.g. "you type a note and press Enter"). Each step: what happens, which part does it, what data moves, the analogy. Step numbers match the numbers on the diagram's arrows. More than one key action -> one numbered walk-through each.
5. The parts: one card per component: what it is, what it does here, its analogy, where it lives in the code (folder), why we chose it (link the ADR).
6. Glossary: every acronym and term on the page, alphabetical: the full form, a plain definition, an everyday example.
7. Decisions: every ADR in `docs/adr/`, one line each, linked.
8. What changed: newest chunk first, 1-3 lines per chunk.

## Accuracy
- Describe what exists in the code at the end of this chunk. Read the code; don't trust the plan alone.
- Parts that are planned but not built: show them greyed out, labeled "coming in chunk N". Never describe them as working.
- Update, don't rewrite: keep earlier chunks' explanations that are still true, fix what changed, add a "What changed" entry.

## Diagram (D2)
- One box per component, 12 or fewer. Label = plain name on the first line, technology in small text on the second (e.g. "Note storage\nSQLite database").
- Every arrow labeled with what moves along it, and numbered to match the step-by-step.
- Trust boundaries (where data crosses from something we don't control, like the internet or a user's input) are dashed containers, labeled.
- Planned parts: `style.opacity: 0.35` and "(chunk N)" in the label.
- Render: `d2 architecture.d2 architecture.svg` (build.sh does this). Check it in a browser: text, arrows and numbers all readable.

## Video (Manim + Kokoro)
- 1-3 minutes. Same steps, same analogy, same plain words as the page. Acronyms spelled out aloud.
- Structure: what the app does -> build the diagram up one part at a time (each part appears as the narration explains it) -> walk the numbered steps with a moving dot or highlight -> recap in one sentence.
- One idea per narration line. Each `self.say(...)` returns its length; give animations that run time so picture and voice stay in sync.
- Shapes and labels only; no clip art. Text at least 24pt. Plain-name labels match the diagram.
- Render: `docs/architecture/build.sh` (needs `brew install d2 cairo pango pkgconf espeak-ng` and uv; first run downloads the voice model).

## Done when (copy these into IMPLEMENTME.md)
- Given the page, when every acronym and technical term is checked, then each is spelled out or explained at first use and has a glossary entry.
- Given the page and video, then every component and step has an analogy from the one analogy family.
- Given the step-by-step section, then each step names the part, the data, and its arrow number on the diagram.
- Given the code at the end of this chunk, then the page, diagram and video describe it accurately; planned parts are marked "coming in chunk N".
- Given `docs/architecture/build.sh` runs, then `architecture.svg` and `architecture.mp4` are rebuilt without errors and the video has narration audio.
- Given `open docs/architecture/index.html`, then the diagram shows and the video plays.
