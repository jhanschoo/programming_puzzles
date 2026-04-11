#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (solve in)
  (define names (~> in read-line string-trim (string-split ",")))
  (read-line in) ; skip blank line
  (define rules
    (for/hash
      ([line (in-lines in)])
      (match-define (list ch prods-string) (string-split line " > "))
      (define prods (for/list ([p (string-split prods-string ",")]) (string-ref p 0)))
      (values (string-ref ch 0) prods)))
  (define (validate name)
    (for/fold
      ([prods (hash-keys rules)] [valid name] #:result valid)
      ([c (in-string name)])
      #:break (not valid)
      (if (ormap (λ (p) (equal? c p)) prods)
          (values (hash-ref rules c '()) name)
          (values '() #f))))
  (for/fold
    ([found #f])
    ([name names])
    #:break found
    (validate name)))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "Oroneth"))
