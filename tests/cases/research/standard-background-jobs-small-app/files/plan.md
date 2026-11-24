# recipe-box

## Vision
A personal recipe manager: save recipes from links, plan meals, get a reminder to shop.

## Users
- Me and my partner.

## Hosting
One small VM in my homelab (k3s). Private, reached over Tailscale.

## Growth
- now: 2 users
- next year: 5-10 friends
- maximum potential: ~50 users (friends of friends); no public launch planned
- how fast: a year or more

## Decisions
- test_cmd: `uv run pytest -q`
- D-1: Python 3.12, FastAPI, SQLite | why: simplest | door: two-way | chunk: 1

## Chunks
### Chunk 1: save and list recipes | status: ready
- [ ] T-1: Project skeleton
