from typing import TextIO


def solve_params(nums: list[int]) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     nums = [int(line.strip().strip(".")) for line in f if line.strip()]
    >>> solve_params(nums)
    11
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     nums = [int(line.strip().strip(".")) for line in f if line.strip()]
    >>> solve_params(nums)
    1579
    """
    cols = list(nums)
    n = len(cols)
    round_count = 0

    # Phase 1: More birds to next column if it has fewer
    while True:
        moved = False
        for i in range(n - 1):
            if cols[i] > cols[i + 1]:
                cols[i] -= 1
                cols[i + 1] += 1
                moved = True
        if not moved:
            break
        round_count += 1

    # Phase 2: More birds from next column if it has more
    while True:
        moved = False
        for i in range(n - 1):
            if cols[i] < cols[i + 1]:
                cols[i] += 1
                cols[i + 1] -= 1
                moved = True
        if not moved:
            break
        round_count += 1

    return round_count


def solve(f: TextIO) -> str:
    nums = [int(line.strip().strip(".")) for line in f if line.strip()]
    return str(solve_params(nums))
