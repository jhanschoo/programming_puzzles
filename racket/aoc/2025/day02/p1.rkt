#lang racket

(require aoc/c)
(provide (contract-out [solve solve/c]))

(define/contract (string->integer s)
  (-> string? exact-integer?)
  (string->number s))

(define/contract (integer->string n)
  (-> integer? string?)
  (if (= n 0) "0" (number->string n)))

(define/contract (exp10i i)
  (-> integer? exact-integer?)
  (expt 10 i))

;; Normalize the invalid ID range from `l-s` (inclusive) to `u-s` (exclusive)
;; An invalid ID `s` is a nonempty string of digits with no leading 0,
;; such that some `w` satisfies `s == w + w`. The returns are as follows:
;; `l` and `u` are integers such that all integers in `[l, u)` have string
;; representations `w` such that `s == w + w` is an invalid ID, and these
;; `s` exhaust the invalid IDs in `[l_str, u_str)`.
;;
;; l-s     : inclusive lower bound of the invalid-ID range (decimal string)
;; u-s     : exclusive upper bound of the invalid-ID range (decimal string)
;; returns : (values l u) — half-open integer range [l, u) of the half-words
(define/contract (normalize-invalid-ids-range l-s u-s)
  (-> string? string? (values integer? integer?))
  (define l-msb-l (quotient (string-length l-s) 2))
  (define u-msb-l (quotient (string-length u-s) 2))
  (define l-msb (substring l-s 0 l-msb-l))
  (define l-lsb (substring l-s l-msb-l))
  (define u-msb (substring u-s 0 u-msb-l))
  (define u-lsb (substring u-s u-msb-l))
  (define l
    (if (l-msb-l . < . (string-length l-lsb))
        (exp10i l-msb-l)
        (let ([l-msb (string->integer l-msb)]
              [l-lsb (string->integer l-lsb)])
          (if (l-msb . < . l-lsb)
              (add1 l-msb)
              l-msb))
        ))
  (define u
    (if (u-msb-l . < . (string-length u-lsb))
        (exp10i u-msb-l)
        (let ([u-msb (string->integer u-msb)]
              [u-lsb (string->integer u-lsb)])
          (if (u-msb . <= . u-lsb)
              (add1 u-msb)
              u-msb))
        ))
  (values l u))

;; Sum of all invalid IDs formed from half-words in [l, u) of length p.
;;
;; l, u    : half-open range of half-word integers
;; p       : length of each half-word (and the full ID has length 2p)
;; returns : sum of all such invalid IDs
(define/contract (sum-invalid-ids-p l u p)
  (-> integer? integer? integer? integer?)
  (if (u . <= . l)
      0
      (* (add1 (exp10i p)) (- u l) (+ u l -1) 1/2)))

;; Sum of all invalid IDs with half-words in [l, u).
;;
;; l, u    : half-open range of half-word integers
;; returns : sum of all invalid IDs whose half-word falls in [l, u)
(define/contract (sum-invalid-ids l u)
  (-> integer? integer? integer?)
  (define l-l (string-length (integer->string l)))
  (define u-l (string-length (integer->string u)))
  (if (= l-l u-l)
      (sum-invalid-ids-p l u l-l)
      (+
        (sum-invalid-ids-p l (exp10i l-l) l-l)
        (for/sum ([p (in-range (add1 l-l) u-l)])
          (sum-invalid-ids-p (exp10i (sub1 p)) (exp10i p) p))
        (sum-invalid-ids-p (exp10i (sub1 u-l)) u u-l))))

(define (solve in)
  (define in-str (string-trim (port->string in)))
  (define range-list (string-split in-str ","))
  (number->string
    (for/sum ([s range-list])
      (match-define (list l-s u-s) (string-split s "-"))
      (define-values (l u) (normalize-invalid-ids-range l-s u-s))
      (sum-invalid-ids l u))))


(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "input.txt") solve) "16793817782"))
