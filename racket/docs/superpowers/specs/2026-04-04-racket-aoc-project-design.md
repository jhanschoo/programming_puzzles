# Racket AoC Project Design

## Overview

A Racket project for solving Advent of Code (and similar programming contests like Everybody Codes). The project is managed by `raco`, uses `rackunit` for testing diagnostics, and supports running solutions against input files via a contest-specific batch runner.

## Directory Structure

```
racket/                          # raco package root
├── info.rkt                     # package definition
├── lib/
│   ├── info.rkt                 # collection info for (require lib/...)
│   └── test-helper.rkt          # shared test macro
├── aoc/
│   ├── run.rkt                  # AoC-specific batch runner
│   └── 2025/
│       └── day01/
│           ├── 1.rkt            # part 1 entry point
│           ├── 2.rkt            # part 2 entry point
│           ├── helpers.rkt      # optional shared helpers for complex days
│           ├── diagnostic.txt   # sample input with known answer
│           ├── diagnostic2.txt  # optional extra diagnostics
│           └── input.txt        # puzzle input
└── ec/
    ├── run.rkt                  # EC-specific batch runner
    └── 2025/
        └── ...                  # same per-day structure, possibly different file conventions
```

- Day directories contain no boilerplate `info.rkt` files.
- Solution entry points use numeric filenames (`1.rkt`, `2.rkt`, ...).
- Helper modules for complex multi-file solutions live alongside entry points.
- Input/diagnostic files are colocated in the same day directory.

## Solution File Structure

Each entry point has two submodules:

### `module+ main` — Runnable Program

Accepts a filename as a command-line argument, runs the solution, prints the answer to stdout.

```racket
(module+ main
  (define filename (command-line #:args (filename) filename))
  (displayln (solve (open-input-file filename))))
```

Invoked as: `racket aoc/2025/day01/1.rkt aoc/2025/day01/input.txt`

### `module+ test` — Diagnostic Tests

Uses the shared test helper to run against `diagnostic*.txt` files with expected-value assertions.

```racket
(module+ test
  (require lib/test-helper)
  (aoc-test solve
    #:diagnostic [("diagnostic.txt" "expected-answer")]))
```

Invoked via: `raco test aoc/2025/day01/1.rkt`

### Full Skeleton

```racket
#lang racket

(provide solve)

(define (solve in)
  ;; read from input port `in`, return answer as string
  ...)

(module+ main
  (define filename (command-line #:args (filename) filename))
  (displayln (solve (open-input-file filename))))

(module+ test
  (require lib/test-helper)
  (aoc-test solve
    #:diagnostic [("diagnostic.txt" "expected-answer")]))
```

## Shared Test Helper (`lib/test-helper.rkt`)

Provides a macro (e.g., `aoc-test`) that:

1. Takes the solver function and a list of `(filename expected-answer)` pairs.
2. Resolves each filename relative to the calling file's directory (using `define-runtime-path` or equivalent).
3. Generates `rackunit` `check-equal?` test cases: calls the solver with an input port opened from the file and asserts the result equals the expected answer.
4. The filename field accepts glob patterns (e.g., `"diagnostic*.txt"`) for matching multiple diagnostic files against the same expected answer if needed.

This eliminates boilerplate repetition across solution files. Each file only specifies the solver function and expected answers.

## Batch Runner (`aoc/run.rkt`)

An AoC-specific Racket script for running solutions against `input*.txt` files.

### Behavior

1. Takes an optional path argument (defaults to the `aoc/` directory).
2. Recursively discovers solution entry points by convention: files with numeric names (`1.rkt`, `2.rkt`, ...) inside directories matching `dayNN/`.
3. Discovers `input*.txt` files in each day directory.
4. Runs each solution against each matching input file (via subprocess or dynamic require) and prints results to stdout.

### Usage

| Command | Scope |
|---------|-------|
| `racket aoc/run.rkt` | All AoC solutions, all inputs |
| `racket aoc/run.rkt 2025/` | All of AoC 2025 |
| `racket aoc/run.rkt 2025/day01/` | One day |
| `racket aoc/run.rkt 2025/day01/1.rkt` | One specific solution |

Each contest type (AoC, EC, etc.) has its own `run.rkt` with its own conventions for file discovery patterns. This allows different contests to use different input file naming without a shared abstraction.

## Package Setup

### `racket/info.rkt`

Declares the raco package. Defines the package name and dependencies (at minimum, `rackunit-lib` for testing).

### `racket/lib/info.rkt`

Declares `lib` as a collection so that `(require lib/test-helper)` works from any solution file after the package is installed.

### No other `info.rkt` files needed

Day directories, year directories, and contest directories (`aoc/`, `ec/`) do not need `info.rkt` files. `raco test` discovers test submodules by recursing into `.rkt` files directly.

## Workflows

| Goal | Command |
|------|---------|
| Test one solution (diagnostic) | `raco test aoc/2025/day01/1.rkt` |
| Test one day (all diagnostics) | `raco test aoc/2025/day01/` |
| Test all AoC 2025 diagnostics | `raco test aoc/2025/` |
| Test everything (all contests) | `raco test .` |
| Run one solution on one input | `racket aoc/2025/day01/1.rkt aoc/2025/day01/input.txt` |
| Run all AoC inputs | `racket aoc/run.rkt` |
| Run AoC 2025 inputs | `racket aoc/run.rkt 2025/` |
| Run one day's inputs | `racket aoc/run.rkt 2025/day01/` |

## Design Decisions

- **`module+ test` for diagnostics**: Idiomatic Racket; `raco test` handles all discovery and execution natively.
- **Separate runner for inputs**: Running against `input*.txt` is not a test (no assertion), so it uses a separate script rather than abusing the test framework.
- **Per-contest runners**: Different contests may have different file naming conventions. Each contest type owns its runner and conventions.
- **Shared test helper as a library collection**: Avoids boilerplate in every solution file. Parameterizable via glob patterns for flexibility.
- **No per-directory `info.rkt` boilerplate**: Day/year directories are plain directories. Only the package root and `lib/` need `info.rkt`.
