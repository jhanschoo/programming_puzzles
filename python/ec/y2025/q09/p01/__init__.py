from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '414'
    """
    lines = [line.strip().split(":")[1] for line in f if line.strip()]
    if not lines:
        return ""
    s1, s2, s3 = lines

    s12 = s13 = s23 = 0
    child1 = child2 = child3 = True

    for c1, c2, c3 in zip(s1, s2, s3):
        c12 = c1 == c2
        c13 = c1 == c3
        c23 = c2 == c3

        if c12:
            s12 += 1
        if c13:
            s13 += 1
        if c23:
            s23 += 1

        child1 = child1 and (c12 or c13)
        child2 = child2 and (c12 or c23)
        child3 = child3 and (c13 or c23)

    return str(
        max(
            s12 * s13 * int(child1),
            s12 * s23 * int(child2),
            s13 * s23 * int(child3),
        )
    )
