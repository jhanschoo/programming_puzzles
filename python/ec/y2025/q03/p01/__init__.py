from typing import TextIO

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '29'
    """

    return f"{sum(set(map(int, f.read().strip().split(","))))}"
