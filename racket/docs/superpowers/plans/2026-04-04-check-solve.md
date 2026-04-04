# check-solve Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `run-diagnostic-tests` (glob-based) with `check-solve` (direct filename-based) in `lib/test-helper.rkt` and update all call sites.

**Architecture:** `lib/test-helper.rkt` exports a single `check-solve` function that opens each named file directly with `call-with-input-file` and asserts the result via rackunit `check-equal?`. No glob expansion. Call sites in `lib/test-helper-test.rkt` and `aoc/2025/day01/1.rkt` are updated to use the new name and signature.

**Tech Stack:** Racket (`#lang racket`, `#lang typed/racket`), rackunit, `racket/contract`, `lib/contracts`

---

### Task 1: Replace `run-diagnostic-tests` with `check-solve` in `lib/test-helper.rkt`

**Files:**
- Modify: `lib/test-helper.rkt`

- [ ] **Step 1: Rewrite `lib/test-helper.rkt`**

Replace the entire file with:

```racket
#lang racket

(provide
 (contract-out
  [check-solve
   (-> solve/c
       path?
       (listof (list/c path-string? string?))
       void?)]))

(require rackunit lib/contracts)

;; check-solve : (InputPort -> String) Path (Listof (List path-string? String)) -> Void
;;
;; For each (filename expected) pair, opens the file at (build-path dir filename),
;; calls solve, and asserts the result equals expected.
(define (check-solve solve dir pairs)
  (for ([pair (in-list pairs)])
    (define filename (first pair))
    (define expected (second pair))
    (define file-path (build-path dir filename))
    (define result
      (call-with-input-file file-path
        (lambda (in) (solve in))))
    (with-check-info (['file (path->string file-path)])
      (check-equal? result expected))))
```

- [ ] **Step 2: Verify the file loads**

Run: `snap run racket -e '(require lib/test-helper)'`

Expected: no output, exit 0.

---

### Task 2: Update `lib/test-helper-test.rkt`

**Files:**
- Modify: `lib/test-helper-test.rkt`

- [ ] **Step 1: Rewrite `lib/test-helper-test.rkt`**

Replace the entire file with:

```racket
#lang racket

(require rackunit racket/runtime-path)
(require lib/test-helper)

(define-runtime-path here ".")

;; A trivial solver that returns the first line of input
(define (first-line-solver in)
  (read-line in))

(define test-dir (build-path here "test-fixtures"))

(test-case "check-solve passes when solver returns expected value"
  (check-solve first-line-solver test-dir
    '(("hello.txt" "hello world"))))

(test-case "check-solve fails when solver returns wrong value"
  (check-exn exn:test:check?
    (lambda ()
      (check-solve first-line-solver test-dir
        '(("hello.txt" "wrong answer"))))))

(test-case "check-solve runs multiple pairs"
  (check-solve first-line-solver test-dir
    '(("hello.txt" "hello world")
      ("hello2.txt" "hello world 2"))))
```

- [ ] **Step 2: Check content of `lib/test-fixtures/hello2.txt`**

Run: `snap run racket -e '(display (file->string "lib/test-fixtures/hello2.txt"))'`

If the first line is not `"hello world 2"`, adjust the expected value in the third test case to match the actual first line.

- [ ] **Step 3: Run the tests**

Run: `snap run raco test lib/test-helper-test.rkt`

Expected: 3 tests, 0 failures.

- [ ] **Step 4: Commit**

```bash
git add lib/test-helper.rkt lib/test-helper-test.rkt
git commit -m "refactor: replace run-diagnostic-tests with check-solve"
```

---

### Task 3: Update `aoc/2025/day01/1.rkt`

**Files:**
- Modify: `aoc/2025/day01/1.rkt`

- [ ] **Step 1: Update the test submodule**

Replace the `module+ test` block:

```racket
(module+ test
  (require/typed lib/test-helper
    [check-solve (-> (-> Input-Port String) Path (Listof (List String String)) Void)])
  (require racket/runtime-path)
  (define-runtime-path here ".")
  (check-solve solve here
    '(("diagnostic.txt" "15"))))
```

- [ ] **Step 2: Run the solution tests**

Run: `snap run raco test aoc/2025/day01/1.rkt`

Expected: 1 test, 0 failures.

- [ ] **Step 3: Commit**

```bash
git add aoc/2025/day01/1.rkt
git commit -m "refactor: update day01 to use check-solve"
```
