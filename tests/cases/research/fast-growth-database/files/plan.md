# drop-pass

## Vision
Event organizers post a limited drop (tickets, merch); fans claim one each, first come first served.

## Users
- A few organizer friends at launch; their fans.

## Hosting
Cloud, region us-east, budget-conscious.

## Growth
- now: 3 organizers, ~200 fans, a few drops a month
- next year: ~50 organizers, ~20k fans
- maximum potential: 1M fans, drops where 100k people claim within the same minute
- how fast: weeks, if one big artist uses it and it spreads

## Decisions
- test_cmd: `uv run pytest -q`
- D-1: Python 3.12, FastAPI | why: user knows it | door: two-way | chunk: 1

## Chunks
### Chunk 1: post a drop, claim one | status: draft
- needs: architecture
- to figure out:
  - where drops and claims are stored
