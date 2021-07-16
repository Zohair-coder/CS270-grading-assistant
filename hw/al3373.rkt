; Anthony Lam al3373 CS270
#lang racket

;The following two lines are required to test the code.
(require rackunit)
(require rackunit/text-ui)

#| CS 270  Homework 2
Create By Professor Bruce Char, Professor Mark Boady, Professor Jeremy Johnson, and Steve Earth

Complete each of the below functions.
Tests given are not resigned to be comprehensive.
They will give you an idea if your code is write, but they do not test all possible cases.
Think about your design. When grading, we may add additional tests for your functions.
When implementing questions 7-15, you may use any other functions that you wrote in earlier questions.

Important Rules:
0. Run your code before submitting it; if it crashes, A ZERO MAY BE GIVEN FOR THE ASSIGNMENT
1. You may not use any loop constructs; if used, your answer will get a zero.
2. All these functions must be implemented recursively -- you will receive a zero if there is no recursion.
Note that for some questions, recursive helper functions are allowed
(in which case, the grader will still give credit even with the main function not being recursive).
3. You may not use any Racket commands not discussed in class. If used, your answer will get a zero.
As a general rule, you should only be using functions taught in class (otherwise you are likely missing
the point of the question and endangering your score).
4. Using If/Cond to pass the specific tests provided instead of following the instructions will always
result in a zero for that question.  Do not assume that simply because your code passes all the example
unit tests here then that means you get 100%; we will be testing with input beyond the examples.
The graders will still obey the input contracts.

Special directions for Questions 1-6:
You may only use (if ...), #t, #f, input arguments. All other functions are forbidden.
For example, do not use =, eq?, or equal?
Be sure to use the boolean literals #t/#f vs spelling it out as true/false, which is slightly different
This homework demonstrates that all boolean operations can be written within these simple restrictions. |#

;EXAMPLE: the NAND Operator 
;Input: a,b are boolean expressions (i.e. evaluate to #t or #f)
;Output: (nandi a b) is True if and only if either a or b (or both) is False.
(define (nandi a b)
  (if a (if b #f #t) #t)
)

; Question 1
; logical negation
; input:  b is a boolean expression
; output:  (noti b) is the other boolean constant which is not b.
(define (noti b)
  (if b #f #t) ;return the opposite of b
 )

;Tests
(define-test-suite testnoti
  (test-equal? ""
    (noti #f) #t)
  (test-equal? ""
    (noti #t) #f))
(display "Question 1 noti (2 points)\n")
(define q1_score (- 2 (run-tests testnoti 'verbose)))


;Question 2: logical and
; input:  a and b are boolean expressions
; output:  (andi a b) is a boolean which is True if and only if a and b are both True.

;because a and b are always boolean expressions, there's no point in doing (if a #t #f) or (if b #t #f). just return a or b
(define (andi a b)
  (if b a #f) ;therefore if both are true, then it'll return true. otherwise, it'll always return false.   
)

;Tests
(define-test-suite testandi
  (test-equal? ""
    (andi #f #f) #f)
  (test-equal? ""
    (andi #f #t) #f)
  (test-equal? ""
    (andi #t #f) #f)
  (test-equal? ""
    (andi #t #t) #t))
(display "Question 2 andi (4 points)\n")
(define q2_score (- 4 (run-tests testandi 'verbose)))


;Question 3: logical or
; input:  a and b are boolean expressions
; output:  (ori a b) is a boolean which is False if and only if a and b are both False.

;because a and b are always boolean expressions, there's no point in doing (if a #t #f) or (if b #t #f). just return a or b
(define (ori a b)
  (if a #t b) ;if both a and b are false, then it'll return false. otherwise, it'll always return true
)

;Tests
(define-test-suite testori
  (test-equal? ""
    (ori #f #f) #f)
  (test-equal? ""
    (ori #f #t) #t)
  (test-equal? ""
    (ori #t #f) #t)
  (test-equal? ""
    (ori #t #t) #t))
(display "Question 3 ori (4 points)\n")
(define q3_score (- 4 (run-tests testori 'verbose)))


;Question 4: logical xor
; input:  a, b are boolean expressions
; output:  (xori a b) is a boolean constant which is true if and only if exactly one of a or b is true.

;Wasn't sure if we were allowed to use previous functions developed.
;because a and b are always boolean expressions, there's no point in doing (if a #t #f) or (if b #t #f). just return a or b
(define (xori a b)
  (if a (if b #f #t) b) ;I set it up so that if a is true, then it'll return not b. Otherwise, if a is false, it'll return b.
                                   ;This makes it so that it's only possible to have #t #f or #f #t return #t
)

;Tests
(define-test-suite testxori
  (test-equal? ""
    (xori #f #f) #f)
  (test-equal? ""
    (xori #f #t) #t)
  (test-equal? ""
    (xori #t #f) #t)
  (test-equal? ""
    (xori #t #t) #f))
(display "Question 4 xori (4 points)\n")
(define q4_score (- 4 (run-tests testxori 'verbose)))


;Question 5: logical implication
; input:  a,b are boolean expressions
; output:  (impliesi a b) is a boolean which is False if and only if a is true and b is false.

;because a and b are always boolean expressions, there's no point in doing (if a #t #f) or (if b #t #f). just return a or b
(define (impliesi a b)
  (if a b #t) ;Since false only occurs when a is true and b is false, put b in the true part so that if b is false, it'll return false. Otherwise, it'll always be true.  
)

;Tests
(define-test-suite testimpliesi
  (test-equal? ""
    (impliesi #f #f) #t)
  (test-equal? ""
    (impliesi #f #t) #t)
  (test-equal? ""
    (impliesi #t #f) #f)
  (test-equal? ""
    (impliesi #t #t) #t))
(display "Question 5 impliesi (4 points)\n")
(define q5_score (- 4 (run-tests testimpliesi 'verbose)))


;Question 6: logical iffi
; input:  a,b are boolean expressions
; output:  (iffi a b) is True if and only if a and b are the same

;because a and b are always boolean expressions, there's no point in doing (if a #t #f) or (if b #t #f). just return a or b
(define (iffi a b)
  (if a b (if b #f #t)) ;if a and b are both true, then it'll always return true. I did not b for the false part because this is how it'll return true when both are false. 
)

;Tests
(define-test-suite testiffi
  (test-equal? ""
    (iffi #f #f) #t)
  (test-equal? ""
    (iffi #f #t) #f)
  (test-equal? ""
    (iffi #t #f) #f)
  (test-equal? ""
    (iffi #t #t) #t))
(display "Question 6 iffi (4 points)\n")
(define q6_score (- 4 (run-tests testiffi 'verbose)))


;Question 7: do NOT use recursion (or any helper functions) in this problem.
; You may only use functions learned in class.
; Input: L is a list of booleans
; Output: (andlist L) is a boolean which is True if and only if every member of L is True
; (in other words, it is ANDing together everything in the list)

(define (andlist L)
  (foldl andi #t L) ;Called the andi function on the list. By folding, it will go through the list and return true is all elements match each other. 
)                   ;If the list is empty, it'll return true because of the initial value of the list. 

;Tests
(define-test-suite testandlist
  (test-equal? ""
    (andlist '()) #t)
  (test-equal? ""
    (andlist '(#t #t #t)) #t)
  (test-equal? ""
    (andlist '(#t #f #t)) #f)
  (test-equal? ""
    (andlist '(#t #t #t #t #f)) #f))
(display "Question 7 andlist (4 points)\n")
(define q7_score (- 4 (run-tests testandlist 'verbose)))


;Question 8: do NOT use recursion (or any helper functions) in this problem.
; You may only use functions learned in class.
; Input: L is a list of booleans
; Output: (orlist L) is a boolean which is False if and only if every member of L is False
; (in other words, it is ORing together everything in the list)

(define (orlist L)
  (foldl ori #f L) ;Called the ori function and fold on the list. This lets it go through the list and return true if there's at least one true.
)                  ;If the list is empty, it'll return false because of the initial value. 

;Tests
(define-test-suite testorlist
  (test-equal? ""
    (orlist '()) #f)
  (test-equal? ""
    (orlist '(#f #f #f)) #f)
  (test-equal? ""
    (orlist '(#t #f #t)) #t)
  (test-equal? ""
    (orlist '(#f #t #t #t #t)) #t))
(display "Question 8 orlist (4 points)\n")
(define q8_score (- 4 (run-tests testorlist 'verbose)))

;Question 9
; Write a recursive function all_q to check if a list of symbols contains all q symbols.
; Hint: You can use equal? on symbols. e.g. (equal? 'q 'b) returns #f, (equal? 'b 'b) returns #t

; Input:  L is a list of symbols (possibly empty)
; Output: (all_q L) a boolean value which is false if and only if L contains a symbol which isn't q
(define (all_q L)
  (cond
    [(null? L) #t] ;Check if the list is null. If so, return true because it only cares if the L has a symbol that isn't q. 
    [(equal? (first L) 'q) (all_q (rest L))] ;Otherwise, check the first element of the list. If it equals q, then perform recursion by calling the function again and taking the rest of the list.
    [else #f]) ;If there's an element that isn't q, stop the function and return #f 
)

(define-test-suite test_all_q
  (test-equal? "" (all_q '(q)) #t)
  (test-equal? "" (all_q '(b)) #f)
  (test-equal? "" (all_q '(b c)) #f)
  (test-equal? "" (all_q '(c q)) #f)
  (test-equal? "" (all_q '(q t)) #f)
  (test-equal? "" (all_q '(q q)) #t)
  (test-equal? "" (all_q '(q x q)) #f)
  (test-equal? "" (all_q '(q q q)) #t)
  (test-equal? "" (all_q '(q q q q q q q q)) #t)
  (test-equal? "" (all_q '(q q q q w q q q)) #f))
(display "Question 9 all_q (10 points)\n")
(define q9_score (- 10 (run-tests test_all_q 'verbose)))

;Question 10
;Solve question 9 again. This time you may NOT write a recursive function; use andlist/orlist instead.
; Do not write helper functions for this question (use λ instead, if need be).

; Input:  L is a list of symbols (possibly empty)
; Output: (all_q_v2 L) a boolean value which is false if and only if L contains a symbol which isn't q
(define (all_q_v2 L)
  (andlist (map (lambda (x) (if (equal? x 'q) #t #f)) L)) ;Begin with mapping all the elements in the list to #t if they match 'q and #f otherwise.
)                                                         ;Then call the andlist function on this list which will perform a foldl and check if all elements match. 

(define-test-suite test_all_q_v2
  (test-equal? "" (all_q_v2 '(q)) #t)
  (test-equal? "" (all_q_v2 '(b)) #f)
  (test-equal? "" (all_q_v2 '(b c)) #f)
  (test-equal? "" (all_q_v2 '(c q)) #f)
  (test-equal? "" (all_q_v2 '(q t)) #f)
  (test-equal? "" (all_q_v2 '(q q)) #t)
  (test-equal? "" (all_q_v2 '(q x q)) #f)
  (test-equal? "" (all_q_v2 '(q q q)) #t)
  (test-equal? "" (all_q_v2 '(q q q q q q q q)) #t)
  (test-equal? "" (all_q_v2 '(q q q q w q q q)) #f))
(display "Question 10 all_q_v2 (10 points)\n")
(define q10_score (- 10 (run-tests test_all_q_v2 'verbose)))


;Question 11
; Write a recursive function all_q to check if a list of symbols contains at least one q symbol.
; Input:  L is a list of symbols (possibly empty)
; Output: (at_least_one_q L) is a boolean which is true if and only if L contains a symbol q.
(define (at_least_one_q L)
  (cond
    [(null? L) #f] ;If the list is null, return #f because it's true if and only if L contains at least 1 q
    [(equal? (first L) 'q)] ;Check if the first element in the list is equal to q. If true, return true and exit because we only need 1 q 
    [else (at_least_one_q (rest L))]) ;otherwise, perform recursion by calling the function and taking the rest of the list until the list is null
)

(define-test-suite test_at_least_one_q
  (test-equal? "" (at_least_one_q '(q)) #t)
  (test-equal? "" (at_least_one_q '(b)) #f)
  (test-equal? "" (at_least_one_q '(x y)) #f)
  (test-equal? "" (at_least_one_q '(v q)) #t)
  (test-equal? "" (at_least_one_q '(q q)) #t)
  (test-equal? "" (at_least_one_q '(x x d)) #f)
  (test-equal? "" (at_least_one_q '(c t q)) #t)
  (test-equal? "" (at_least_one_q '(q q q)) #t)
  (test-equal? "" (at_least_one_q '(q w q q)) #t)
  (test-equal? "" (at_least_one_q '(x y d w)) #f))
(display "Question 11 at_least_one_q (10 points)\n")
(define q11_score (- 10 (run-tests test_at_least_one_q 'verbose)))


;Question 12
; Solve question 11 again. This time you may NOT write a recursive function; use andlist/orlist instead.
; Do not write helper functions for this question (use λ instead, if need be).
; Input:  L is a list of symbols (possibly empty)
; Output: (at_least_one_q L) is a boolean which is true if and only if L contains a symbol q.
(define (at_least_one_q_v2 L)
  (orlist (map (lambda (x) (if (equal? x 'q) #t #f)) L)) ;Begin with mapping all the elements in the list to #t if they match 'q and #f otherwise.
)                                                        ;Call the orlist function which folds and checks if there's at least one #t. otherwise it'll return #f

(define-test-suite test_at_least_one_q_v2
  (test-equal? "" (at_least_one_q_v2 '(q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(b)) #f)
  (test-equal? "" (at_least_one_q_v2 '(x y)) #f)
  (test-equal? "" (at_least_one_q_v2 '(v q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(q q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(x x d)) #f)
  (test-equal? "" (at_least_one_q_v2 '(c t q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(q q q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(q w q q)) #t)
  (test-equal? "" (at_least_one_q_v2 '(x y d w)) #f))
(display "Question 12 at_least_one_q_v2 (10 points\n)")
(define q12_score (- 10 (run-tests test_at_least_one_q_v2 'verbose)))


;Question 13
; Input:  L is a list of symbols (possibly empty).
; Output: (exactly_one_q L) is true if and only if L contains exactly one q.
; Hint: The answer to question 11 is helpful to use here.
(define (exactly_one_q L)
  (cond
    [(null? L) #f] ;check if the list is null. if so, return false because it's true if and only if L contains exactly 1 q
    [(equal? (first L) 'q) (noti (at_least_one_q (rest L)))] ;check if the first element is equal to q. if true, run the at_least_one_q function that checks if the rest of the list contains q.
                                                             ;Then take the not of this boolean in order to show that it's true that there's no other q's and false otherwise.   
    [else (exactly_one_q (rest L))]) ;otherwise take the rest of the list
)

(define-test-suite test_exactly_one_q
  (test-equal? "" (exactly_one_q '(q)) #t)
  (test-equal? "" (exactly_one_q '(x)) #f)
  (test-equal? "" (exactly_one_q '(z r)) #f)
  (test-equal? "" (exactly_one_q '(q d)) #t)
  (test-equal? "" (exactly_one_q '(q q)) #f)
  (test-equal? "" (exactly_one_q '(d e p)) #f)
  (test-equal? "" (exactly_one_q '(q b q)) #f)
  (test-equal? "" (exactly_one_q '(q q q)) #f)
  (test-equal? "" (exactly_one_q '(q n q q)) #f)
  (test-equal? "" (exactly_one_q '(m n m q)) #t))
(display "Question 13 exactly_one_q (10 points)\n")
(define q13_score (- 10 (run-tests test_exactly_one_q 'verbose)))


;Question 14.
; Write a recursive function odd_amt_q to check if a list of symbols contains an odd number of q symbols.
; Input:  L is a list of symbols (possibly empty).
; Output: (odd_amt_q L) is true if and only if the amount of q's in L is odd.
; Hint: if you are counting the total number of q's, then you are not going about it in a good way.
(define (odd_amt_q L)
  (cond
    [(null? L) #f] ;Check if the list is null. if it is, return false because 0 is neither odd or even. 
    [(equal? (first L) 'q) (noti (odd_amt_q (rest L)))] ;check if the first element is equal to q. if it is, then perform recursion, but use the noti boolean function in order to return false if there is another q.
                                                        ;This will cause it to flip between trues and false depending on if it's odd or not. 
    [else (odd_amt_q (rest L))]) ;otherwise, perform recursion by calling the function again and using the rest of the list
)

(define-test-suite test_odd_amt_q
  (test-equal? "" (odd_amt_q '(q)) #t)
  (test-equal? "" (odd_amt_q '(h i)) #f)
  (test-equal? "" (odd_amt_q '(k q)) #t)
  (test-equal? "" (odd_amt_q '(q z)) #t)
  (test-equal? "" (odd_amt_q '(t f b)) #f)
  (test-equal? "" (odd_amt_q '(u w q)) #t)
  (test-equal? "" (odd_amt_q '(q r q)) #f)
  (test-equal? "" (odd_amt_q '(q q q)) #t)
  (test-equal? "" (odd_amt_q '(x q q)) #f)
  (test-equal? "" (odd_amt_q '(q q q q)) #f))
(display "Question 14 odd_amt_q (10 points)\n")
(define q14_score (- 10 (run-tests test_odd_amt_q 'verbose)))


;Question 15.
; Solve question 14 again. This time you may NOT write a recursive function.
; Do not write helper functions for this question (use λ instead, if need be).
; Input:  L is a list of symbols (possibly empty).
; Output: (odd_amt_q L) is true if and only if the amount of q's in L is odd.

(define (odd_amt_q_v2 L)
  (foldl xori #f (map (lambda (x) (if (equal? x 'q) #t #f)) L)) ;map all the elements in the list that equal to 'q true and false otherwise. Then, fold with initial value #f so that if the list is empty, it returns false. 
)                                                               ;Then, do xori throughout the list. It will do (xori (first L) init) and then take that result and keep going until the list is empty. 

(define-test-suite test_odd_amt_q_v2
  (test-equal? "" (odd_amt_q_v2 '(q)) #t)
  (test-equal? "" (odd_amt_q_v2 '(h i)) #f)
  (test-equal? "" (odd_amt_q_v2 '(k q)) #t)
  (test-equal? "" (odd_amt_q_v2 '(q z)) #t)
  (test-equal? "" (odd_amt_q_v2 '(t f b)) #f)
  (test-equal? "" (odd_amt_q_v2 '(u w q)) #t)
  (test-equal? "" (odd_amt_q_v2 '(q r q)) #f)
  (test-equal? "" (odd_amt_q_v2 '(q q q)) #t)
  (test-equal? "" (odd_amt_q_v2 '(q x q)) #f)
  (test-equal? "" (odd_amt_q_v2 '(q q q q)) #f))
(display "Question 15 odd_amt_q_v2 (10 points)\n")
(define q15_score (- 10 (run-tests test_odd_amt_q_v2 'verbose)))

;---------------------------------------------------------------------
(display "------Test Summary------\n")
(display "Q1 passed ")
(display q1_score)
(display "/2\n")
(display "Q2 passed ")
(display q2_score)
(display "/4\n")
(display "Q3 passed ")
(display q3_score)
(display "/4\n")
(display "Q4 passed ")
(display q4_score)
(display "/4\n")
(display "Q5 passed ")
(display q5_score)
(display "/4\n")
(display "Q6 passed ")
(display q6_score)
(display "/4\n")
(display "Q7 passed ")
(display q7_score)
(display "/4\n")
(display "Q8 passed ")
(display q8_score)
(display "/4\n")
(display "Q9 passed ")
(display q9_score)
(display "/10\n")
(display "Q10 passed ")
(display q10_score)
(display "/10\n")
(display "Q11 passed ")
(display q11_score)
(display "/10\n")
(display "Q12 passed ")
(display q12_score)
(display "/10\n")
(display "Q13 passed ")
(display q13_score)
(display "/10\n")
(display "Q14 passed ")
(display q14_score)
(display "/10\n")
(display "Q15 passed ")
(display q15_score)
(display "/10\n")

(define grand_total (+ q1_score q2_score q3_score q4_score q5_score q6_score q7_score q8_score q9_score q10_score q11_score q12_score q13_score q14_score q15_score))
(display "\n")
(display "Total successes: ")
(display grand_total)
(display "/100\n")