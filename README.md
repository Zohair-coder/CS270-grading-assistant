# CS270 Grading Assistant

This program helps me grade student submissions for CS270. It's meant to help grade rkt files

## Usage

Download the list of entire students from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Make sure to select comma as the delimiter and click submit and download the file.

A csv file will be generated. Place the csv file in the project root directory. Open getStudents.py with a text editor and change the read_filename variable to the name of the csv file. Run the program to generate a students.json file.

Next, go back to the grade center in Blackboard and select the homework column you want to grade by clicking the arrow right next to it. Then select Assignment File Download, select all and click submit to download the zip file. Extract the zip file into a folder named "hw" in the projects root directory. Run rename.py.

You're all set! Run main.py to run the program.