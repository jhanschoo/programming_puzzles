#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (string-last s) (string-ref s (sub1 (string-length s))))

(define (solve in)
  (define names (~> in read-line (string-split ",")))
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
  (define names-by-length (make-hash))
  (for ([name names] #:when (validate name))
    (hash-update!
      names-by-length
      (string-length name)
      (λ (s) (set-add! s name) s)
      (λ () (mutable-set))))
  (for* ([l (in-range 11)]
         [name (hash-ref names-by-length l (mutable-set))]
         [prod (hash-ref rules (string-last name) '())])
    (define new-name (string-append name (string prod)))
    (hash-update!
      names-by-length
      (add1 l)
      (λ (s) (set-add! s new-name) s)
      (λ () (mutable-set))))
  (number->string
    (for/sum
      ([i (in-range 7 12)])
      (set-count (hash-ref names-by-length i (mutable-set))))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "25")
  (check-equal? (call-with-input-file (build-path here "example2.txt") solve) "1154"))
