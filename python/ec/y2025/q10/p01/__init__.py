from typing import TextIO


def solve_params(grid: list[str], max_moves: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     grid = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid, 3)
    27
    """
    r, c = -1, -1
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == "D":
                r, c = i, j
                break

    R, C = len(grid), len(grid[0])
    visited = {(r, c)}
    ans = 0

    frontier = [(r, c)]
    for _ in range(max_moves):
        next_frontier = []
        for curr_r, curr_c in frontier:
            for dr, dc in [
                (-2, -1),
                (-2, 1),
                (-1, -2),
                (-1, 2),
                (1, -2),
                (1, 2),
                (2, -1),
                (2, 1),
            ]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    next_frontier.append((nr, nc))
                    if grid[nr][nc] == "S":
                        ans += 1
        frontier = next_frontier

    return ans


def solve(f: TextIO) -> str:
    grid = [line.strip() for line in f if line.strip()]
    return str(solve_params(grid, 4))
