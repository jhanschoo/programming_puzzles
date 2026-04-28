from typing import TextIO


def solve_params(nums: list[int]) -> int:
    cols = list(nums)
    n = len(cols)
    round_count = 0

    # Phase 1: More birds to next column if it has fewer
    # (Note: For Part 3, the input is already non-decreasing, so this will do nothing)
    while True:
        moved = False
        for i in range(n - 1):
            if cols[i] > cols[i + 1]:
                cols[i] -= 1
                cols[i + 1] += 1
                moved = True
        if not moved:
            break
        round_count += 1

    # Optimized Phase 2:
    # Since Phase 2 moves ducks left until the sequence is non-increasing,
    # and we start from a non-decreasing state (from Phase 1), the final state
    # is perfectly balanced (all columns = total / n).
    # Each round of Phase 2 increases the prefix sum S[i] by at most 1.
    # The number of rounds is the maximum deficit in the prefix sums.
    s_current = [0] * (n + 1)
    for i in range(n):
        s_current[i + 1] = s_current[i] + cols[i]

    total = s_current[n]
    avg = total // n
    s_final = [i * avg for i in range(n + 1)]

    r2 = max(s_final[i] - s_current[i] for i in range(n + 1))
    round_count += r2

    return round_count


def solve(f: TextIO) -> str:
    nums = [int(line.strip().strip(".")) for line in f if line.strip()]
    if not nums:
        return ""
    return str(solve_params(nums))
