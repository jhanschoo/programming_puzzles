#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (match-define (list Ax Ay) (map string->number (string-split (string-trim (port->string in) #px"(A=\\[|\\]|\\s)+") ",")))
  (define (cycle x y Cx Cy)
    (let*-values ([(x y) (values (- (* x x) (* y y)) (* 2 x y))]
                  [(x y) (values (quotient x 100000) (quotient y 100000))]
                  [(x y) (values (+ x Cx) (+ y Cy))])
      (values x y)))
  (define (within-bounds x y)
    (and (<= -1000000 x 1000000)
         (<= -1000000 y 1000000)))
  (define total
    (for*/sum ([Cy (in-inclusive-range Ay (+ Ay 1000))]
               [Cx (in-inclusive-range Ax (+ Ax 1000))])
      (define-values (x y)
        (for/fold
          ([x 0] [y 0])
          ([_ (in-range 100)])
          #:break (not (within-bounds x y))
          (cycle x y Cx Cy)))
      (if (within-bounds x y) 1 0)))
  (number->string total))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "406954"))
