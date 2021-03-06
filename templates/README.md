## Questions

For the questions, make sure:

* there is a line at the top that reads:
```
;type your name after the colon:
```

* The question starts with:
```
; Question 1:
```
Make sure to replace the 1 with the question number, and make sure the questions start from 1 and progress without gaps (so 1, 2, 3, 4 not 1, 3, 6, 7) and there are no subparts to a question e.g. 4a, 4b, 4c. Simply make 3 different questions: 4, 5, 6 instead.

If you want to display the same answer for multiple questions, start your question like so:

```
; Question 1,2,3,4, 5:
```

* There is a `(define)` statement in between the question comment and end comment

* The default for an unattempted question should be
```
(define (myfunc a b)
  0);Implement Me
```
Make sure there is a `0);Implement Me` line.

* The question ends with:
```
;end
```

* The output tests at the end of the rkt file are displayed like so:
```
Q1 passed 4/5
```
Make sure to replace the number to the left of the / with the marks obtained and the numbers to the right of the / with total marks. Write down "passed" even if the answer gets a 0. The "passed" indicates the program didn't crash.

* The total points for any assignment SHOULD be 100. This is important for calculating the late penalties accurately.

## Key

The key has the exact same format as the questions file, but also needs to have this comment somewhere in the rkt file:
```
; put the due date here in MM/DD/YYYY HH:MM (24hrs) format after the colon:
```

Make sure to actually put in the date and time after the colon too.

## Comments

Comments should be in the format:
```
#1: -1 this is a sample comment
```
Where #1 is the question number, -1 are the marks to deduct and `this is a sample comment` is the description of the comment. Positive values cannot be deducted and hence would crash the program.

