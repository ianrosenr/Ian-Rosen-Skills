# docs/architecture/

How the app is built, explained for someone who has never written code. Open `index.html` in a browser.

- `index.html`: the page.
- `architecture.d2` -> `architecture.svg`: the diagram (D2 source, rendered SVG).
- `video/scenes.py` -> `architecture.mp4`: the narrated video (Manim scene, Kokoro voice). `video/narrate.py` is the voice helper.
- `build.sh`: rebuilds the SVG and MP4. Needs `brew install d2 cairo pango pkgconf espeak-ng` and uv.

Updated by the last line item of every chunk. Decisions behind it: `docs/adr/`.
