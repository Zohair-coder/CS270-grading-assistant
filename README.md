# CS270 Grading Assistant

This program helps me grade student submissions for CS270. It's meant to help grade rkt files

![screenshot](https://i.ibb.co/HY6cXLt/image.png)

## Usage

Download the list of entire students from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Make sure to select comma as the delimiter and click submit and download the file.

A csv file will be generated. Place the csv file in the project root directory. Open getStudents.py with a text editor and change the read_filename variable to the name of the csv file. Run the program to generate a students.json file.

Next, go back to the grade center in Blackboard and select the homework column you want to grade by clicking the arrow right next to it. Then select Assignment File Download, select all and click submit to download the zip file. Extract the zip file into a folder named "hw" in the projects root directory. Run rename.py.

Now create a "key" directory and then create an "answers" and "comments" directory inside of it. Populate the answers and comments directory with as many text files as there are questions in the form {question_number}.txt. Open the grading key racket file and copy and paste the answers of individuals questions into the individual text files. Then, inside the comments directory, populate the text files with possible comments for each question.

Open up main.py and scroll the bottom where the checker object is being initialized. Change the input to however many questions are in your homework.

You're all set! Run main.py to run the program.

## TODO

* ~~Fix Blackboard csv file feature to easily upload grades~~
* ~~Add ability to save custom comments~~
* ~~Add student name checker~~
* Parse student name text file from Blackboard instead of parsing the full grade center
* Write a script for copying grading key to key/answers
* Import all files to main.py so the user only has to run `python main.py`
* ~~Fix "view grading status" bug when all files have been graded~~
* View anonymous animal names instead of student names when grading to avoid bias
* Add ability to go back a submission when grading
* Add ability to edit any students grade from the main menu
* Create a document explaining what the requirements for making a question.rkt file should be to run this program successfully
* Create a "Mistake analysis" feature in the main menu that would show how many students made a specific mistake and their names
* Add an autograder option in the menu that checks all the submissions and adds comments automatically without any manual grading involved (feasability needs to be evaluated)
* Write more detailed documentation about how the program works and how to use the program with images
