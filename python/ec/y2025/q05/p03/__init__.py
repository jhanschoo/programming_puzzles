from typing import Iterable, TextIO

def cat_int(it: Iterable[int | str]) -> int:
    return int("".join(map(str, it)))

def signature(s: str) -> int:
    id, nums = s.split(":")
    nums = list(map(int, nums.split(",")))
    spine = [nums[0]]
    nums = nums[1:]
    left = {}
    right = {}
    for n in nums:
        place_found = False
        for i, s in enumerate(spine):
            if n < s and left.get(i) is None:
                left[i] = n
                place_found = True
                break
            elif n > s and right.get(i) is None:
                right[i] = n
                place_found = True
                break
        if not place_found:
            spine.append(n)
    q = cat_int(spine)
    lvls = [cat_int((left.get(i, ""), s, right.get(i, ""))) for i, s in enumerate(spine)]
    return q, lvls, int(id)

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '260'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '4'
    """
    swords = sorted(map(signature, f.read().strip().splitlines()), reverse=True)
    checksum = sum(i * id for i, (_, _, id) in enumerate(swords, 1))

    return f"{checksum}"
