#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (~>
    in
    port->string
    string-trim
    (string-split ",")
    (map string->number _)
    remove-duplicates
    (apply + _)
    number->string))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "29"))
