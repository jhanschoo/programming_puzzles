from typing import TextIO


def solve_params(path: list[int], nails: int):
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     path = list(map(int, f.read().strip().split(",")))
    >>> solve_params(path, 8)
    4
    """
    return sum(1 for (s, e) in zip(path, path[1:]) if abs(s - e) * 2 == nails)


def solve(f: TextIO) -> str:
    path = list(map(int, f.read().strip().split(",")))
    return str(solve_params(path, 32))
