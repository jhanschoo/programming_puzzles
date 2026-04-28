import itertools
from typing import TextIO


class UnionFind:
    def __init__(self, size: int):
        self.parents = list(range(size))
        self.sizes = [1] * size

    def find(self, i: int) -> int:
        path = []
        while self.parents[i] != i:
            path.append(i)
            i = self.parents[i]
        for node in path:
            self.parents[node] = i
        return i

    def union(self, i: int, j: int):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.sizes[root_i] < self.sizes[root_j]:
                root_i, root_j = root_j, root_i
            self.parents[root_j] = root_i
            self.sizes[root_i] += self.sizes[root_j]

    def size(self, i: int) -> int:
        return self.sizes[self.find(i)]


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '12'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '36'
    """
    samples = [line.strip().split(":")[1] for line in f if line.strip()]
    n = len(samples)
    uf = UnionFind(n)

    for (i, s1), (j, s2), (k, s3) in itertools.combinations(enumerate(samples), 3):
        if (
            all(c1 in (c2, c3) for c1, c2, c3 in zip(s1, s2, s3))
            or all(c2 in (c1, c3) for c1, c2, c3 in zip(s1, s2, s3))
            or all(c3 in (c1, c2) for c1, c2, c3 in zip(s1, s2, s3))
        ):
            uf.union(i, j)
            uf.union(j, k)

    largest_set = -1
    largest_size = -1
    for i in range(n):
        current_set = uf.find(i)
        current_size = uf.size(current_set)
        if current_size > largest_size:
            largest_size = current_size
            largest_set = current_set

    total = sum(i + 1 for i in range(n) if uf.find(i) == largest_set)
    return str(total)
