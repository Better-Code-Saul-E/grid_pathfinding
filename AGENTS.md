# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (`list`, iterative only)

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`) unless user asks otherwise.
- Keep function signatures in `pathfinding.py` unchanged.
- DFS must be iterative (no recursion).
- BFS must use `collections.deque`.
- Use `visited` set and `parent` dict for path reconstruction.
- Keep changes minimal and keep `main()` runnable.

## Output Contract
Running `python pathfinding.py` must:
- Run BFS and DFS on at least 2 maps.
- Print found/path length/visited count.
- Print rendered map with overlays.
