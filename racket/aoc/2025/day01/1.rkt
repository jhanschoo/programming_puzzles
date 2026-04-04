#lang racket

(provide solve)

(define (solve in)
  (define total
    (for/sum ([line (in-lines in)]
              #:when (non-empty-string? line))
      (string->number line)))
  (number->string total))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (displayln (solve (open-input-file filename))))

(module+ test
  (require lib/test-helper racket/runtime-path)
  (define-runtime-path here ".")
  (run-diagnostic-tests solve here
    '(("diagnostic.txt" "15"))))
