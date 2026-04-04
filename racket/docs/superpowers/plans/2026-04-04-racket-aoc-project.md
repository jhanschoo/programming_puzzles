# Racket AoC Project Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up a raco-managed Racket project for Advent of Code with a shared test helper, per-contest batch runners, and an example solution to verify everything works.

**Architecture:** Single raco package at `racket/` with a `lib` collection for shared code. Solution files use `module+ main` (runnable) and `module+ test` (diagnostic assertions via shared helper). Each contest type (`aoc/`, `ec/`) has its own `run.rkt` for batch-executing solutions against input files.

**Tech Stack:** Racket 9.0, rackunit, file/glob, racket/runtime-path

---

## File Map

| File | Responsibility |
|------|---------------|
| `info.rkt` | Package root — declares package name, deps |
| `lib/info.rkt` | Declares `lib` as a collection |
| `lib/test-helper.rkt` | Provides `run-diagnostic-tests` function for rackunit assertions |
| `aoc/run.rkt` | AoC-specific batch runner — discovers and runs solutions against `input*.txt` |
| `aoc/2025/day01/1.rkt` | Example solution (AoC 2025 Day 1 Part 1) — verifies the full workflow |
| `aoc/2025/day01/diagnostic.txt` | Example diagnostic input for the example solution |

Old directories to remove: `aoc-2025/`, `ec-2025/`

---

### Task 1: Package Scaffolding

**Files:**
- Create: `info.rkt`
- Create: `lib/info.rkt`

- [ ] **Step 1: Create the package root `info.rkt`**

```racket
#lang info

(define collection 'multi)
(define deps '("base"))
(define build-deps '("rackunit-lib"))
```

`collection 'multi` tells raco this package provides multiple collections (lib, aoc, ec, etc.) rather than being a single collection.

- [ ] **Step 2: Create `lib/info.rkt`**

```racket
#lang info

(define collection "lib")
```

This declares `lib` as a collection so `(require lib/test-helper)` works.

- [ ] **Step 3: Install the package in development mode**

Run (from `racket/`):
```bash
raco pkg install --auto --link .
```

Expected: Package installs successfully, linking the working directory.

- [ ] **Step 4: Verify the package is installed**

Run:
```bash
raco pkg show --auto | grep -E "^(Name|lib)"
```

Expected: The package appears in the installed list.

- [ ] **Step 5: Commit**

```bash
git add info.rkt lib/info.rkt
git commit -m "feat: add raco package scaffolding with lib collection"
```

---

### Task 2: Shared Test Helper

**Files:**
- Create: `lib/test-helper.rkt`

The test helper provides `run-diagnostic-tests`, a function that takes a solver function, a directory path, and a list of `(glob-pattern expected-answer)` pairs. For each pair, it expands the glob relative to the directory, opens each matching file, calls the solver, and asserts the result with rackunit.

Solution files use it like this:

```racket
(module+ test
  (require lib/test-helper racket/runtime-path)
  (define-runtime-path here ".")
  (run-diagnostic-tests solve here
    '(("diagnostic.txt" "expected-answer"))))
```

The caller owns the `define-runtime-path` (one line of boilerplate) so path resolution is always correct relative to the solution file.

- [ ] **Step 1: Write a failing test for `run-diagnostic-tests`**

Create `lib/test-helper-test.rkt`:

```racket
#lang racket

(require rackunit racket/runtime-path)
(require lib/test-helper)

(define-runtime-path here ".")

;; A trivial solver that returns the first line of input
(define (first-line-solver in)
  (read-line in))

;; run-diagnostic-tests should call the solver on each matching file
;; and assert the result equals the expected value.
;; We test it by calling it with a known file and expected value.
(define test-dir (build-path here "test-fixtures"))

(test-case "run-diagnostic-tests passes when solver returns expected value"
  (run-diagnostic-tests first-line-solver test-dir
    '(("hello.txt" "hello world"))))

(test-case "run-diagnostic-tests fails when solver returns wrong value"
  (check-exn exn:test:check?
    (lambda ()
      (run-diagnostic-tests first-line-solver test-dir
        '(("hello.txt" "wrong answer"))))))

(test-case "run-diagnostic-tests expands globs"
  (run-diagnostic-tests first-line-solver test-dir
    '(("hello*.txt" "hello world"))))
```

- [ ] **Step 2: Create test fixtures**

Create `lib/test-fixtures/hello.txt`:
```
hello world
```

Create `lib/test-fixtures/hello2.txt`:
```
hello world
```

- [ ] **Step 3: Run the test to verify it fails**

Run:
```bash
raco test lib/test-helper-test.rkt
```

Expected: FAIL — `lib/test-helper` module not found or `run-diagnostic-tests` not provided.

- [ ] **Step 4: Implement `lib/test-helper.rkt`**

```racket
#lang racket

(provide run-diagnostic-tests)

(require rackunit file/glob)

;; run-diagnostic-tests : (InputPort -> String) Path (Listof (List String String)) -> Void
;;
;; For each (glob-pattern expected) pair, expands the glob relative to dir,
;; opens each matching file, calls solve, and asserts the result equals expected.
(define (run-diagnostic-tests solve dir pairs)
  (for ([pair (in-list pairs)])
    (define pattern (first pair))
    (define expected (second pair))
    (define full-pattern (build-path dir pattern))
    (define matches (glob (path->string full-pattern)))
    (when (null? matches)
      (fail (format "No files matched pattern: ~a" full-pattern)))
    (for ([file-path (in-list matches)])
      (define result
        (call-with-input-file file-path
          (lambda (in) (solve in))))
      (with-check-info (['file (path->string file-path)]
                        ['pattern pattern])
        (check-equal? result expected)))))
```

- [ ] **Step 5: Run the test to verify it passes**

Run:
```bash
raco test lib/test-helper-test.rkt
```

Expected: All 3 tests pass.

- [ ] **Step 6: Commit**

```bash
git add lib/test-helper.rkt lib/test-helper-test.rkt lib/test-fixtures/
git commit -m "feat: add shared test helper with glob support"
```

---

### Task 3: Example Solution with Diagnostic

**Files:**
- Create: `aoc/2025/day01/diagnostic.txt`
- Create: `aoc/2025/day01/1.rkt`

This task creates a minimal working example to verify the full workflow: `raco test` runs diagnostics, and `racket 1.rkt <file>` runs the solution.

The example solves a trivial problem: sum all numbers in the input (one per line).

- [ ] **Step 1: Create the diagnostic input file**

Create `aoc/2025/day01/diagnostic.txt`:
```
1
2
3
4
5
```

- [ ] **Step 2: Write the solution file with `module+ test`**

Create `aoc/2025/day01/1.rkt`:

```racket
#lang racket

(provide solve)

(define (solve in)
  (define total
    (for/sum ([line (in-lines in)]
              #:when (non-empty-string? line))
      (string->number line)))
  (number->string total))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (displayln (solve (open-input-file filename))))

(module+ test
  (require lib/test-helper racket/runtime-path)
  (define-runtime-path here ".")
  (run-diagnostic-tests solve here
    '(("diagnostic.txt" "15"))))
```

- [ ] **Step 3: Run the diagnostic test**

Run:
```bash
raco test aoc/2025/day01/1.rkt
```

Expected: 1 test passes (sum of 1+2+3+4+5 = 15).

- [ ] **Step 4: Run the solution as a standalone program**

Run:
```bash
racket aoc/2025/day01/1.rkt aoc/2025/day01/diagnostic.txt
```

Expected output:
```
15
```

- [ ] **Step 5: Verify recursive `raco test` discovery**

Run:
```bash
raco test aoc/
```

Expected: discovers and runs the test in `aoc/2025/day01/1.rkt`, 1 test passes.

- [ ] **Step 6: Commit**

```bash
git add aoc/2025/day01/
git commit -m "feat: add example AoC solution (2025 day01 part 1)"
```

---

### Task 4: AoC Batch Runner

**Files:**
- Create: `aoc/run.rkt`

The runner discovers solution files and input files by filesystem convention, then runs each solution against each input via subprocess.

- [ ] **Step 1: Create `aoc/run.rkt`**

```racket
#lang racket

(require racket/runtime-path file/glob)

(define-runtime-path aoc-root ".")

;; Discover solution entry points: files named <digit>.rkt inside day<NN>/ dirs
(define (discover-solutions base-dir)
  (define pattern (build-path base-dir "**" "day*" "*.rkt"))
  (define candidates (glob (path->string pattern)))
  (filter
   (lambda (p)
     (define name (path->string (file-name-from-path p)))
     (regexp-match? #rx"^[0-9]+\\.rkt$" name))
   candidates))

;; Discover input files matching input*.txt in a directory
(define (discover-inputs dir)
  (define pattern (build-path dir "input*.txt"))
  (glob (path->string pattern)))

;; Run a solution file against an input file, return output string
(define (run-solution solution-path input-path)
  (define-values (proc stdout stdin stderr)
    (subprocess #f #f #f
                (find-executable-path "racket")
                (path->string solution-path)
                (path->string input-path)))
  (close-output-port stdin)
  (define output (port->string stdout))
  (close-input-port stdout)
  (subprocess-wait proc)
  (define status (subprocess-status proc))
  (close-input-port stderr)
  (values (string-trim output) status))

(module+ main
  (define target
    (command-line
     #:args ([path "."])
     path))

  (define base-dir
    (simplify-path (build-path aoc-root target)))

  (define solutions (discover-solutions base-dir))

  (when (null? solutions)
    (printf "No solutions found under ~a\n" base-dir)
    (exit 1))

  (for ([sol (in-list (sort solutions path<?))])
    (define dir (path-only sol))
    (define inputs (discover-inputs dir))
    (for ([inp (in-list (sort inputs path<?))])
      (define sol-rel (find-relative-path aoc-root sol))
      (define inp-rel (find-relative-path aoc-root inp))
      (printf "~a < ~a: " sol-rel inp-rel)
      (flush-output)
      (define-values (output status) (run-solution sol inp))
      (if (zero? status)
          (printf "~a\n" output)
          (printf "FAILED (exit ~a)\n" status)))))
```

- [ ] **Step 2: Test the runner with the example solution**

First create a dummy input file `aoc/2025/day01/input-example.txt`:
```
10
20
30
```

Run:
```bash
racket aoc/run.rkt 2025/day01/
```

Expected output:
```
2025/day01/1.rkt < 2025/day01/input-example.txt: 60
```

- [ ] **Step 3: Test runner with year-level scope**

Run:
```bash
racket aoc/run.rkt 2025/
```

Expected: same output as above (discovers the same solution).

- [ ] **Step 4: Test runner with no arguments (all of AoC)**

Run:
```bash
racket aoc/run.rkt
```

Expected: same output (discovers everything under `aoc/`).

- [ ] **Step 5: Commit**

```bash
git add aoc/run.rkt aoc/2025/day01/input-example.txt
git commit -m "feat: add AoC batch runner with path-based scoping"
```

---

### Task 5: Cleanup and Final Verification

**Files:**
- Remove: `aoc-2025/` (empty directory)
- Remove: `ec-2025/` (empty directory)

- [ ] **Step 1: Remove old empty directories**

```bash
rmdir aoc-2025 ec-2025
```

- [ ] **Step 2: Full end-to-end verification — diagnostic tests**

Run:
```bash
raco test .
```

Expected: All tests pass — both the test helper's own tests and the example solution's diagnostic test.

- [ ] **Step 3: Full end-to-end verification — batch runner**

Run:
```bash
racket aoc/run.rkt
```

Expected: Runs the example solution against `input-example.txt` and prints the result.

- [ ] **Step 4: Verify standalone execution**

Run:
```bash
racket aoc/2025/day01/1.rkt aoc/2025/day01/diagnostic.txt
```

Expected output: `15`

- [ ] **Step 5: Commit cleanup**

```bash
git commit -m "chore: remove old empty directories"
```
