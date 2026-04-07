from typing import TextIO

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '581078'
    """
    _, nums = next(f).split(":")
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

    return f"{"".join(str(n) for n in spine)}"
