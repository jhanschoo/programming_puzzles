# Design: Replace `run-diagnostic-tests` with `check-solve`

**Date:** 2026-04-04

## Problem

`run-diagnostic-tests` in `lib/test-helper.rkt` accepts glob patterns and expands them at runtime. At every call site, the glob patterns are literal filenames anyway — the test submodule already knows exactly which files to open and what answers to expect. The glob machinery adds indirection without benefit and pulls in `file/glob` as a dependency.

## Decision

Replace `run-diagnostic-tests` with `check-solve`, a simpler helper that opens files by name directly.

## API

```racket
;; check-solve : (InputPort -> String) Path (Listof (List path-string? String)) -> Void
(check-solve solve dir '(("diagnostic.txt" "15")
                          ("diagnostic2.txt" "42")))
```

- `solve` — the solution function, matching `solve/c` (`(-> input-port? string?)`)
- `dir` — base directory (typically bound with `define-runtime-path`)
- pairs — list of `(filename expected)` pairs; filenames are plain strings, not glob patterns

For each pair, `check-solve` opens `(build-path dir filename)` with `call-with-input-file`, calls `solve`, and asserts the result equals `expected` via `check-equal?`. A `with-check-info` context includes `['file ...]` for readable rackunit failure output.

## Changes

| File | Change |
|---|---|
| `lib/test-helper.rkt` | Replace `run-diagnostic-tests` with `check-solve`; remove `file/glob` require; update `contract-out` |
| `lib/test-helper-test.rkt` | Update all test cases to call `check-solve` with plain filenames; drop the glob-expansion test case |
| `aoc/2025/day01/1.rkt` | Update `require/typed` annotation and call site |

## Out of scope

- `lib/contracts.rkt` — no change; `solve/c` is unchanged
- `lib/runner.rkt` — no change; batch runner is separate from diagnostic testing
