#lang racket

(provide
 (contract-out
  [check-solve
   (-> solve/c
       path?
       (listof (list/c path-string? string?))
       void?)]))

(require rackunit lib/contracts)

;; check-solve : (InputPort -> String) Path (Listof (List path-string? String)) -> Void
;;
;; For each (filename expected) pair, opens the file at (build-path dir filename),
;; calls solve, and asserts the result equals expected.
(define (check-solve solve dir pairs)
  (for ([pair (in-list pairs)])
    (define filename (first pair))
    (define expected (second pair))
    (define file-path (build-path dir filename))
    (define result
      (call-with-input-file file-path
        (lambda (in) (solve in))))
    (with-check-info (['file (path->string file-path)])
      (check-equal? result expected))))
