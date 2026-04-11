#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (match-define (list Ax Ay)
    (~> in port->string (string-trim #px"(A=\\[|\\]|\\s)+") (string-split ",") (map string->number _)))
  (define (cycle x y)
    (let*-values ([(x y) (values (- (* x x) (* y y)) (* 2 x y))]
                  [(x y) (values (quotient x 10) (quotient y 10))]
                  [(x y) (values (+ x Ax) (+ y Ay))])
      (values x y)))
  (for/fold ([x 0] [y 0] #:result (format "[~a,~a]" x y)) ([_ (in-range 3)])
    (cycle x y)))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "[357,862]"))
