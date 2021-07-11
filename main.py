import os
import json
import re
import pyinputplus as pyip

class checker:
    def __init__(self, total_questions, submissions_directory="hw", student_data_file="students.json", main_dir_name="students", report_file="grade_report.json", save_file="save_file.json"):
        self.total_questions = total_questions
        self.submissions_directory = submissions_directory
        self.student_data_file = student_data_file
        self.main_dir_name = main_dir_name
        self.report_file = report_file
        self.save_file = save_file



        self.all_student_names = self.get_all_students()
        self.submitted_student_names = self.get_submitted_students()
        self.unsubmitted_student_names = self.get_unsubmitted_students()
        self.create_student_dirs()
        self.questions = [i for i in range(1, total_questions+1)]
        self.copy_student_answers()
        self.initialize_files()
        
        self.welcome_screen()

        self.start_gui()





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
    
    def initialize_files(self):
        if not os.path.isfile(self.save_file):
            self.ungraded_questions = {}
            for question in self.questions:
                self.ungraded_questions[question] = self.submitted_student_names

            with open(self.save_file, "w") as f:
                f.write(json.dumps(self.ungraded_questions, indent=4))
            
            questions = {}
            for i in self.questions:
                questions[i] = 0
            self.data = [{"id": student, "questions": questions, "score": 0, "comments": [
                "Not submitted."]} for student in self.unsubmitted_student_names]

            with open(self.report_file, "w") as f:
                f.write(json.dumps(self.data, indent=4))
        else:
            with open(self.save_file, "r") as f:
                self.ungraded_questions = json.load(f)
            
            with open(self.report_file, "r") as f:
                self.data = json.load(f)

    def welcome_screen(self):
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
        
        print("You are currently working on question {}".format(min(self.ungraded_questions)))
        print()
        
        
        
    def start_gui(self):
        options = ["Start Grading", "Print Grade Report", "View Grading Status", "Save and Exit"]
        
        choice = pyip.inputMenu(options, numbered=True)
        print()
        
        if choice == "Start Grading":
            self.grading()
        
        elif choice == "Print Grade Report":
            self.print_report()
        
        elif choice == "View Grading Status":
            self.print_grading_status()
        
        elif choice == "Save and Exit":
            self.end_program()
    
    def grading(self):
        pass
                
        

    def print_report(self):
        pass

    def print_grading_status(self):
        pass

    def end_program(self):
        pass





if __name__ == "__main__":
    checker(15)
