import itertools
from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '1245'
    """
    samples = [line.strip().split(":")[1] for line in f if line.strip()]
    total = 0

    for s1, s2, s3 in itertools.combinations(samples, 3):
        child1 = all(c1 in (c2, c3) for c1, c2, c3 in zip(s1, s2, s3))
        child2 = all(c2 in (c1, c3) for c1, c2, c3 in zip(s1, s2, s3))
        child3 = all(c3 in (c1, c2) for c1, c2, c3 in zip(s1, s2, s3))

        if child1:
            total += sum(c1 == c2 for c1, c2 in zip(s1, s2)) * sum(c1 == c3 for c1, c3 in zip(s1, s3))
        if child2:
            total += sum(c2 == c1 for c1, c2 in zip(s1, s2)) * sum(c2 == c3 for c2, c3 in zip(s2, s3))
        if child3:
            total += sum(c3 == c1 for c1, c3 in zip(s1, s3)) * sum(c3 == c2 for c2, c3 in zip(s2, s3))

    return str(total)
