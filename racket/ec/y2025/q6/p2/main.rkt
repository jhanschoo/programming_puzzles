#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (define people (make-hash))
  (number->string
    (for/sum
      ([c (in-input-port-chars in)])
      (if (char-lower-case? c)
        (hash-ref people (char-upcase c) 0)
        (begin
          (hash-update! people c add1 0)
          0)))))


(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "11"))
