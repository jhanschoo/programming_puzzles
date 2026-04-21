from typing import TextIO


class MaxSegmentTree:
    def __init__(self, size):
        self.n = 1
        while self.n < size:
            self.n <<= 1
        self.tree = [(0, 0)] * (2 * self.n)

    def _push_down(self, node):
        n_val, n_lazy = self.tree[node]
        if n_lazy == 0:
            return

        l_val, l_lazy = self.tree[2 * node]
        r_val, r_lazy = self.tree[2 * node + 1]

        self.tree[2 * node] = (l_val + n_lazy, l_lazy + n_lazy)
        self.tree[2 * node + 1] = (r_val + n_lazy, r_lazy + n_lazy)
        self.tree[node] = (n_val, 0)

    def _update_range(
        self, node: int, start: int, end: int, left: int, right: int, delta: int
    ):
        """Increment the values in the range [left, right] by delta, subject to the
        subtree of the segment tree rooted at `node`.

        Args:
            node (int): the "physical" `self.tree` index of the current node in the segment tree
            start (int): the start of the logical range covered by the current node
            end (int): the end of the logical range covered by the current node
            left (int): the start of the logical range to update
            right (int): the end of the logical range to update
            delta (int): the value to add to the range
        """
        # Case 1: [left, right] is outside of [start, end]
        if right < start or end < left:
            return

        # Case 2: [left, right] contains [start, end]
        if left <= start and end <= right:
            self.tree[node] = (self.tree[node][0] + delta, self.tree[node][1] + delta)
            return

        # Case 3: [left, right] partly overlaps with [start, end]
        self._push_down(node)
        mid = (start + end) // 2
        self._update_range(2 * node, start, mid, left, right, delta)
        self._update_range(2 * node + 1, mid + 1, end, left, right, delta)

        l_val, _ = self.tree[2 * node]
        r_val, _ = self.tree[2 * node + 1]
        self.tree[node] = (max(l_val, r_val), 0)

    def _query_range(self, node, start, end, left, right):
        # Case 1: [left, right] is outside of [start, end]
        if right < start or end < left:
            return float("-inf")

        # Case 2: [left, right] contains [start, end]
        if left <= start and end <= right:
            return self.tree[node][0]

        # Case 3: [left, right] partly overlaps with [start, end]
        self._push_down(node)
        mid = (start + end) // 2
        l_val = self._query_range(2 * node, start, mid, left, right)
        r_val = self._query_range(2 * node + 1, mid + 1, end, left, right)
        return max(l_val, r_val)

    def add_to_range(self, left: int, right: int, delta: int):
        if right < left:
            return
        self._update_range(1, 0, self.n - 1, left, right, delta)

    def query_range(self, left: int, right: int):
        return self._query_range(1, 0, self.n - 1, left, right)

    def query_all(self):
        return self.tree[1][0]


def solve_params(path: list[int], nails: int):
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     path = list(map(int, f.read().strip().split(",")))
    >>> solve_params(path, 8)
    7
    """
    st = MaxSegmentTree(nails)
    # for this part we consider the vertices 0-indexed.
    segments = (
        (s - 1, e - 1) if s <= e else (e - 1, s - 1) for s, e in zip(path, path[1:])
    )
    events = [[] for _ in range(nails)]
    # let (x, y) denote the chord for which we want to evaluate the number of crossings.
    for s, e in segments:
        # 0 <= x < s < y < e < nails
        events[0].append((s + 1, e - 1, 1))
        events[s].append((s + 1, e - 1, -1))

        # 0 <= x = s < e = y < nails (special case: we count once)
        events[s].append((e, e, 1))
        events[s + 1].append((e, e, -1))

        # 0 <= s < x < e < y < nails
        events[s + 1].append((e + 1, nails - 1, 1))
        events[e].append((e + 1, nails - 1, -1))

    global_max = 0
    for es in events:
        for left, right, delta in es:
            st.add_to_range(left, right, delta)
        global_max = max(global_max, st.query_all())
    return global_max


def solve(f: TextIO) -> str:
    path = list(map(int, f.read().strip().split(",")))
    return str(solve_params(path, 256))
