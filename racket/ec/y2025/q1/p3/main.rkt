#lang racket

(require ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (match-define (list names-str instructions-str) (string-split (string-trim (port->string in))))
  (define names (list->vector (string-split names-str ",")))
  (define num-names (vector-length names))
  (define instructions (string-split instructions-str ","))
  (for/fold ([name-0 (vector-ref names 0)])
            ([instr instructions])
    (let ([dir (string-ref instr 0)]
          [num (string->number (substring instr 1))])
      (define idx (modulo (match dir
                            [#\L (- num)]
                            [#\R num]) num-names))
      (define other (vector-ref names idx))
      (vector-set*! names 0 other idx name-0)
      other)))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "Drakzyph"))
