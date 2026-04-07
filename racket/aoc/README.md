# Advent of Code — Racket solutions

Solutions are organised by year and day under this directory.

## Directory layout

```
aoc/
├── c.rkt            # shared contract (solve/c)
└── 2025/
    └── day01/
        ├── p1.rkt           # part 1
        ├── p2.rkt           # part 2
        ├── diagnostic.txt   # sample input with known answer
        └── input.txt        # personal puzzle input
```

## Running solutions

All commands are run from the `racket/` package root.

| Goal | Command |
|------|---------|
| Run part 1 against personal input | `racket aoc/2025/day01/p1.rkt aoc/2025/day01/input.txt` |
| Run part 1 against sample input | `racket aoc/2025/day01/p1.rkt aoc/2025/day01/diagnostic.txt` |

## Testing

Each solution file contains a `module+ test` submodule that checks the answer against the sample input.

| Goal | Command |
|------|---------|
| Test one part | `raco test aoc/2025/day01/p1.rkt` |
| Test one day | `raco test aoc/2025/day01/` |
| Test a whole year | `raco test aoc/2025/` |
| Test everything | `raco test .` |

## Solution file skeleton

```racket
#lang racket

(require aoc/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  ;; read from `in`, return answer as a string
  ...)

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "diagnostic.txt") solve) "expected-answer"))
```
