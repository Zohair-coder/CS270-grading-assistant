# CS270 Grading Assistant

This program helps me grade student submissions for CS270. It's meant to help grade rkt files.

![screenshot](https://i.ibb.co/HY6cXLt/image.png)

## Setup

If this is the first time you're using this program on your computer, follow these instructions:

### Windows
Locate where your Racket is installed. By default it should be in `C:\Program Files\Racket`.
Go inside the directory and copy the path.
Press start and search for "Edit the system environment variables".
Click "Environment variables" at the bottom right.
Click "Path" in the user variables and then click "Edit".
Click "New" on the top right and paste the path that you copied.
Click "OK" until all the windows have been closed.
Launch a terminal and type "Racket".
If the terminal displays `Welcome to Racket`, you have successfully installed Racket on the command line. You can now move on to the usage step.

## Usage

Open a terminal in a directory and type in the following command:
```
git clone https://github.com/Zohair-coder/CS270-grading-assistant.git
```
Download the list of entire students from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Make sure to select comma as the delimiter and click submit and download the file. A csv file will be generated. Place the csv file in the project root directory. Open main.py with a text editor and change the STUDENT_NAMES_CSV variable to the name of the csv file.

Download the grading file template from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Select "Selected Column" in the "Select Data to Download" field and select the homework you want to grade from the drop-down menu. Include comments for the column. Select the delimiter type as comma, and hit submit. Place the downloaded csv file into the root directory of the project and open main.py with a text editor. Change the value of GRADES_CSV to the name of the file that you just copied to the root of you project.

Next, go back to the grade center in Blackboard and select the homework column you want to grade by clicking the arrow right next to it. Then select Assignment File Download. Scroll to the bottom and click show all and then select all and click submit to download the zip file. Extract the zip file into a new folder named "hw" in the projects root directory.

In the root directory, create a new "key" directory with 2 sub-directories: "answers" and "comments". Inside the key directory, populate the answers and comments directory with as many text files as there are questions in the form {question_number}.txt. Open the grading key racket file and copy and paste the answers of individuals questions into the individual text files. Then, inside the comments directory, populate the text files with possible comments for each question.
If you have 5 questions to grade, your key directory should look like this:
```
/key
    |- answers
        |- 1.txt
        |- 2.txt
        |- 3.txt
        |- 4.txt
        |- 5.txt
    |- comments
        |- 1.txt
        |- 2.txt
        |- 3.txt
        |- 4.txt
        |- 5.txt
```

Make sure the comments follow the following format:
```
#1: -1 this is incorrect
```
You can also optionally leave the comments directory empty and input the comments inside the program.

Go back to the root directory and open a terminal and run the following command:
```
python main.py
```

## TODO

* ~~Fix Blackboard csv file feature to easily upload grades~~
* ~~Add ability to save custom comments~~
* ~~Add student name checker~~
* Parse student name text file from Blackboard instead of parsing the full grade center
* Unzip student answers automatically
* ~~Write a script for copying grading key to key/answers~~
* Import all files to main.py so the user only has to run `python main.py`
* ~~Fix "view grading status" bug when all files have been graded~~
* View anonymous animal names instead of student names when grading to avoid bias
* Add ability to go back a submission when grading
* Add ability to edit any students grade from the main menu
* Create a document explaining what the requirements for making a question.rkt file should be to run this program successfully
* Create a "Mistake analysis" feature in the main menu that would show how many students made a specific mistake and their names
* Add an autograder option in the menu that checks all the submissions and adds comments automatically without any manual grading involved (feasability needs to be evaluated)
* Write more detailed documentation about how the program works and how to use the program with images
