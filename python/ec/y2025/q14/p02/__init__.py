from typing import TextIO


def solve_params(grid: list[list[str]], rounds: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     grid = [list(line.strip()) for line in f if line.strip()]
    >>> solve_params(grid, 10)
    200
    """
    R = len(grid)
    C = len(grid[0])

    current = [row[:] for row in grid]
    total_active = 0

    for _ in range(rounds):
        next_grid = [["." for _ in range(C)] for _ in range(R)]
        for r in range(R):
            for c in range(C):
                # Count diagonal neighbors
                count = 0
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C:
                        if current[nr][nc] == "#":
                            count += 1

                if current[r][c] == "#":
                    if count % 2 == 1:
                        next_grid[r][c] = "#"
                else:
                    if count % 2 == 0:
                        next_grid[r][c] = "#"

        current = next_grid
        total_active += sum(row.count("#") for row in current)

    return total_active


def solve(f: TextIO) -> str:
    grid = [list(line.strip()) for line in f if line.strip()]
    return str(solve_params(grid, 2025))
