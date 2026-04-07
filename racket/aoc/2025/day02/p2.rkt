#lang racket

(require lib/aoc)
(provide (contract-out [solve solve/c]))

(define/contract (string->integer s)
  (-> string? exact-integer?)
  (string->number s))

(define/contract (exp10i i)
  (-> integer? exact-integer?)
  (expt 10 i))

;; Collect all invalid IDs (as integers) in the closed range [l-s, u-s].
;; An invalid ID is formed by concatenating a half-word w with itself: w++w.
;;
;; l-s     : inclusive lower bound (decimal string)
;; u-s     : exclusive upper bound (decimal string)
;; returns : set of invalid ID integers in the closed range [l-s, u-s]
(define/contract (accumulate-invalid-ids l-s u-s)
  (-> string? string? (set/c integer?))
  (define l (string->integer l-s))
  (define u (string->integer u-s))
  (define w-max-p (quotient (string-length u-s) 2))
  (define lo (max 10 l))
  (for*/set
    ([p (in-range 1 (add1 w-max-p))]
     [n (in-range (exp10i (sub1 p)) (exp10i p))]
     [w (in-stream
          (let loop ([v n])
            (cond
              [(u . < . v) empty-stream]
              [(v . < . lo) (loop (+ n (* v (exp10i p))))]
              [else (stream-cons v (loop (+ n (* v (exp10i p)))))])))])
    ; (display (format "Processing w in range [~a, ~a], ~a: ~a\n" l u n w))
    w))

(define (solve in)
  (define in-str (string-trim (port->string in)))
  (define range-list (string-split in-str ","))
  (number->string
    (for/sum ([s range-list])
      (match-define (list l-s u-s) (string-split s "-"))
      (define invalid-ids (accumulate-invalid-ids l-s u-s))
      (for/sum ([w (in-set invalid-ids)])
        w))))


(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "diagnostic.txt") solve) "4174379265"))
