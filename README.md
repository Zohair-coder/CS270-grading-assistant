# CS270 Grading Assistant

This program helps me grade student submissions for CS270. It's meant to help grade rkt files

## Usage

Download the list of entire students from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Make sure to select comma as the delimiter and click submit and download the file.

A csv file will be generated. Place the csv file in the project root directory. Open getStudents.py with a text editor and change the read_filename variable to the name of the csv file. Run the program to generate a students.json file.

Next, go back to the grade center in Blackboard and select the homework column you want to grade by clicking the arrow right next to it. Then select Assignment File Download, select all and click submit to download the zip file. Extract the zip file into a folder named "hw" in the projects root directory. Run rename.py.

Now create a "key" directory and then create an "answers" and "comments" directory inside of it. Populate the answers and comments directory with as many text files as there are questions in the form {question_number}.txt. Open the grading key racket file and copy and paste the answers of individuals questions into the individual text files. Then, inside the comments directory, populate the text files with possible comments for each question.

Open up main.py and scroll the bottom where the checker object is being initialized. Change the input to however many questions are in your homework.

You're all set! Run main.py to run the program.