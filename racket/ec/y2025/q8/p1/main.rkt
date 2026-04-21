#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve-p l nails)
  (define diff (/ nails 2))
  (for/sum
    ([prev-nail-idx l]
     [nail-idx (drop l 1)])
    (if (= (abs (- nail-idx prev-nail-idx)) diff) 1 0)))

(define (solve in)
  (solve-p (map string->number (string-split (string-trim (port->string in)) ",")) 32))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt")
                  (λ (in) (solve-p (map string->number (string-split (string-trim (port->string in)) ",")) 8))) 4))
