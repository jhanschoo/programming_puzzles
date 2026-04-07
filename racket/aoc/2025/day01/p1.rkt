#lang racket

(require aoc/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (define-values (_ result)
    (for/fold
      ([curr 50] [count-0 0])
      ([line (in-lines in)] #:when (>= (string-length line) 2))
      (define dir (string-ref line 0))
      (define delta (string->number (substring line 1)))
      (define next (modulo (match dir [#\L (- curr delta)] [#\R (+ curr delta)]) 100))
      (define next-count-0 (if (= 0 next) (+ count-0 1) count-0))
      (values next next-count-0)))
  (number->string result))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "diagnostic.txt") solve) "3"))
