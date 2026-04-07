from typing import TextIO
from fractions import Fraction
from math import floor

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '32400'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '15888'
    """
    last = first = next(f)
    for g in f:
        last = g
    turns = floor(Fraction(2025) * Fraction(first) / Fraction(last))

    return f"{turns}"
