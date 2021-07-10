import os
import json
import re
import pyinputplus as pyip

class checker:
    def __init__(self, total_questions, submissions_directory="hw", student_data_file="students.json", main_dir_name="students", report_file="grade_report.json"):
        self.total_questions = total_questions
        self.submissions_directory = submissions_directory
        self.student_data_file = student_data_file
        self.main_dir_name = main_dir_name
        self.report_file = report_file

        self.all_student_names = self.get_all_students()
        self.submitted_student_names = self.get_submitted_students()
        self.unsubmitted_student_names = self.get_unsubmitted_students()
        self.create_student_dirs()
        self.questions = [i for i in range(1, total_questions+1)]
        self.copy_student_answers()
        
        self.first_run = self.welcome_screen()





    def get_all_students(self):
        with open(self.student_data_file, "r") as jfile:
            students = json.load(jfile)
        return students
    
    def get_submitted_students(self):
        s = []
        for file in os.listdir(self.submissions_directory):
            s.append(file.split(".")[0])
        return s


    def get_unsubmitted_students(self):
        return [student for student in self.all_student_names if student not in self.submitted_student_names]
    
    def create_student_dirs(self):
        if not os.path.isdir(self.main_dir_name):
            os.mkdir(self.main_dir_name)

        for student in self.submitted_student_names:
            dir_name = "{}/{}".format(self.main_dir_name, student)
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)
    
    def copy_student_answers(self):
        for student in self.submitted_student_names:
            for question in self.questions:
                submission_file = "{}/{}.rkt".format(self.submissions_directory, student)
                answer = self.get_answer(question, submission_file)
                with open("{}/{}/{}.txt".format(self.main_dir_name, student, question), "w") as f:
                    f.write(answer)
    
    def get_answer(self, question, file):
        with open(file, "r") as f:
            rkt = f.read()

        search_string = r"; ?Question {}.*?(\(define.*?)(^\n|^[\t ]*$)".format(
            question)
        match = re.search(search_string, rkt, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1)
        else:
            print("match not found for {}, question {}".format(file, question))
            return "Check manually; not found via regex"
    
    def welcome_screen(self):
        if not os.path.isfile(self.report_file):  # if this program is being run for the first time
            first_run = True
            print("Welcome to the CS270 grading assistant")
            print()

            print("There are {} total students and {} submissions".format(
                len(self.all_student_names), len(self.submitted_student_names)))

            if len(self.unsubmitted_student_names) > 0:
                print("The following students did not send any submissions: ")

                names = []
                for student in self.unsubmitted_student_names:
                    names.append(self.all_student_names[student])
                print(*names, sep=", ")

                print()

            choice = pyip.inputYesNo(
                prompt="Generate grade report file? (yes/no): ")
            if choice == "yes":

                data = [{"id": student, "score": 0, "comments": [
                    "Not submitted."]} for student in self.unsubmitted_student_names]

                if not data:
                    data = [{}]

                with open(self.report_file, "w") as f:
                    f.write(json.dumps(data, indent=4))

        else:
            first_run = False
            print("Welcome back!")
        
        return first_run


if __name__ == "__main__":
    checker(15)
