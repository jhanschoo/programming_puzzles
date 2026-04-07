# Python AoC Project Design

**Date:** 2026-04-06

## Overview

A Python project for Advent of Code (and similar competitions), structured as a hierarchy of packages: contest → year → day → part. Each part is a standalone Python file with a `solve` function, inline doctests, and a CLI entry point.

## Directory Structure

```
python/
  pyproject.toml
  aoc/
    __init__.py
    y2025/
      __init__.py
      d01/
        __init__.py
        p1.py
        p2.py
        input.txt
        diagnostic.txt
  lib/
    __init__.py
```

- `aoc/` — top-level contest package (one per contest, e.g. `aoc/`)
- `yYYYY/` — year sub-package (e.g. `y2025/`); numeric-only names are invalid Python identifiers hence the `y` prefix
- `dDD/` — day sub-package (e.g. `d01/`, zero-padded)
- `p1.py`, `p2.py` — part files
- `input.txt` — full puzzle input (not committed)
- `diagnostic.txt` — small example input used in doctests
- `lib/` — shared utilities importable by any solution

Both `aoc` and `lib` are declared as packages in `pyproject.toml`.

## Part File Anatomy

Each `pN.py` follows this template:

```python
from pathlib import Path
from typing import TextIO


def solve(in_: TextIO) -> str:
    """
    >>> solve(open(Path(__file__).parent / "diagnostic.txt"))
    '3'
    """
    ...


if __name__ == "__main__":
    import sys
    print(solve(open(sys.argv[1])))
```

- `solve(in_: TextIO) -> str` — takes any file-like text object, returns the answer as a string
- Doctest opens `diagnostic.txt` relative to `__file__`, so it works regardless of the working directory
- `__main__` block accepts a filename as a CLI argument and prints the result

## Running Solutions

```
python aoc/y2025/d01/p1.py aoc/y2025/d01/input.txt
```

## Testing

`pytest` is added as a dev dependency. Doctests are discovered via `--doctest-modules`.

```
# All doctests across the project
pytest --doctest-modules

# A specific year
pytest --doctest-modules aoc/y2025/

# A specific day
pytest --doctest-modules aoc/y2025/d01/

# A specific part
pytest --doctest-modules aoc/y2025/d01/p1.py
```

## Dependencies

- **Runtime:** none beyond the stdlib
- **Dev:** `pytest`

## lib/ Package

`lib/` is an initially empty package for shared utilities (grid helpers, parsing utilities, etc.) that grow organically as common patterns emerge across solutions. No utilities are pre-populated.
