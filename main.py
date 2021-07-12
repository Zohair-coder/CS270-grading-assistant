import os
import sys
import json
import re
import pyinputplus as pyip
from colorama import Fore
import colorama
import subprocess

class checker:
    def __init__(self, total_questions, submissions_directory="hw", student_data_file="students.json", main_dir_name="students", report_file="grade_report.json", save_file="save_file.json", key_dir="key", key_answers_dir="answers", key_comments_dir="comments"):
        self.total_questions = total_questions
        self.submissions_directory = submissions_directory
        self.student_data_file = student_data_file
        self.main_dir_name = main_dir_name
        self.report_file = report_file
        self.save_file = save_file
        self.key_dir = key_dir
        self.key_answers_dir = key_answers_dir
        self.key_comments_dir = key_comments_dir



        self.all_student_names = self.get_all_students()
        self.submitted_student_names = self.get_submitted_students()
        self.unsubmitted_student_names = self.get_unsubmitted_students()
        self.create_student_dirs()
        self.questions = [i for i in range(1, total_questions+1)]
        self.copy_student_answers()
        self.initialize_files()
        
        self.welcome_screen()

        self.options()





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
            self.data = [{"id": student, "questions": questions, "total_score": 0, "comments": [
                "Not submitted."]} for student in self.unsubmitted_student_names]

            with open(self.report_file, "w") as f:
                f.write(json.dumps(self.data, indent=4))
        else:
            with open(self.save_file, "r") as f:
                self.ungraded_questions = json.load(f)
            
            with open(self.report_file, "r") as f:
                self.data = json.load(f)

    def welcome_screen(self):
        print(Fore.CYAN + "Welcome to the CS270 grading assistant")
        print()

        print(Fore.CYAN + "There are {} total students and {} submissions".format(
            len(self.all_student_names), len(self.submitted_student_names)))

        if len(self.unsubmitted_student_names) > 0:
            print(Fore.CYAN + "The following students did not send any submissions: ")

            for student in self.unsubmitted_student_names:
                print(Fore.CYAN + self.all_student_names[student])


            print()
        
        int_ungraded_questions = [int(i) for i in self.ungraded_questions]
        if len(int_ungraded_questions) == 0:
            print(Fore.GREEN + "Completed Grading!")
            return
        print(Fore.CYAN + "You are currently working on question {}".format(min(int_ungraded_questions)))
        print()
        
        
        
    def options(self):
        options = ["Start Grading", "Print Grade Report", "View Grading Status", "Save and Exit"]
        
        choice = pyip.inputMenu(options, numbered=True)
        print()
        
        if choice == "Start Grading":
            self.grading()
            print(Fore.GREEN + "Finished Grading!")
        
        elif choice == "Print Grade Report":
            self.print_report()
            self.options()
        
        elif choice == "View Grading Status":
            self.print_grading_status()
            self.options()

        elif choice == "Save and Exit":
            self.end_program()
        else:
            print(Fore.RED + "Oops - error :o")
    
    def grading(self):
        while len(self.ungraded_questions) != 0:
            int_ungraded_questions = [int(i) for i in self.ungraded_questions]
            current_question = min(int_ungraded_questions)
            current_question = str(current_question)

            while len(self.ungraded_questions[current_question]) != 0:
                student = self.ungraded_questions[current_question][0]
                with open("{}/{}/{}.txt".format(self.key_dir, self.key_answers_dir, current_question)) as f:
                    correct_answer = f.read()
                
                with open("{}/{}/{}.txt".format(self.main_dir_name, student, current_question)) as f:
                    student_answer = f.read()

                auto_feedback = self.auto_grader(student, current_question)

                comments = []
                while True:
                    print(Fore.CYAN + "======================================================")
                    print()
                    print(Fore.CYAN +
                            "Grading {}".format(self.all_student_names[student]))
                    print(
                        Fore.CYAN + "Currently grading Question {}".format(current_question))
                    print()
                    print(Fore.CYAN + "Correct Answer:")
                    print()
                    print(Fore.YELLOW + correct_answer)
                    print()
                    print(Fore.CYAN + "Student Answer:")
                    print()
                    print(Fore.YELLOW + student_answer)
                    print()

                    if auto_feedback:
                        if auto_feedback.group(1) == auto_feedback.group(2):
                            print(Fore.GREEN + auto_feedback.group())
                        else:
                            print(Fore.RED + auto_feedback.group())
                    else:
                        print(Fore.RED + "Auto grader unable to check rkt file automatically")

                    if len(comments) > 0:
                        print(Fore.CYAN + "Comments Added:")
                        for comment in comments:
                            print(Fore.CYAN + comment)
                    print()


                    options = ["Add comment", "Remove comment", "Enter score", "Skip student", "Exit to main menu"]
                    choice = pyip.inputMenu(options, numbered=True)
                    print()

                    if choice == "Add comment":
                        comment = self.add_comment(current_question)
                        if comment:
                            comments.append(comment)
                            self.save_comment(comment, student)

                    elif choice == "Remove comment":
                        if not comment:
                            print(Fore.RED + "No comments to remove")
                            continue
                        comment = self.delete_comment(comments, student)
                        if comment:
                            comments.remove(comment)

                    elif choice == "Enter score":
                        res = self.save_score(current_question, student)
                        if not res:
                            continue
                        self.remove_student(current_question, student)
                        print(Fore.YELLOW + "Autosaving..")
                        self.save_files()
                        print(Fore.GREEN + "Saved.")
                        print(Fore.CYAN + "Next student..")
                        break

                    elif choice == "Skip student":
                        first = student
                        self.remove_student(current_question, student)
                        self.ungraded_questions[current_question].append(first)
                        break

                    elif choice == "Exit to main menu":
                        print(Fore.CYAN + "Main Menu")
                        self.options()

                    else:
                        print(Fore.RED + "Oops - error :o")

            self.ungraded_questions.pop(current_question)
    
    def auto_grader(self, student, quesiton):
        process = subprocess.run(["Racket.exe", "{}/{}.rkt".format(self.submissions_directory, student)], capture_output=True)
        output = process.stdout.decode("utf-8")
        search_string = "Q{} passed (\d+)/(\d+)".format(quesiton)
        match = re.search(search_string, output)
        if match:
            return match
        else:
            return None


    def add_comment(self, question):
        with open("{}/{}/{}.txt".format(self.key_dir, self.key_comments_dir, question)) as f:
            comments = f.read()
        comments_list = comments.split("\n")
        comments_list.append("Custom comment")
        comments_list.append("No comment")

        choice = pyip.inputMenu(comments_list, numbered=True)
        if choice == "Custom comment":
            comment = pyip.inputStr("Enter custom comment: ")
        elif choice == "No comment":
            return None
        else:
            comment = choice
        
        return comment
    
    def save_comment(self, comment, id):
        found = False
        for grade in self.data:
            if grade['id'] == id:
                found = True
                if not 'comments' in grade:
                    grade['comments'] = []
                grade['comments'].append(comment)
        
        if not found:
            self.data.append({"id": id, "comments": [comment]})
    
    def delete_comment(self, comments, id):
        if comments == []:
            print(Fore.RED + "No comments to delete!")
            return None

        comment = pyip.inputMenu(comments, numbered=True, prompt="Select which comment to delete\n", blank=True)
        if comment == "":
            comment = comments[0]

        for grade in self.data:
            if grade['id'] == id:
                if ('comments' in grade) and (comment in grade['comments']):
                    grade['comments'].remove(comment)
                    return comment

        

    def save_score(self, question, id):
        score = pyip.inputInt(prompt="Score: ")

        if score == -1:
            return False

        found = False
        
        for grade in self.data:
            if grade['id'] == id:
                found = True
                if 'questions' not in grade:
                    grade['questions'] = dict()

                grade['questions'][question] = score 
                
                if 'total_score' in grade:
                    grade['total_score'] += score
                else:
                    grade['total_score'] = score

        if not found:
            self.data.append({"id": id, "questions": {question: score}, "total_score": score})
        return True
    
    def remove_student(self, q, id):
        for question, students in self.ungraded_questions.items():
            if question == q:
                students.remove(id)
                return
        raise Exception("Trying to remove student that isn't in self.ungraded_questions")
    


    def print_report(self):
        for grade in self.data:
            print(Fore.GREEN + self.all_student_names[grade['id']])
            print()
            for question, score in grade['questions'].items():
                print(Fore.CYAN + "Question {}: {}".format(question, score))
            print()
            print(Fore.CYAN + "Total Score: {}".format(grade['total_score']))
            print()
            if 'comments' in grade:
                print(Fore.CYAN + "Comments:")
                for comment in grade['comments']:
                    print(Fore.CYAN + comment)
            else:
                print(Fore.CYAN + "No comments")

            print()

            print("==================================")

    def print_grading_status(self):
        int_ungraded_questions = [int(i) for i in self.ungraded_questions]
        current_question = min(int_ungraded_questions)
        total_questions = self.total_questions * len(self.all_student_names)
        remaining_questions = 0
        
        for students in self.ungraded_questions.values():
            remaining_questions += len(students)

        graded_questions = total_questions - remaining_questions

        print(Fore.YELLOW + "Currently grading question {}".format(current_question))
        print(Fore.YELLOW + "Graded {} questions".format(graded_questions))
        print(Fore.YELLOW + "{} questions remaining".format(remaining_questions))
        print()
        print(Fore.GREEN + "{}% completed".format(round(graded_questions/total_questions * 100, 1)))
        print()

    def end_program(self):
        self.save_files()
        print(Fore.GREEN + "Progress saved. Exiting program.")
        sys.exit()


    def save_files(self):
        with open(self.save_file, "w") as f:
            f.write(json.dumps(self.ungraded_questions, indent=4))
    
        with open(self.report_file, "w") as f:
            f.write(json.dumps(self.data, indent=4))

if __name__ == "__main__":
    colorama.init(autoreset=True)
    checker(15)
    colorama.deinit()
