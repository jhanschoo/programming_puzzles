#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (define f (string->number (read-line in)))
  (define l (for/fold ([_ f]) ([l (in-lines in)]) (string->number l)))
  (number->string (ceiling (/ (* 10000000000000 l) f))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "625000000000")
  (check-equal? (call-with-input-file (build-path here "example2.txt") solve) "1274509803922"))
