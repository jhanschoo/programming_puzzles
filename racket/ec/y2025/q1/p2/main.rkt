#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (match-define (list names-str instructions-str)
    (~> in port->string string-trim string-split))
  (define names (string-split names-str ","))
  (define num-names (length names))
  (define instructions (string-split instructions-str ","))
  (define idx
    (modulo (for/sum ([instr instructions])
              (let ([dir (string-ref instr 0)]
                    [num (string->number (substring instr 1))])
                (match dir
                  [#\L (- num)]
                  [#\R num]))) num-names))
  (list-ref names idx))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "Elarzris"))
