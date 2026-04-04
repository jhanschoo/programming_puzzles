#lang racket

(require racket/runtime-path file/glob)

(define-runtime-path aoc-root-raw ".")
(define aoc-root (normalize-path aoc-root-raw))

;; Discover solution entry points: files named <digit>.rkt inside day<NN>/ dirs
(define (discover-solutions base-dir)
  ;; Three patterns to handle: aoc/, year/, and day/ as base-dir
  (define deep-pattern (build-path base-dir "**" "day*" "*.rkt"))
  (define shallow-pattern (build-path base-dir "day*" "*.rkt"))
  (define direct-pattern (build-path base-dir "*.rkt"))
  (define candidates
    (remove-duplicates
     (append (glob (path->string deep-pattern))
             (glob (path->string shallow-pattern))
             (glob (path->string direct-pattern)))))
  (filter
   (lambda (p)
     (define-values (parent-dir name _must1) (split-path p))
     (define-values (_grandparent dayname _must2) (split-path parent-dir))
     (and (path? name)
          (regexp-match? #rx"^[0-9]+\\.rkt$" (path->string name))
          (path? dayname)
          (regexp-match? #rx"^day" (path->string dayname))))
   candidates))

;; Discover input files matching input*.txt in a directory
(define (discover-inputs dir)
  (define pattern (build-path dir "input*.txt"))
  (glob (path->string pattern)))

;; Run a solution file against an input file, return output string
(define (run-solution solution-path input-path)
  (define-values (proc stdout stdin stderr)
    (subprocess #f #f (current-error-port)
                (find-executable-path "racket")
                (path->string solution-path)
                (path->string input-path)))
  (close-output-port stdin)
  (define output (port->string stdout))
  (close-input-port stdout)
  (subprocess-wait proc)
  (define status (subprocess-status proc))
  (values (string-trim output) status))

(module+ main
  (define target
    (command-line
     #:args ([path "."])
     path))

  (define base-dir
    (simplify-path (build-path aoc-root target)))

  (define solutions (discover-solutions base-dir))

  (when (null? solutions)
    (printf "No solutions found under ~a\n" base-dir)
    (exit 1))

  (for ([sol (in-list (sort solutions path<?))])
    (define dir (path-only sol))
    (define inputs (discover-inputs dir))
    (for ([inp (in-list (sort inputs path<?))])
      (define sol-rel (find-relative-path aoc-root sol))
      (define inp-rel (find-relative-path aoc-root inp))
      (printf "~a < ~a: " sol-rel inp-rel)
      (flush-output)
      (define-values (output status) (run-solution sol inp))
      (if (zero? status)
          (printf "~a\n" output)
          (printf "FAILED (exit ~a)\n" status)))))
