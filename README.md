# CS270 Grading Assistant

This program helps me grade student submissions for CS270. It's meant to help grade rkt files.

![screenshot](https://i.ibb.co/HY6cXLt/image.png)

## Setup

If this is the first time you're using this program on your computer, follow these instructions:

Make sure you have [Racket](https://download.racket-lang.org/), [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed.

If you're using Windows or Mac, you'll also have to run this command after cloning the repository:

```
pip install -r requirements.txt
```

### Windows
Locate where your Racket is installed. By default it should be in `C:\Program Files\Racket`.
Go inside the directory and copy the path.
Press start and search for "Edit the system environment variables".

![start-menu](https://i.ibb.co/xG8T8vv/image.png)

Click "Environment variables" at the bottom right.

![menu](https://i.ibb.co/6ZcQR7v/image.png)

Click "Path" in the user variables and then click "Edit".

![menu](https://i.ibb.co/PTgg2HL/image.png)

Click "New" on the top right and paste the path that you copied.

![menu](https://i.ibb.co/4dBLYBJ/image.png)

Click "OK" until all the windows have been closed.
Launch a terminal and type "racket".
If the terminal displays `Welcome to Racket`, you have successfully installed Racket on the command line. You can now move on to the usage step.

![command prompt](https://i.ibb.co/vw4SdLy/image.png)

### Mac
Add racket to path if it isn't already by following the instructions [here](https://beautifulracket.com/setting-the-mac-os-path.html).

### Docker
If you want to avoid the complicated set up, you can alternatively use [Docker](https://docs.docker.com/get-docker/). Install Docker and make sure it's running. Then complete all the "Usage" steps given below. At the end, instead of running `python main.py`, just run
```
docker build -t cs270_grader .
```
Once that's done, run:
```
docker run -ti --rm -v /absolute/path/to/your/local/directory:/app cs270_grader
```

You do not need to install or set up Racket, Python or any of the Python modules using pip if you choose to use Docker. 

## Usage

Open a terminal in a directory and type in the following command:
```
git clone https://github.com/Zohair-coder/CS270-grading-assistant.git
```

![terminal with command](https://i.ibb.co/LzDnGyB/image.png)

A new folder with the repository name will be created. This is the project root folder.

Download the list of entire students from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Make sure to select comma as the delimiter and click submit and download the file.

![grade center](https://i.ibb.co/T17yqXg/image.png)

![download page](https://i.ibb.co/XZSnf1S/image.png)

A csv file will be generated. Place the csv file in the project root directory. Open main.py with a text editor and change the STUDENT_NAMES_CSV variable to the name of the csv file.

![file explorer](https://i.ibb.co/BncMVtb/image.png)

![text editor](https://i.ibb.co/0cZh2D4/image.png)

Download the grading file template from Blackboard by going to the full grade center, selecting Work Offline on the top right hand corner and clicking Download. Select "Selected Column" in the "Select Data to Download" field and select the homework you want to grade from the drop-down menu. Include comments for the column. Select the delimiter type as comma, and hit submit.

![download page](https://i.ibb.co/ZBmSXq3/image.png)

Place the downloaded csv file into the root directory of the project and open main.py with a text editor. Change the value of GRADES_CSV to the name of the file that you just copied to the root of you project. Make sure to put the filename in between the quotations.

Next, go back to the grade center in Blackboard and select the homework column you want to grade by clicking the arrow right next to it. Then select Assignment File Download.

![grade center](https://i.ibb.co/NV44tqb/image.png)


Scroll to the bottom and click show all and then select all and click submit to download the zip file.

![download page](https://i.ibb.co/842g8B3/image.png)

![download page](https://i.ibb.co/s1zK1fW/image.png)

Place the zip file in the root directory of the project. Open main.py with a text editor and change the value of ANSWERS_ZIP_FILE to the name of the zip file you just downloaded.

Copy the grading key rkt file into the root directory of the project.

![file explorer](https://i.ibb.co/XJkBmvp/image.png)

 Open main.py with a text editor and change the value of KEY_FILE to the name of the key rkt file.

Run the following command:
```
python main.py
```

You can add custom comments inside the program. Make sure the comments follow the following format:
```
#1: -1 this is incorrect
```
You can also optionally go inside key > comments to write your own comments. To do so, create files in the format {question-number}.txt and enter in the comments separated by a newline.

## TODO

* ~~Fix Blackboard csv file feature to easily upload grades~~
* ~~Add ability to save custom comments~~
* ~~Add student name checker~~
* ~~Parse student name text file from Blackboard instead of parsing the full grade center~~
* ~~Unzip student answers automatically~~
* ~~Write a script for copying grading key to key/answers~~
* ~~Import all files to main.py so the user only has to run `python main.py`~~
* ~~Fix "view grading status" bug when all files have been graded~~
* ~~Cut points automatically for late submissions~~
* ~~View anonymous animal names instead of student names when grading to avoid bias~~
* ~~Add ability to go back a submission when grading~~
* ~~Add ability to edit any students grade from the main menu~~
* ~~Create a document explaining what the requirements for making a question.rkt file should be to run this program successfully~~
* ~~Create a "Mistake analysis" feature in the main menu that would show how many students made a specific mistake and their names~~
* ~~Write more detailed documentation about how the program works and how to use the program with images~~
* ~~Adjust scores < 0 to 0~~
* ~~Add plagarism analyzing feature~~
* ~~Add Docker support~~
* ~~Added annonymous names toggle~~
* ~~Fix remove comment when no comments exist bug~~
* ~~Add search term feature to make it easier to grade~~
* ~~Add delete files option in main menu~~

### Refactor TO-DO
* Make more classes instead of a singleton
* Add more comments to code
* Use "pickle" library to store objects on disk instead of using json files to store data
* Create methods to save data as a json file if needed
* Add testing suite
* ~~Change ANSWERS variable name to SUBMISSIONS~~
* Print line numbers instead of question numbers for the submissions that aren't found
* Go back option instead of no comment in the add comment menu
* Modify key template to get total points and specific question points from the key
* Get total points and specific question points from the key
* Change "custom comment" button to "add new comment"
* Use some default characters in every menu e.g. "b" to go back or "e" to exit the program instead of integers
* In the search menu for grading, ask the user whether they want to display the output in red or green instead of asking them whether they want it in green or not.
* edit_grade function is not working properly. Fix.
* No "go back" option in delete menu. Add it.
* Add a feature to easily edit the penalty of existing comments added to the grade report. Editing a comment's penalty weight must retroactively change all previous graded students that were assigned that comment
* Add multiple comments at once by typing in multiple indexes.
* Run through submissions by alphabetical animal name order instead of alphabetical user id order
* Clearly state the "output.csv" has been saved to a file in the current directory when choosing the "Save repoort as .csv" option
* ~~Pass in command line arguments instead of renaming variables~~
* Make a list of known issues and work arounds
* Explicitly pass students.json in main file to getStudents.py
* Add comments inside key and read comments from there to preload some comments
* Write else case in unzip.py rename function
* Change implementation of getting question number to get the string between `Question ` and `:`


