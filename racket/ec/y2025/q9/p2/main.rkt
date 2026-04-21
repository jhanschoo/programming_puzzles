#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (tails lst)
  (match lst
    ['() '()]
    [(cons _ t) (cons lst (tails t))]))

(define (bool->int b) (if b 1 0))

(define (solve in)
  (define samples (for/list ([line (in-lines in)]) (cadr (string-split line ":"))))
  (number->string
    (for*/sum
      ([sl1 (tails samples)]
       #:unless (empty? (rest sl1))
       [sl2 (tails (rest sl1))]
       #:unless (empty? (rest sl2))
       [s3 (rest sl2)])
      (define s1 (first sl1))
      (define s2 (first sl2))
      (for/fold
        ([s12 0] [s13 0] [s23 0] [child1 #t] [child2 #t] [child3 #t]
         #:result
         (+
           (* s12 s13 (bool->int child1))
           (* s12 s23 (bool->int child2))
           (* s13 s23 (bool->int child3))))
        ([c1 s1] [c2 s2] [c3 s3])
        (define c12=? (char=? c1 c2))
        (define c13=? (char=? c1 c3))
        (define c23=? (char=? c2 c3))
        (values
          (if c12=? (add1 s12) s12)
          (if c13=? (add1 s13) s13)
          (if c23=? (add1 s23) s23)
          (and child1 (or c12=? c13=?))
          (and child2 (or c12=? c23=?))
          (and child3 (or c13=? c23=?)))))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "1245"))
