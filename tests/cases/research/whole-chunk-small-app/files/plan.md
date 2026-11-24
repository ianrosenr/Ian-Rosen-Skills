# recipe-box

## Vision
A personal recipe manager: save recipes from links, plan meals, get a reminder to shop.

## Users
- Me and my partner; later a few friends.

## Hosting
One small VM in my homelab (k3s). Private, reached over Tailscale.

## Growth
Maybe 5-10 friends within a year. No plans beyond that.

## Decisions
- test_cmd: `uv run pytest -q`
- D-1: Python 3.12, FastAPI, SQLite | why: simplest | door: two-way | chunk: 1

## Chunks
### Chunk 1: save and list recipes | status: done
- [x] T-1: Project skeleton
- [x] T-2: Save a recipe from a link

### Chunk 2: sharing with friends | status: draft
- goal: friends can sign in and see recipes I share with them
- needs: architecture
- to figure out:
  - how friends sign in
  - how sharing permissions are stored
  - how friends reach the app (it's Tailscale-only today)
