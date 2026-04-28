from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f_ex:
    ...     solve(f_ex)
    '14'
    """
    grid = [[int(c) for c in line.strip()] for line in f if line.strip()]
    if not grid:
        return "0"
    R, C = len(grid), len(grid[0])

    # Pre-sort all coordinates by barrel size descending
    coords = sorted(((grid[r][c], r, c) for r in range(R) for c in range(C)), key=lambda x: x[0], reverse=True)

    destroyed = [[False] * C for _ in range(R)]
    total_count = 0

    for _ in range(3):
        best_gain = -1
        best_visited = None

        # Disqualify barrels reached in this round from being starting targets
        disqualified = [[False] * C for _ in range(R)]

        for val, r, c in coords:
            if destroyed[r][c] or disqualified[r][c]:
                continue

            # BFS/Flood-fill from this candidate
            visited = []
            stack = [(r, c)]
            visited_set = {(r, c)}
            disqualified[r][c] = True
            gain = 0

            idx = 0
            while idx < len(stack):
                curr_r, curr_c = stack[idx]
                idx += 1
                gain += 1
                visited.append((curr_r, curr_c))
                curr_val = grid[curr_r][curr_c]

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < R and 0 <= nc < C and not destroyed[nr][nc]:
                        if grid[nr][nc] <= curr_val and (nr, nc) not in visited_set:
                            visited_set.add((nr, nc))
                            disqualified[nr][nc] = True
                            stack.append((nr, nc))

            if gain > best_gain:
                best_gain = gain
                best_visited = visited

        if best_visited is None:
            break

        for dr, dc in best_visited:
            destroyed[dr][dc] = True
        total_count += best_gain

    return str(total_count)
