from typing import TextIO

def parse_int(s: str) -> int:
    return int(s) if s else 0

def to_str(i: int) -> str:
    return str(i) if i else ""

def normalize_invalid_id_range(l_str: str, u_str: str) -> tuple[int, int]:
    """Normalize the invalid ID range from `l_str` (inclusive) to `u_str` (exclusive)

    An invalid ID `s` is a nonempty string of digits with no leading 0,
    such that some `w` satisfies `s == w + w`. The returns are as follows:
    `l` and `u` are integers such that all integers in `[l, u)` have string
    representations `w` such that `s == w + w` is an invalid ID, and these
    `s` exhaust the invalid IDs in `[l_str, u_str)`.

    Args:
        l_str (str): integer inclusive lower bound of range as str
        u_str (str): integer exclusive upper bound of range as str

    Returns:
        tuple[int, int]: (`l`, `u`)
    """
    l_msb_len, u_msb_len = len(l_str) // 2, len(u_str) // 2
    l_msb_str, l_lsb_str, u_msb_str, u_lsb_str = l_str[:l_msb_len], l_str[l_msb_len:], u_str[:u_msb_len], u_str[u_msb_len:]
    # l_msb_len == l_lsb_len or l_msb_len + 1 == l_lsb_len
    if len(l_msb_str) != len(l_lsb_str):
        # l_msb_len + 1 == l_lsb_len: set l_msb to 10 ** l_msb_len, e.g. "11" => 10 ** 2 == 100
        l_msb = 10 ** l_msb_len
    else:
        # l_msb_len == l_lsb_len: set l_msb to the integer value of l_msb_str,
        # then add one if l_msb < l_lsb, so that old l_msb is excluded
        l_msb, l_lsb = parse_int(l_msb_str), parse_int(l_lsb_str)
        if l_msb < l_lsb:
            l_msb += 1
    # u_msb_len == u_lsb_len or u_msb_len + 1 == u_lsb_len
    if len(u_msb_str) != len(u_lsb_str):
        # u_msb_len + 1 == u_lsb_len: set u_msb to 10 ** u_msb_len, e.g. "11" => 10 ** 2 == 100
        u_msb = 10 ** u_msb_len
    else:
        # u_msb_len == u_lsb_len: set u_msb to the integer value of u_msb_str,
        # then add one if u_msb <= u_lsb, so that old u_msb is included
        u_msb, u_lsb = parse_int(u_msb_str), parse_int(u_lsb_str)
        if u_msb <= u_lsb:
            u_msb += 1
    return l_msb, u_msb

def sum_invalid_ids_p(l: int, u:int, p: int) -> int:
    if u <= l:
        return 0
    return (((10 ** p) + 1) * (u - l) * (u + l - 1)) // 2

def sum_invalid_ids(l: int, u:int) -> int:
    l_digits, u_digits = len(to_str(l)), len(to_str(u))
    if l_digits == u_digits:
        return sum_invalid_ids_p(l, u, l_digits)
    l_numbers = sum_invalid_ids_p(l, 10 ** l_digits, l_digits)
    standard_numbers = sum(sum_invalid_ids_p(10 ** (p-1), 10 ** p, p) for p in range(l_digits + 1, u_digits))
    u_numbers = sum_invalid_ids_p(10 ** (u_digits - 1), u, u_digits)
    return l_numbers + standard_numbers + u_numbers

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "diagnostic.txt") as f:
    ...     solve(f)
    '1227775554'
    """
    id_ranges_str = (pair.split("-") for pair in f.read().strip().split(","))
    return str(sum(sum_invalid_ids(*normalize_invalid_id_range(l_str, u_str)) for l_str, u_str in id_ranges_str))


if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        print(solve(f))
