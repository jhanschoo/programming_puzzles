from typing import TextIO
import math

def add(w1: tuple[int, int], w2: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = w1
    x2, y2 = w2
    return (x1 + x2, y1 + y2)

def mul(w1: tuple[int, int], w2: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = w1
    x2, y2 = w2
    return (x1 * x2 - y1 * y2, x1 * y2 + y1 * x2)

def div(w1: tuple[int, int], w2: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = w1
    x2, y2 = w2
    # nonstandard!
    return (math.trunc(x1 / x2), math.trunc(y1 / y2))

def cycle(w: tuple[int, int], C: tuple[int, int]) -> tuple[int, int]:
    return add(div(mul(w, w), (100_000, 100_000)), C)

def should_engrave(C: tuple[int, int]) -> bool:
    w = (0, 0)
    for n in range(100):
        w = cycle(w, C)
        for i in w:
            if not (-1_000_000 <= i <= 1_000_000):
                # print("?", n, w)
                return False
    # print("!", w)
    return True

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '4076'
    """
    _, A = f.read().strip().split("=")
    Ax, Ay = A[1:-1].split(",")
    Ax, Ay = int(Ax), int(Ay)

    engraving_points = sum(should_engrave((Cx, Cy)) for Cx in range(Ax, Ax + 1001, 10) for Cy in range(Ay, Ay + 1001, 10))

    return f"{engraving_points}"