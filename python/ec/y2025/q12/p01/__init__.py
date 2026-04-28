from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f_ex:
    ...     solve(f_ex)
    '16'
    """
    grid = [[int(c) for c in line.strip()] for line in f if line.strip()]
    if not grid or not grid[0]:
        return "0"
    R = len(grid)
    C = len(grid[0])

    visited = {(0, 0)}
    stack = [(0, 0)]

    while stack:
        r, c = stack.pop()
        current_size = grid[r][c]

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in visited:
                if grid[nr][nc] <= current_size:
                    visited.add((nr, nc))
                    stack.append((nr, nc))

    return str(len(visited))
