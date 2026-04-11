#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (add-to-fishbone fishbone n)
  (match fishbone
    ['() (list (list #f n #f))]
    [(cons (list #f m r) fb)
      #:when (< n m)
      (cons (list n m r) fb)]
    [(cons (list l m #f) fb)
      #:when (< m n)
      (cons (list l m n) fb)]
    [(cons s fb) (cons s (add-to-fishbone fb n))]))

(define (solve in)
  (match-define (list _ numbers-str) (string-split (string-trim (port->string in)) ":"))
  (define numbers (map string->number (string-split numbers-str ",")))
  (define fishbone (for/fold ([fb '()]) ([n numbers]) (add-to-fishbone fb n)))
  (string-join
    (for/list ([segment fishbone]) (number->string (second segment))) ""))


(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "581078"))
