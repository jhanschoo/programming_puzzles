#lang racket

(provide solve/c)

;; Contract for AoC solution functions: reads from an input port, returns a string answer.
(define solve/c (-> input-port? string?))
