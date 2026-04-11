from typing import TextIO
from fractions import Fraction
from math import floor

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '400'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '6818'
    """
    last = teeth = Fraction(next(f))
    for g in f:
        g = g.replace('|', '/')
        last = g
        if '/' in g:
            g = g.replace('\n', '')
            teeth = teeth / Fraction(g)
    turns = floor(Fraction(100) * Fraction(teeth) / Fraction(last))

    return f"{turns}"
