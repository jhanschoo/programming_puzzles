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
