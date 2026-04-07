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

def cycle(w: tuple[int, int], A: tuple[int, int]) -> tuple[int, int]:
    return add(div(mul(w, w), (10, 10)), A)

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '[357,862]'
    """
    w = (0, 0)
    _, A = f.read().strip().split("=")
    Ax, Ay = A[1:-1].split(",")
    Ax, Ay = int(Ax), int(Ay)
    A = (Ax, Ay)
    for _ in range(3):
        w = cycle(w, A)

    return f"[{w[0]},{w[1]}]"
