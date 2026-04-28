from collections import Counter
from typing import TextIO


def solve_params(grid: list[str], max_rounds: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     grid = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid, 3)
    27
    """
    dr, dc = -1, -1
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'D':
                dr, dc = r, c
                break

    R, C = len(grid), len(grid[0])
    hideouts = {(r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == "#"}

    # Store sheep as { (r, c): count }
    sheep = Counter((r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == "S")

    total_eaten = 0
    dragon_pos = {(dr, dc)}

    for _ in range(max_rounds):
        # 1. Dragon moves to ALL possible variants
        new_dragon_pos = set()
        for r, c in dragon_pos:
            for drr, dcc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                nr, nc = r + drr, c + dcc
                if 0 <= nr < R and 0 <= nc < C:
                    new_dragon_pos.add((nr, nc))
        dragon_pos = new_dragon_pos

        # 2. Check if dragon eats sheep at current position
        for pos in dragon_pos:
            if pos not in hideouts and pos in sheep:
                total_eaten += sheep[pos]
                del sheep[pos]

        # 3. Sheep move down
        new_sheep = Counter()
        for (r, c), count in sheep.items():
            nr = r + 1
            if nr < R:
                if (nr, c) in dragon_pos and (nr, c) not in hideouts:
                    total_eaten += count
                else:
                    new_sheep[(nr, c)] += count
        sheep = new_sheep

    return total_eaten


def solve(f: TextIO) -> str:
    grid = [line.strip() for line in f if line.strip()]
    return str(solve_params(grid, 20))
