;type your name after the colon:

; Question 1: Sample question. Question summary goes here.
; Make sure there is a semi-colon right before "Question 1:" even if it is a multi-line comment.
; The answer starts with the first "(define" statement that appears after "Question 1:"
; and ends right before the ;end comment.

(define (lookup target environment)
  0);Implement Me

;end

; Question 2,3,4 5: Sample questions 2, 3, 4 and 5. Multiple questions testing the same function can be grouped like so.
; All 4 questions would have the same function printed out when the program is run.
(define (bool-eval expression environment)
  (cond
    [(is-constant? expression) (eval-constant expression environment)] ;Case 1 Constants
    [(is-variable? expression) (eval-variable expression environment)] ;Case 2 Variables
    [(is-or? expression) (eval-or expression environment)]             ;Case 3 or statements
    ;Case 4 implement not statements
    ;Case 5 implement and statements
    ;Case 6 implement implies statements
    ;Case 7 implement iff statements
    [else null])) ; note that this else case should never be hit because of the input contract

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
; Q5 passed 6/10