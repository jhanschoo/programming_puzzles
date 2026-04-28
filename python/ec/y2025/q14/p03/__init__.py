from typing import TextIO


def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     res = solve(f)
    >>> res
    '278388552'
    """
    target_pattern = [line.strip() for line in f if line.strip()]
    
    R, C = 34, 34
    rounds = 1000000000
    
    r_start = (R - 8) // 2
    c_start = (C - 8) // 2
    
    # Target pattern bits for center
    target_bits = []
    for row in target_pattern:
        bits = 0
        for char in row:
            bits = (bits << 1) | (1 if char == '#' else 0)
        target_bits.append(bits)

    # Initial state: all inactive
    current = [0] * R
    
    # Seen states for cycle detection
    # State is a tuple of rows
    seen = {}
    history = [] # (total_active_in_round, matches_pattern)
    
    ALL_ONES = (1 << C) - 1
    
    for t in range(1, rounds + 1):
        next_grid = [0] * R
        for r in range(R):
            diag_parity = 0
            if r > 0:
                diag_parity ^= (current[r-1] << 1) ^ (current[r-1] >> 1)
            if r < R - 1:
                diag_parity ^= (current[r+1] << 1) ^ (current[r+1] >> 1)
            
            diag_parity &= ALL_ONES
            
            # Rule: active if (active and odd) or (inactive and even)
            # next = current ^ diag_parity ^ 1
            next_grid[r] = current[r] ^ diag_parity ^ ALL_ONES
            
        current = next_grid
        
        # Check center pattern
        matches = True
        for i in range(8):
            center_row_bits = (current[r_start + i] >> (C - c_start - 8)) & 0xFF
            if center_row_bits != target_bits[i]:
                matches = False
                break
        
        active_count = sum(row.bit_count() for row in current)
        
        state = tuple(current)
        if state in seen:
            start_round = seen[state]
            period = t - start_round
            
            # Pre-period sum
            total_active = 0
            for i in range(start_round - 1):
                cnt, match = history[i]
                if match:
                    total_active += cnt
            
            # Full cycles
            rounds_left = rounds - (start_round - 1)
            num_cycles = rounds_left // period
            rem_rounds = rounds_left % period
            
            cycle_active = 0
            for i in range(start_round - 1, t - 1):
                cnt, match = history[i]
                if match:
                    cycle_active += cnt
            
            total_active += num_cycles * cycle_active
            
            # Remaining fractional cycle
            for i in range(start_round - 1, start_round - 1 + rem_rounds):
                cnt, match = history[i]
                if match:
                    total_active += cnt
            
            return str(total_active)
        
        seen[state] = t
        history.append((active_count, matches))

    # If no cycle detected within rounds
    total_active = 0
    for cnt, match in history:
        if match:
            total_active += cnt
    return str(total_active)
