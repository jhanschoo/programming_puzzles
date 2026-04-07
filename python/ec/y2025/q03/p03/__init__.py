from typing import TextIO
from collections import Counter

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '3'
    """
    crates = Counter(f.read().strip().split(","))
    crates.most_common(1)[0][1]

    return f"{crates.most_common(1)[0][1]}"
