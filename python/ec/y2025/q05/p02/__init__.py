from typing import TextIO

def quality(s: str) -> int:
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
    return id, int("".join(str(n) for n in spine))

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '77053'
    """
    _, quality_min = quality(next(f))
    quality_max = quality_min
    for sword in f:
        _, q = quality(sword)
        if q < quality_min:
            quality_min = q
        if q > quality_max:
            quality_max = q

    return f"{quality_max - quality_min}"
