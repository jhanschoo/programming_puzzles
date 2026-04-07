from typing import TextIO
import math

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "diagnostic.txt") as f:
    ...     solve(f)
    '6'
    """
    pos = 50
    zero_count = 0
    for line in f:
        direction, count = line[0], int(line[1:])
        match direction:
            case "L":
                next_pos = pos - count
            case "R":
                next_pos = pos + count
        base_count = int((next_pos <= 0 < pos) or (pos < 0 <= next_pos))
        excess_counts = math.trunc(next_pos / 100)
        pos = next_pos - (excess_counts * 100)
        zero_count += base_count + abs(excess_counts)
    return str(zero_count)


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        print(solve(f))
