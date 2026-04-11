from collections import Counter
from typing import TextIO

def solve_params(draft: str, reps: int, distance: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     draft = f.read().strip()
    >>> solve_params(draft, 1, 10)
    34
    >>> solve_params(draft, 2, 10)
    72
    """
    people = Counter()
    rep_len = len(draft)
    draft = 3 * draft
    aug_len = len(draft)
    pairings = 0
    usual_mul = reps - 2
    for i in range(distance):
        people[draft[i]] += 1
    for i in range(aug_len):
        c = draft[i]
        if i + distance < aug_len:
            people[draft[i + distance]] += 1
        if 0 <= i - distance - 1:
            people[draft[i - distance - 1]] -= 1
        if c.islower():
            mul = usual_mul if rep_len <= i < rep_len * 2 else 1
            pairings += mul * people[c.upper()]
    return pairings

def solve(f: TextIO) -> str:
    pairings = solve_params(f.read().strip(), 1000, 1000)

    return f"{pairings}"
