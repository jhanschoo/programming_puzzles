#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(module fenwick-tree racket
  (provide
    (contract-out
      [fenwick-tree? (-> any/c boolean?)]
      [make-fenwick-tree (-> exact-integer? fenwick-tree?)]
      [fenwick-tree-incr (-> fenwick-tree? exact-integer? exact-integer? void?)]
      [fenwick-tree-sum (-> fenwick-tree? exact-integer? exact-integer?)]
      [fenwick-tree-sum-range-inclusive (-> fenwick-tree? exact-integer? exact-integer? exact-integer?)]))

  (struct fenwick-tree (tree))

  (define (make-fenwick-tree size)
    (fenwick-tree (make-vector (add1 size) 0)))
  (define (fenwick-tree-incr ft i delta)
    (let loop ([idx i])
      (when (< idx (vector-length (fenwick-tree-tree ft)))
        (vector-set! (fenwick-tree-tree ft)
                     idx
                     (+ (vector-ref (fenwick-tree-tree ft) idx) delta))
        (loop (+ idx (bitwise-and idx (- idx)))))))
  (define (fenwick-tree-sum ft i)
    (let loop ([idx i] [total 0])
      (if (<= idx 0) total
          (loop (- idx (bitwise-and idx (- idx)))
                (+ total (vector-ref (fenwick-tree-tree ft) idx))))))
  (define (fenwick-tree-sum-range-inclusive ft start end)
    (- (fenwick-tree-sum ft end) (fenwick-tree-sum ft (- start 1)))))
(require 'fenwick-tree)

(define (solve-p l nails)
  (define ft (make-fenwick-tree nails))
  (define segments
    (sort
      (for/list
        ([s l] [e (drop l 1)])
        (if (<= s e) (cons s e) (cons e s)))
      (lambda (a b)
        (match-let ([(cons sa ea) a] [(cons sb eb) b])
          (or (< sa sb) (and (= sa sb) (< eb ea)))))))
  (for/sum
    ([seg segments])
    (match-let ([(cons start end) seg])
      (fenwick-tree-incr ft end 1)
      (if (<= (+ start 1) (- end 1))
          (fenwick-tree-sum-range-inclusive ft (+ start 1) (- end 1))
          0))))

(define (solve in)
  (solve-p (map string->number (string-split (string-trim (port->string in)) ",")) 256))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt")
                  (λ (in) (solve-p (map string->number (string-split (string-trim (port->string in)) ",")) 8))) 21))
