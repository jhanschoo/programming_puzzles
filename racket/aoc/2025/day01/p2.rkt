#lang racket

(require aoc/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (let-values ([(_ result)
                (for/fold
                  ([curr 50] [curr-0 0])
                  ([line (in-lines in)] #:when (>= (string-length line) 2))
                  (let*-values
                    ([(dir) (string-ref line 0)]
                     [(delta-abs) (string->number (substring line 1))]
                     [(delta) (match dir [#\L (- delta-abs)] [#\R delta-abs])]
                     [(next) (+ curr delta)]
                     [(through-0-base) (or (and (<= next 0) (< 0 curr)) (and (< curr 0) (<= 0 next)))]
                     [(through-0-excess next-rem) (quotient/remainder next 100)]
                     [(next-0) (+ curr-0 (abs through-0-excess) (if through-0-base 1 0))])
                    (values next-rem next-0)))])
    (number->string result)))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "diagnostic.txt") solve) "6"))
