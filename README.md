# BFS + DFS Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

## What to look for
- BFS returns a shortest path in this unweighted 4-direction grid.
- DFS may return a longer path depending on exploration order.
- Output includes `found`, `path_len`, `visited`, and map overlays.

## Reflection
On `EXAMPLE_MAP_2`, DFS explores in a depth-first pattern and can commit to long corridors before trying alternatives. BFS expands in wavefront layers, so the first time it reaches `G` is guaranteed to be along a shortest path (fewest steps) in an unweighted graph.

In these maps, visited counts can differ based on corridor layout and neighbor order. BFS often visits more nearby tiles uniformly, while DFS can go deep quickly and either find a path early or spend effort in a dead-end branch first.

Why BFS is shortest here:
1. Each move has equal cost (1 step).
2. BFS explores all nodes at distance `d` before any at distance `d+1`.
3. Therefore the first discovered path to `G` has minimum edge count.

Why DFS is not shortest:
1. DFS follows one branch deeply before backtracking.
2. It may reach `G` through a long route before ever checking a shorter branch.
3. So DFS is useful for reachability, but not shortest-path guarantees in this setting.

## Monster Chase (Turn-Based)
A required game idea is implemented as `run_monster_chase(mode)` in `pathfinding.py`.

- Map has player `P`, monster `M`, walls `#`, floor `.` and exit `G`.
- Player moves with WASD (blocked by walls).
- Monster recomputes path to player every turn using `mode="BFS"` or `mode="DFS"`.
- Monster moves one step along its computed path.
- If monster reaches player, you lose. If player reaches `G`, you win.

Try in a Python REPL:
```python
from pathfinding import run_monster_chase
run_monster_chase("BFS")
```
