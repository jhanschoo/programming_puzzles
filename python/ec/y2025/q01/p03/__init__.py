from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    'Drakzyph'
    """
    names, instructions = f.read().strip().split()
    names = names.split(",")
    num_names = len(names)
    instructions = instructions.split(",")
    for instruction in instructions:
        direction, i = instruction[0], int(instruction[1:])
        if direction == "L":
            i = -i
        i %= num_names
        names[0], names[i] = names[i], names[0]
    return names[0]
