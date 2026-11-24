#!/usr/bin/env bash
# Rebuild the architecture diagram (D2) and video (Manim + Kokoro narration).
# Needs: brew install d2 cairo pango pkgconf espeak-ng; uv. First run downloads the voice model.
set -euo pipefail
cd "$(dirname "$0")"

d2 architecture.d2 architecture.svg

cd video
rm -rf media/videos
uv run -q --python 3.12 --with manim --with kokoro --with soundfile \
  manim --resolution 1920,1080 --frame_rate 30 --disable_caching scenes.py Architecture
cp media/videos/scenes/1080p30/Architecture.mp4 ../architecture.mp4
echo "built: architecture.svg, architecture.mp4"
