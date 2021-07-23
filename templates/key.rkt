#lang racket

; put the due date here in MM/DD/YYYY HH:MM (24hrs) format after the colon:

;Question 1:  Sample question. Question summary goes here.
; Make sure there is a semi-colon right before "Question 1:" even if it is a multi-line comment.
; The answer starts with the first "(define" statement that appears after "Question 1:"
; and ends right before the ;end comment.

(define (sub m n)
  (if (zero? n)
      m
      (sub (pred m) (pred n))))

;end

;Question 2,3,4:  Sample questions 2, 3 and 4. Multiple questions testing the same function can be grouped like so.
; All 3 questions would have the same function printed out when the program is run.

(define (div m n)
  (if (ltnat? m n) zero (succ (div (sub m n) n))))

;end

;---------------------------------------------------------------------
;---------------------------------------------------------------------
;---------------------------------------------------------------------
;;;;;;;;;;;;;;Unit Test Summary;;;;;;;;;;;;;;;;;;;;;;;

; make sure the results are printed out in the format:
; Q1 passed 5/5
; Q2 passed 5/5
; Q3 passed 10/10
; Q4 passed 8/10

