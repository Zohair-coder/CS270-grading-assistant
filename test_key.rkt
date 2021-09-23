#lang racket

; put the due date here in MM/DD/YYYY HH:MM (24hrs) format after the colon: 07/28/2021 23:59

; Total Questions: 8
; Total Points: 40
; Question 1a points: 4
; Question 1b points: 4
; Question 1c points: 4
; Question 1d points: 4
; Question 2a points: 6
; Question 2b points: 6
; Question 2c points: 6
; Question 2d points: 6

; Comments 1a:
; -1: test comment
;end

; Comments 1c:
; -0: testing minus nothing
;end

; Comments 2c:
; -1: first comment
; -1: second comment

; Comments 2d:
; -10: too many points cut off


(require rackunit)
(require rackunit/text-ui)
(define (check-equal? x y) (test-equal? "" x y))

;Question 1a: Addition
(define (add x y)
  (+ x y))
;end

;Question 1b: Subtraction
(define (subtract x y)
  (- x y))
;end

;Question 1c: Multiplication
(define (multiply x y)
  (* x y))
;end

;Question 1d: Division
(define (divide x y)
  (/ x y))
;end

;Question 2a: Addition by 1
  (define (addby1 x)
    (add 1 x))
;end

;Question 2b: Subtraction by 1
  (define (subtractby1 x)
    (subtract x 1))
;end

;Question 2c: Multiplication by 1
  (define (multiplyby1 x)
    (multiply 1 x))
;end

;Question 2a: Divide by 1
  (define (divideby1 x)
    (divide x 1))
;end
  
;Tests
(display "=================================\n")
(display "Points\n")
(display "=================================\n")
(display "Q1a: ")(display "4/4\n")
(display "Q1b: ")(display "4/4\n")
(display "Q1c: ")(display "4/4\n")
(display "Q1d: ")(display "4/4\n")
(display "Q2a: ")(display "6/6\n")
(display "Q2b: ")(display "6/6\n")
(display "Q2c: ")(display "6/6\n")
(display "Q2d: ")(display "6/6\n")
(display "Total: ")(display "40/40\n")
