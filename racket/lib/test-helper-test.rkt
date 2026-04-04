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
      ("hello2.txt" "hello world"))))
