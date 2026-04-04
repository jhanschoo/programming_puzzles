#lang racket

(provide
 (contract-out
  [run-diagnostic-tests
   (-> (-> input-port? string?)
       path?
       (listof (list/c string? string?))
       void?)]))

(require rackunit file/glob)

;; run-diagnostic-tests : (InputPort -> String) Path (Listof (List String String)) -> Void
;;
;; For each (glob-pattern expected) pair, expands the glob relative to dir,
;; opens each matching file, calls solve, and asserts the result equals expected.
(define (run-diagnostic-tests solve dir pairs)
  (for ([pair (in-list pairs)])
    (define pattern (first pair))
    (define expected (second pair))
    (define full-pattern (build-path dir pattern))
    (define matches (glob (path->string full-pattern)))
    (when (null? matches)
      (fail (format "No files matched pattern: ~a" full-pattern)))
    (for ([file-path (in-list matches)])
      (define result
        (call-with-input-file file-path
          (lambda (in) (solve in))))
      (with-check-info (['file (path->string file-path)]
                        ['pattern pattern])
        (check-equal? result expected)))))
