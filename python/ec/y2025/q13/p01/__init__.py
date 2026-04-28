from typing import TextIO
from collections import deque


def solve_params(nums: list[int], steps: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     nums = [int(line.strip()) for line in f if line.strip()]
    >>> solve_params(nums, 2025)
    67
    """
    wheel = deque([1])
    for i, num in enumerate(nums):
        if i % 2 == 0:
            wheel.append(num)
        else:
            wheel.appendleft(num)
    
    # 1 is at some index
    idx = wheel.index(1)
    
    # wheel clockwise from index 0 is already correct relative order
    # just need to offset by idx
    final_idx = (idx + steps) % len(wheel)
    return wheel[final_idx]


def solve(f: TextIO) -> str:
    nums = [int(line.strip()) for line in f if line.strip()]
    return str(solve_params(nums, 2025))
