from collections import Counter
from typing import TextIO


def solve_params(grid: list[str]) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     grid1 = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid1)
    15
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     grid2 = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid2)
    8
    >>> with open(Path(__file__).parent / "example3.txt") as f:
    ...     grid3 = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid3)
    44
    >>> with open(Path(__file__).parent / "example4.txt") as f:
    ...     grid4 = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid4)
    4406
    >>> with open(Path(__file__).parent / "example5.txt") as f:
    ...     grid5 = [line.strip() for line in f if line.strip()]
    >>> solve_params(grid5)
    13033988838
    """
    R = len(grid)
    C = len(grid[0])

    dragon_pos = None
    initial_sheep_rows = [-2] * C  # -2: nonexistent
    hideouts = set()

    for r in range(R):
        for c in range(C):
            match grid[r][c]:
                case "D":
                    dragon_pos = (r, c)
                case "S":
                    initial_sheep_rows[c] = r
                case "#":
                    hideouts.add((r, c))

    # Initial state: (dragon_pos, sheep_rows)
    # Turn: starts with sheep.
    sheep_to_move = Counter({(dragon_pos, tuple(initial_sheep_rows)): 1})
    total_sequences = 0

    while sheep_to_move:
        # 1. Sheep turn
        dragon_to_move = Counter()
        for (d_pos, s_rows), mult in sheep_to_move.items():
            turn_can_be_made = False
            d_pos_is_hideout = d_pos in hideouts
            for c in range(C):
                r = s_rows[c]
                if r >= 0:  # Sheep exists on the board
                    nr = r + 1
                    if nr == R:
                        turn_can_be_made = True
                    elif (nr, c) != d_pos or d_pos_is_hideout:
                        turn_can_be_made = True
                        next_s_rows = tuple(
                            nr if i == c else s_rows[i] for i in range(C)
                        )
                        dragon_to_move[(d_pos, next_s_rows)] += mult

            if not turn_can_be_made:
                # Turn skipped
                dragon_to_move[(d_pos, s_rows)] += mult

        if not dragon_to_move:
            break

        # 2. Dragon turn
        sheep_to_move = next_sheep_to_move = Counter()
        for (d_pos, s_rows), mult in dragon_to_move.items():
            dr, dc = d_pos
            for ddr, ddc in [
                (-2, -1),
                (-2, 1),
                (-1, -2),
                (-1, 2),
                (1, -2),
                (1, 2),
                (2, -1),
                (2, 1),
            ]:
                nr, nc = dr + ddr, dc + ddc
                if 0 <= nr < R and 0 <= nc < C:
                    next_d_pos = (nr, nc)
                    # Check if dragon eats a sheep
                    is_eating = next_d_pos not in hideouts and s_rows[nc] == nr
                    next_s_rows = tuple(
                        -1 if c == nc and is_eating else s_rows[c] for c in range(C)
                    )

                    if all(
                        r < 0 for r in next_s_rows
                    ):  # All eaten (-1) or nonexistent (-2)
                        total_sequences += mult
                    else:
                        next_sheep_to_move[(next_d_pos, next_s_rows)] += mult

    return total_sequences


def solve(f: TextIO) -> str:
    grid = [line.strip() for line in f if line.strip()]
    return str(solve_params(grid))
