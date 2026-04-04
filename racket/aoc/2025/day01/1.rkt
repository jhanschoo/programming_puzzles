#lang typed/racket

(provide solve)

(: solve (-> Input-Port String))
(define (solve in)
  (number->string
   (for/sum : Integer ([line (in-lines in)]
                        #:when (non-empty-string? line))
     (assert (string->number line) exact-integer?))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (displayln (solve (open-input-file (cast filename String)))))

(module+ test
  (require/typed lib/test-helper
    [run-diagnostic-tests (-> (-> Input-Port String) Path (Listof (List String String)) Void)])
  (require racket/runtime-path)
  (define-runtime-path here ".")
  (run-diagnostic-tests solve here
    '(("diagnostic.txt" "15"))))
