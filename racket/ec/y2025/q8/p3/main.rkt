#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(module max-segment-tree racket
  (provide
    (contract-out
      [max-segment-tree? (-> any/c boolean?)]
      [make-max-segment-tree (-> exact-integer? max-segment-tree?)]
      [max-segment-tree-add-to-range (-> max-segment-tree? exact-integer? exact-integer? exact-integer? void?)]
      [max-segment-tree-query-range (-> max-segment-tree? exact-integer? exact-integer? exact-integer?)]
      [max-segment-tree-query-all (-> max-segment-tree? exact-integer?)]))

  (struct max-segment-tree (n vals deferred))

  (define (vector-update! vec idx f . rest)
    (vector-set! vec idx (apply f (vector-ref vec idx) rest)))

  (define (make-max-segment-tree size)
    (define n (let loop ([n 1]) (if (< n size) (loop (* 2 n)) n)))
    (max-segment-tree n (make-vector (* 2 n) 0) (make-vector (* 2 n) 0)))

  (define (push-down st node)
    (match-define (max-segment-tree _ vals deferred) st)
    (define node-deferred (vector-ref deferred node))
    (unless (zero? node-deferred)
      (define left-child (* 2 node))
      (define right-child (add1 (* 2 node)))
      (vector-update! vals left-child + node-deferred)
      (vector-update! vals right-child + node-deferred)
      (vector-update! deferred left-child + node-deferred)
      (vector-update! deferred right-child + node-deferred)
      (vector-set! deferred node 0)))

  (define (update-range st node start end left right delta)
    (match-define (max-segment-tree _ vals deferred) st)
    (cond
      [(or (< right start) (< end left)) (void)]
      [(and (<= left start) (<= end right))
       (vector-update! vals node + delta)
       (vector-update! deferred node + delta)]
      [else
       (push-down st node)
       (define mid (quotient (+ start end) 2))
       (update-range st (* 2 node) start mid left right delta)
       (update-range st (add1 (* 2 node)) (add1 mid) end left right delta)
       (define left-val (vector-ref vals (* 2 node)))
       (define right-val (vector-ref vals (add1 (* 2 node))))
       (vector-set! vals node (max left-val right-val))
       (vector-set! deferred node 0)]))
  (define (query-range st node start end left right)
    (define vals (max-segment-tree-vals st))
    (cond
      [(or (< right start) (< end left)) -inf.0]
      [(and (<= left start) (<= end right))
       (vector-ref vals node)]
      [else
       (push-down st node)
       (define mid (quotient (+ start end) 2))
       (define left-val (query-range st (* 2 node) start mid left right))
       (define right-val (query-range st (add1 (* 2 node)) (add1 mid) end left right))
       (max left-val right-val)]))
  (define (max-segment-tree-add-to-range st left right delta)
    (unless (< right left)
      (update-range st 1 0 (sub1 (max-segment-tree-n st)) left right delta)))
  (define (max-segment-tree-query-range st left right)
    (query-range st 1 0 (sub1 (max-segment-tree-n st)) left right))
  (define (max-segment-tree-query-all st)
    (vector-ref (max-segment-tree-vals st) 1)))
(require 'max-segment-tree)

(define (solve-p l nails)
  (define st (make-max-segment-tree nails))
  (define segments
    (for/list
      ([s l] [e (drop l 1)])
      (if (<= s e) (cons (sub1 s) (sub1 e)) (cons (sub1 e) (sub1 s)))))
  (define events (make-vector nails '()))
  (define (cons-events! i el)
    (vector-set! events i (cons el (vector-ref events i))))
  (for ([segment segments])
    (match-define (cons s e) segment)

    (cons-events! 0 (list (add1 s) (sub1 e) 1))
    (cons-events! s (list (add1 s) (sub1 e) -1))

    (cons-events! s (list e e 1))
    (cons-events! (add1 s) (list e e -1))

    (cons-events! (add1 s) (list (add1 e) (sub1 nails) 1))
    (cons-events! e (list (add1 e) (sub1 nails) -1)))

  (for/fold ([global-max 0]) ([x-events events])
    (for ([x-event x-events])
      (match-define (list left right delta) x-event)
      (max-segment-tree-add-to-range st left right delta))
    (max global-max (max-segment-tree-query-all st))))

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
                  (λ (in) (solve-p (map string->number (string-split (string-trim (port->string in)) ",")) 8))) 7))
