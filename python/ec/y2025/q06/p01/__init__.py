from collections import Counter
from typing import TextIO

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '5'
    """
    draft = f.read().strip()
    people = Counter()
    pairings = 0
    for c in draft:
        people[c] += 1
        if c == 'a':
            pairings += people['A']
    return f"{pairings}"
