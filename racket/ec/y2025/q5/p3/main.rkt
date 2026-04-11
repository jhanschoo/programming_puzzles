#lang racket

(require threading ec/c)
(provide (contract-out [solve solve/c]))

(define (add-to-raw-fishbone raw-fishbone n)
  (match raw-fishbone
    ['() (list (list #f n #f))]
    [(cons (list #f m r) fb)
     #:when (< n m)
     (cons (list n m r) fb)]
    [(cons (list l m #f) fb)
     #:when (< m n)
     (cons (list l m n) fb)]
    [(cons s fb) (cons s (add-to-raw-fishbone fb n))]))

(define (quality fishbone)
  (string->number (string-join
                    (for/list ([segment (second fishbone)]) (number->string (second segment))) "")))

(define (line->fishbone line)
  (match-define (list id numbers-str) (string-split (string-trim line) ":"))
  (define numbers (map string->number (string-split numbers-str ",")))
  (define raw-fishbone (for/fold ([fb '()]) ([n numbers]) (add-to-raw-fishbone fb n)))
  (list (string->number id) raw-fishbone))

(define (segment->number segment)
  (string->number (string-join (for/list ([n segment]) (if (number? n) (number->string n) "")) "")))

(define (fishbone->fishbone-stats fishbone)
  (match-define (list id raw-fishbone) fishbone)
  (list (quality fishbone)
        (for/list ([segment raw-fishbone]) (segment->number segment))
        id))

(define (fishbone-stats< stats1 stats2)
  (match-define (list q1 segnum1 id1) stats1)
  (match-define (list q2 segnum2 id2) stats2)
  (cond
    [(< q1 q2) #t]
    [(> q1 q2) #f]
    [else
     (for/fold
       ([status 'undecided]
        #:result (if (boolean? status) status (< id1 id2)))
       ([s1 segnum1]
        [s2 segnum2])
       #:break (boolean? status)
       (match* (s1 s2)
         [('() '()) 'undecided]
         [('() _) #t]
         [(_ '()) #f]
         [(s1 s2) #:when (< s1 s2) #t]
         [(s1 s2) #:when (> s1 s2) #f]
         [(_ _) 'undecided]))
         ]))

(define (solve in)
  (define stats
    (~> in
      port->lines
      (map line->fishbone _)
      (map fishbone->fishbone-stats _)
      (sort fishbone-stats<)
      reverse))
  (number->string
    (for/sum
      ([stat stats]
        [i (in-naturals 1)])
      (* i (third stat)))))

(module+ main
  (define filename (command-line #:args (filename) filename))
  (call-with-input-file filename
    (λ (in) (displayln (solve in)))))

(module+ test
  (require rackunit racket/runtime-path)
  (define-runtime-path here ".")
  (check-equal? (call-with-input-file (build-path here "example.txt") solve) "260")
  (check-equal? (call-with-input-file (build-path here "example2.txt") solve) "4"))
