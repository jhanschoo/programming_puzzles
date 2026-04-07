from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    'Elarzris'
    """
    names, instructions = f.read().strip().split()
    names = names.split(",")
    num_names = len(names)
    instructions = instructions.split(",")
    idx = 0
    for instruction in instructions:
        direction, count = instruction[0], int(instruction[1:])
        if direction == "L":
            count = -count
        idx = (idx + count) % num_names
    return names[idx]
