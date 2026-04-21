from typing import TextIO


class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def increment(self, i: int, delta: int = 1):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def sum_range_inclusive(self, s: int, e: int) -> int:
        return self.sum(e) - self.sum(s - 1)


def solve_params(path: list[int], nails: int):
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     path = list(map(int, f.read().strip().split(",")))
    >>> solve_params(path, 8)
    21
    """
    ft = FenwickTree(nails)
    segments = sorted(
        ((s, e) if s <= e else (e, s) for s, e in zip(path, path[1:])),
        key=lambda x: (x[0], -x[1]),
    )
    total = 0
    for s, e in segments:
        if s + 1 <= e - 1:
            total += ft.sum_range_inclusive(s + 1, e - 1)
        ft.increment(e)
    return total


def solve(f: TextIO) -> str:
    path = list(map(int, f.read().strip().split(",")))
    return str(solve_params(path, 256))
