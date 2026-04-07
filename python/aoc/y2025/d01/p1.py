from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "diagnostic.txt") as f:
    ...     solve(f)
    '3'
    """
    pos = 50
    zero_count = 0
    for line in f:
        direction, count = line[0], int(line[1:])
        match direction:
            case "L":
                pos -= count
            case "R":
                pos += count
        pos = pos % 100
        if pos == 0:
            zero_count += 1
    return str(zero_count)


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        print(solve(f))
