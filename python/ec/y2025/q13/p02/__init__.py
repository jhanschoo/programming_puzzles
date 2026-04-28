from typing import TextIO


def solve_params(ranges: list[tuple[int, int]], target_steps: int) -> int:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     ranges = []
    ...     for line in f:
    ...         if line.strip():
    ...             A, B = map(int, line.strip().split('-'))
    ...             ranges.append((A, B))
    >>> solve_params(ranges, 20252025)
    30
    """
    cw_ranges = []
    ccw_ranges = []
    
    for i, r in enumerate(ranges):
        if i % 2 == 0:
            cw_ranges.append(r)
        else:
            ccw_ranges.append(r)
            
    total_range_len = sum(B - A + 1 for A, B in ranges)
    total_len = 1 + total_range_len
    
    # conceptual list starting from 1: [1] + [cw_ranges] + [ccw_ranges in reverse order and internally reversed]
    # Example: 10-15 (CW), 12-13 (CCW), 20-21 (CW), 19-23 (CCW), 30-37 (CW)
    # CW: 10-15, 20-21, 30-37
    # CCW: 12-13, 19-23
    # List: 1, (10, 11, 12, 13, 14, 15), (20, 21), (30, 31, 32, 33, 34, 35, 36, 37), (23, 22, 21, 20, 19), (13, 12)
    
    target_idx = target_steps % total_len
    
    if target_idx == 0:
        return 1
    
    curr_idx = 1
    # Check CW ranges
    for A, B in cw_ranges:
        length = B - A + 1
        if curr_idx <= target_idx < curr_idx + length:
            return A + (target_idx - curr_idx)
        curr_idx += length
        
    # Check CCW ranges
    for A, B in reversed(ccw_ranges):
        length = B - A + 1
        if curr_idx <= target_idx < curr_idx + length:
            # The range is reversed: B, B-1, ..., A
            return B - (target_idx - curr_idx)
        curr_idx += length
            
    raise ValueError("Target index not found")


def solve(f: TextIO) -> str:
    ranges = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        A, B = map(int, line.split('-'))
        ranges.append((A, B))
        
    return str(solve_params(ranges, 20252025))
