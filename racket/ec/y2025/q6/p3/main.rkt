#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve-p draft reps distance)
  (define people (make-hash))
  (define rep-length (string-length draft))
  (define aug-draft (string-join (list draft draft draft) ""))
  (define aug-length (string-length aug-draft))
  (define normal-mul (- reps 2))
  (for ([i (in-range distance)]) (hash-update! people (string-ref aug-draft i) add1 0))
  (for/sum
    ([i (in-range aug-length)])
    (define i-forward (+ i distance))
    (define i-backward (- i distance 1))
    (when (< i-forward aug-length)
      (hash-update! people (string-ref aug-draft i-forward) add1 0))
    (when (<= 0 i-backward)
      (hash-update! people (string-ref aug-draft i-backward) sub1))
    (define c (string-ref aug-draft i))
    (if (char-lower-case? c)
        (* (hash-ref people (char-upcase c) 0)
           (if (and (<= rep-length i) (< i (* 2 rep-length)))
               normal-mul
               1))
        0)))

(define (solve in)
  (number->string (solve-p (string-trim (port->string in)) 1000 1000)))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt")
                  (λ (in) (solve-p (string-trim (port->string in)) 1 10))) 34)
  (check-equal? (call-with-input-file (build-path here "example.txt")
                  (λ (in) (solve-p (string-trim (port->string in)) 2 10))) 72))
