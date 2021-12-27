Blackboard has a feature where you can download a csv file that is basically a template for grading and then you can modify it by entering in the scores and comments of the students and then upload it again.

The template before grading looks like this:

<img width="1054" alt="Screen Shot 2021-12-27 at 8 35 15 AM" src="https://user-images.githubusercontent.com/52404521/147431794-ce68c2c2-e370-40fb-a9a8-0e370054a782.png">

The template after grading looks like this:

<img width="1053" alt="Screen Shot 2021-12-27 at 8 37 14 AM" src="https://user-images.githubusercontent.com/52404521/147431885-6da9f991-5df5-40a8-b76b-5d6e8fa52969.png">

The graded file can then be uploaded to Blackboard and all the student grades would automatically update. 

The CS270-grading-assistant has a feature to output a csv file that will be in the format of Blackboard's grading file template so that users can easily upload the file and not worry about manually entering each students score in the Blackboard grading center.

This feature is implemented in the `save_as_csv()` function in `main.py`. The function first reads the contents of the template file and stores it in a 2D-list. It then modifies the 2D array by looking up the grade and comments for every student in the JSON database and filling up those 2 columns. It then writes to an output csv file that the user can then upload.

However, the code relies on the fact that Blackboard would keep its grading template consistent over time and historically this has not been true so you may have to change it up a little. Blackboard uses column 8 for student grades as of right now, but in the future they may change this. Currently, the code for modifying column 8 looks like:

```
            if "total_score" not in student_grade:
                record[7] = pyip.inputInt( prompt= Fore.YELLOW + "Total score for {} not found. Please enter score manually: ".format(record[2]))
            else:
                record[7] = student_grade["total_score"]
```

As you might've guessed, if Blackboard changes its student grades column to `n`, you'll have to change the instances of `record[7]` to `record[n-1]`.

Similarly, this piece of code modifies the "comments" column (also known as Feedback to Learner):

```
comments = ""
            if "comments" in student_grade:
                for comment in student_grade["comments"]:
                    comments += "<p>" + comment + "</p>"
            record[10] = comments
```

As of right now, the 11th column is being used by Blackboard to write comments. In the future, you can change `records[10]` to `records[column_number_of_comments - 1]`. 
