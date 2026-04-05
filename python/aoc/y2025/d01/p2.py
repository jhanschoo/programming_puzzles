from pathlib import Path
from typing import TextIO


def solve(in_: TextIO) -> str:
    """
    >>> solve(open(Path(__file__).parent / "diagnostic.txt"))
    '3'
    """
    return str(max(int(line) for line in in_))


if __name__ == "__main__":
    import sys
    print(solve(open(sys.argv[1])))
