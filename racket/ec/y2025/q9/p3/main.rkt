#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(module union-find-vector racket
  (provide
    (contract-out
      [union-find-vector? (-> any/c boolean?)]
      [make-union-find-vector (-> exact-integer? union-find-vector?)]
      [union-find-vector-union (-> union-find-vector? exact-integer? exact-integer? void?)]
      [union-find-vector-find (-> union-find-vector? exact-integer? exact-integer?)]
      [union-find-vector-size (-> union-find-vector? exact-integer? exact-integer?)]))

  (struct union-find-vector (parents sizes))

  (define (make-union-find-vector size)
    (union-find-vector (for/vector #:length size ([i (in-range size)]) i) (make-vector size 1)))

  (define (union-find-vector-find uf i)
    (match-define (union-find-vector parents sizes) uf)
    (define (find i)
      (define p (vector-ref parents i))
      (cond
        [(= i p) i]
        [else
         (vector-set! parents i (vector-ref parents p))
         (find p)]))
    (find i))

  (define (union-find-vector-union uf i j)
    (match-define (union-find-vector parents sizes) uf)
    (define root-i (union-find-vector-find uf i))
    (define root-j (union-find-vector-find uf j))
    (define root-i-size (vector-ref sizes root-i))
    (define root-j-size (vector-ref sizes root-j))
    (unless (= root-i root-j)
      (define a (if (< root-i-size root-j-size) root-i root-j))
      (define b (if (< root-i-size root-j-size) root-j root-i))
      (vector-set! parents a b)
      (vector-set! sizes b (+ root-i-size root-j-size))))

  (define (union-find-vector-size uf i)
    (match-define (union-find-vector _ sizes) uf)
    (vector-ref sizes (union-find-vector-find uf i))))

(require 'union-find-vector)

(define (tails lst)
  (match lst
    ['() '()]
    [(cons _ t) (cons lst (tails t))]))

(define (solve in)
  (define samples (for/list ([line (in-lines in)]) (cadr (string-split line ":"))))
  (define uf (make-union-find-vector (length samples)))

  (for
    ([sl1 (tails samples)]
     [i1 (in-naturals)]
     #:unless (empty? (rest sl1))
     [sl2 (tails (rest sl1))]
     [i2 (in-naturals (add1 i1))]
     #:unless (empty? (rest sl2))
     [s3 (rest sl2)]
     [i3 (in-naturals (add1 i2))])
    (define s1 (first sl1))
    (define s2 (first sl2))
    (when
      (for/fold
        ([child1 #t] [child2 #t] [child3 #t]
         #:result
         (or child1 child2 child3))
        ([c1 s1] [c2 s2] [c3 s3])
        (define c12=? (char=? c1 c2))
        (define c13=? (char=? c1 c3))
        (define c23=? (char=? c2 c3))
        (values
          (and child1 (or c12=? c13=?))
          (and child2 (or c12=? c23=?))
          (and child3 (or c13=? c23=?))))
      (union-find-vector-union uf i1 i2)
      (union-find-vector-union uf i2 i3)))
  (define
    largest-set
    (for/fold
      ([l-set -1] [l-size -1] #:result l-set)
      ([i (in-range (length samples))])
      (define current-set (union-find-vector-find uf i))
      (define current-size (union-find-vector-size uf current-set))
      (if (> current-size l-size) (values current-set current-size) (values l-set l-size))))
  (number->string
    (for/sum ([i (in-range (length samples))] #:when (= largest-set (union-find-vector-find uf i)))
      (add1 i))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "12")
  (check-equal? (call-with-input-file (build-path here "example2.txt") solve) "36"))
