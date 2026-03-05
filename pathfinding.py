from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]


EXAMPLE_MAP_1 = """
#######
#S...G#
#.###.#
#.....#
#######
""".strip("\n")

EXAMPLE_MAP_2 = """
#########
#S.....G#
#.#.###.#
#.#.....#
#.#######
#.......#
#########
""".strip("\n")

MONSTER_MAP = """
#############
#P....#....G#
#.##..#..##.#
#....M#.....#
#############
""".strip("\n")

MODE = "BFS"  # Choose from: "BFS" or "DFS"


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Grid text is empty")

    width = len(lines[0])
    if any(len(line) != width for line in lines):
        raise ValueError("Grid must be rectangular")

    grid: Grid = []
    start: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, line in enumerate(lines):
        row: List[str] = []
        for c, ch in enumerate(line):
            if ch not in {"#", ".", "S", "G", "P", "M"}:
                raise ValueError(f"Invalid grid character: {ch!r}")
            if ch in {"S", "P"}:
                if start is not None:
                    raise ValueError("Grid must contain exactly one start")
                start = (r, c)
            if ch == "G":
                if goal is not None:
                    raise ValueError("Grid must contain exactly one goal")
                goal = (r, c)
            row.append(ch)
        grid.append(row)

    if start is None or goal is None:
        raise ValueError("Grid must contain one start (S/P) and one goal (G)")

    return grid, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    rows, cols = len(grid), len(grid[0])
    r, c = node
    candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    valid: List[Pos] = []
    for nr, nc in candidates:
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            valid.append((nr, nc))
    return valid


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if start == goal:
        return [start]
    if goal not in parent:
        return None

    path: List[Pos] = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    q: deque[Pos] = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while q:
        cur = q.popleft()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            q.append(nxt)

    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack: List[Pos] = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        cur = stack.pop()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in reversed(neighbors(grid, cur)):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            stack.append(nxt)

    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules:
    - path tiles shown as '*'
    - visited tiles shown as '+'
    - preserve S/P and G
    """
    out = [row[:] for row in grid]
    path_set = set(path or [])
    visited_set = visited or set()

    for r in range(len(out)):
        for c in range(len(out[0])):
            cell = out[r][c]
            pos = (r, c)
            if cell in {"S", "G", "P", "M"}:
                continue
            if pos in path_set:
                out[r][c] = "*"
            elif pos in visited_set and cell != "#":
                out[r][c] = "+"

    return "\n".join("".join(row) for row in out)


def _path_metrics(path: Optional[List[Pos]], visited: Set[Pos]) -> str:
    return f"found={path is not None} path_len={(len(path) if path else None)} visited={len(visited)}"


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

    print("=" * 60)
    print(label)
    print("- Raw map")
    print(render(grid))

    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    print("\n- BFS")
    print(_path_metrics(path_bfs, visited_bfs))
    print(render(grid, path=path_bfs, visited=visited_bfs))

    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    print("\n- DFS")
    print(_path_metrics(path_dfs, visited_dfs))
    print(render(grid, path=path_dfs, visited=visited_dfs))


def run_monster_chase(mode: str = MODE) -> None:
    """Simple turn-based demo with WASD player and BFS/DFS monster chasing the player."""
    text = MONSTER_MAP.replace("P", "S").replace("M", ".")
    grid, player, goal = parse_grid(text)

    monster = None
    raw = [list(line) for line in MONSTER_MAP.splitlines()]
    for r, row in enumerate(raw):
        for c, ch in enumerate(row):
            if ch == "M":
                monster = (r, c)
    if monster is None:
        raise ValueError("Monster map requires one M")

    controls = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
    print("\nMonster Chase! Move with WASD, q to quit.")
    print(f"Monster mode: {mode}")

    while True:
        display = [row[:] for row in grid]
        pr, pc = player
        mr, mc = monster
        display[pr][pc] = "P"
        display[mr][mc] = "M"
        print(render(display))

        if player == goal:
            print("You reached G. You win!")
            return
        if monster == player:
            print("Monster caught you. You lose!")
            return

        move = input("Move [W/A/S/D or q]: ").strip().lower()
        if move == "q":
            print("Quit.")
            return
        if move not in controls:
            print("Invalid move.")
            continue

        dr, dc = controls[move]
        candidate = (player[0] + dr, player[1] + dc)
        if candidate in neighbors(grid, player):
            player = candidate

        chase_grid = [row[:] for row in grid]
        chase_grid[monster[0]][monster[1]] = "S"
        chase_grid[player[0]][player[1]] = "G"
        _, m_start, m_goal = parse_grid("\n".join("".join(row) for row in chase_grid))

        if mode.upper() == "BFS":
            m_path, _ = bfs_path(chase_grid, m_start, m_goal)
        else:
            m_path, _ = dfs_path(chase_grid, m_start, m_goal)

        if m_path and len(m_path) > 1:
            monster = m_path[1]


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)
    print("\nTip: call run_monster_chase('BFS') or run_monster_chase('DFS') to play.")


if __name__ == "__main__":
    main()
