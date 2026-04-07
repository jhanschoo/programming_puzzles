from typing import TextIO

def parse_int(s: str) -> int:
    return int(s) if s else 0

def to_str(i: int) -> str:
    return str(i) if i else ""

def extract_bounds(l_str: str, u_str: str) -> tuple[int, int, int]:
    """Extract bounds for accumulating invalid IDs that range from `l_str` (inclusive) to `u_str` (exclusive)

    An invalid ID `s` is a nonempty string of digits with no leading 0,
    such that some `w` and `n` > 2 satisfies `s == w * n`. The returns are as follows:
    `l` and `u` are simply `l_str` and `u_str` as integers.
    `w_max` is a power of 10 that is an exclusive upper bound for valid `w`. `w_max_p` is that power.

    Args:
        l_str (str): integer inclusive lower bound of range as str
        u_str (str): integer exclusive upper bound of range as str

    Returns:
        tuple[int, int]: (`l`, `u`, `w_max_p`)
    """
    l, u = parse_int(l_str), parse_int(u_str)
    w_max_p = len(u_str) // 2
    return l, u, w_max_p

def sum_invalid_ids(l_str: str, u_str: str) -> int:
    l, u, w_max_p = extract_bounds(l_str, u_str)
    invalid_ids = set()
    for p in range(1, w_max_p + 1):
        for n in range(10 ** (p-1), 10 ** p):
            w = n
            while w < l or w < 10:
                w = n + w * 10 ** p
            while w <= u:
                invalid_ids.add(w)
                w = n + w * 10 ** p
    return sum(invalid_ids)

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "diagnostic.txt") as f:
    ...     solve(f)
    '4174379265'
    """
    id_ranges_str = (pair.split("-") for pair in f.read().strip().split(","))
    return str(sum(sum_invalid_ids(l_str, u_str) for l_str, u_str in id_ranges_str))


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        print(solve(f))
