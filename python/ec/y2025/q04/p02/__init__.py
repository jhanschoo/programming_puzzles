from typing import TextIO
from fractions import Fraction
from math import ceil

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '625000000000'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '1274509803922'
    """
    last = first = next(f)
    for g in f:
        last = g
    turns = ceil(Fraction(10000000000000) / Fraction(first) * Fraction(last))

    return f"{turns}"
