#lang typed/racket

(provide solve)

(: solve (-> Input-Port String))
(define (solve in)
  (number->string
   (for/sum : Integer ([line (in-lines in)]
                        #:when (non-empty-string? line))
     (assert (string->number line) exact-integer?))))

(module+ main
  (define filename (cast (command-line #:args (filename) filename) String))
  (displayln (solve (open-input-file filename))))

(module+ test
  (require/typed lib/test-helper
    [check-solve (-> (-> Input-Port String) Path (Listof (List String String)) Void)])
  (require racket/runtime-path)
  (define-runtime-path here ".")
  (check-solve solve here
    '(("diagnostic.txt" "15"))))
