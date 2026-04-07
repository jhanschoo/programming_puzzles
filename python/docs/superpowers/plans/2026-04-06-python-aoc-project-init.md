# Python AoC Project Initialization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Initialize the Python workspace with the `aoc/` and `lib/` package hierarchy, configure pytest for doctest discovery, and verify end-to-end with a sample day scaffold.

**Architecture:** Single uv-managed Python project with two top-level packages (`aoc/` for contest solutions, `lib/` for shared utilities). Hatchling is configured to include both packages. Pytest is configured to discover doctests across both packages automatically.

**Tech Stack:** Python 3.14, uv, hatchling (build backend), pytest

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Modify | `pyproject.toml` | Add build system, hatchling package config, pytest config, pytest dev dep |
| Create | `.gitignore` | Ignore `input.txt` files (puzzle inputs are personal/copyrighted) |
| Create | `aoc/__init__.py` | Contest package root |
| Create | `lib/__init__.py` | Shared utilities package root |
| Delete | `main.py` | Generated stub, not part of the design |
| Create | `aoc/y2025/__init__.py` | Year sub-package |
| Create | `aoc/y2025/d01/__init__.py` | Day sub-package |
| Create | `aoc/y2025/d01/diagnostic.txt` | Sample input for doctests |
| Create | `aoc/y2025/d01/p1.py` | Part 1 sample solution (verifies scaffold) |
| Create | `aoc/y2025/d01/p2.py` | Part 2 sample solution (verifies scaffold) |

---

## Task 1: Configure pyproject.toml and add pytest

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add pytest as a dev dependency via uv**

```bash
cd /home/jhanschoo/src/aoc/python
uv add --dev pytest
```

Expected: `pyproject.toml` gains a `[dependency-groups]` section with `pytest`, and `uv.lock` is updated. No errors.

- [ ] **Step 2: Add build system, package discovery, and pytest config to pyproject.toml**

Open `pyproject.toml`. It currently looks like:

```toml
[project]
name = "python"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=...",
]
```

Add the following sections at the end:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["aoc", "lib"]

[tool.pytest.ini_options]
addopts = "--doctest-modules"
testpaths = ["aoc", "lib"]
```

- [ ] **Step 3: Sync to install the project in editable mode**

```bash
uv sync
```

Expected: project installed editably, no errors.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: configure hatchling packages, pytest doctest discovery, add pytest dev dep"
```

---

## Task 2: Create package roots and gitignore

**Files:**
- Create: `aoc/__init__.py`
- Create: `lib/__init__.py`
- Create: `.gitignore`
- Delete: `main.py`

- [ ] **Step 1: Create aoc/__init__.py**

Create `aoc/__init__.py` as an empty file (zero bytes or a single newline).

- [ ] **Step 2: Create lib/__init__.py**

Create `lib/__init__.py` as an empty file.

- [ ] **Step 3: Create .gitignore**

Create `python/.gitignore` with the following content:

```
input.txt
```

This ignores puzzle input files, which are personal and should not be committed. `diagnostic.txt` is intentionally not ignored — it must be committed since doctests depend on it.

- [ ] **Step 4: Remove generated stub**

```bash
git rm main.py
```

Expected: `main.py` staged for deletion.

- [ ] **Step 5: Verify pytest finds no errors on empty packages**

```bash
uv run pytest -v
```

Expected: `no tests ran` or similar — no failures, no errors.

- [ ] **Step 6: Commit**

```bash
git add aoc/__init__.py lib/__init__.py .gitignore
git commit -m "chore: initialize aoc and lib packages, add gitignore, remove generated stub"
```

---

## Task 3: Create sample day scaffold

**Files:**
- Create: `aoc/y2025/__init__.py`
- Create: `aoc/y2025/d01/__init__.py`
- Create: `aoc/y2025/d01/diagnostic.txt`
- Create: `aoc/y2025/d01/p1.py`
- Create: `aoc/y2025/d01/p2.py`

- [ ] **Step 1: Create year and day __init__.py files**

Create `aoc/y2025/__init__.py` — empty file.
Create `aoc/y2025/d01/__init__.py` — empty file.

- [ ] **Step 2: Create diagnostic.txt**

Create `aoc/y2025/d01/diagnostic.txt` with this content (three numbers, one per line):

```
3
1
2
```

- [ ] **Step 3: Create p1.py**

Create `aoc/y2025/d01/p1.py`:

```python
from pathlib import Path
from typing import TextIO


def solve(in_: TextIO) -> str:
    """
    >>> solve(open(Path(__file__).parent / "diagnostic.txt"))
    '6'
    """
    return str(sum(int(line) for line in in_))


if __name__ == "__main__":
    import sys
    print(solve(open(sys.argv[1])))
```

- [ ] **Step 4: Run p1 doctest to verify it passes**

```bash
uv run pytest aoc/y2025/d01/p1.py -v
```

Expected:
```
aoc/y2025/d01/p1.py::aoc.y2025.d01.p1.solve PASSED
```

- [ ] **Step 5: Create p2.py**

Create `aoc/y2025/d01/p2.py`:

```python
from pathlib import Path
from typing import TextIO


def solve(in_: TextIO) -> str:
    """
    >>> solve(open(Path(__file__).parent / "diagnostic.txt"))
    '3'
    """
    return str(max(int(line) for line in in_))


if __name__ == "__main__":
    import sys
    print(solve(open(sys.argv[1])))
```

- [ ] **Step 6: Run all doctests**

```bash
uv run pytest -v
```

Expected: both doctests pass:
```
aoc/y2025/d01/p1.py::aoc.y2025.d01.p1.solve PASSED
aoc/y2025/d01/p2.py::aoc.y2025.d01.p2.solve PASSED
```

- [ ] **Step 7: Verify CLI invocation**

```bash
uv run python aoc/y2025/d01/p1.py aoc/y2025/d01/diagnostic.txt
uv run python aoc/y2025/d01/p2.py aoc/y2025/d01/diagnostic.txt
```

Expected output: `6` then `3`.

- [ ] **Step 8: Commit**

```bash
git add aoc/y2025/__init__.py aoc/y2025/d01/__init__.py aoc/y2025/d01/diagnostic.txt aoc/y2025/d01/p1.py aoc/y2025/d01/p2.py
git commit -m "feat: add aoc/y2025/d01 sample scaffold to verify project structure"
```
