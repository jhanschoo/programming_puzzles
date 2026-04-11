#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (parse-ratio s)
  (if
    (string-contains? s "|")
    (string->number (string-replace s "|" "/"))
    (/ 1 (string->number s))))

(define (solve in)
  ; Assumption: first and last gears are are not compound
  (define f (string->number (read-line in)))
  (number->string
    (floor
      (for/product
        ([gear (in-lines in)])
        (if (string-contains? gear "|")
            (/ 1 (string->number (string-replace gear "|" "/")))
            (* 100 f (/ 1 (string->number gear))))))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "400")
  (check-equal? (call-with-input-file (build-path here "example2.txt") solve) "6818"))
