import os
import sys
import json
import re
import csv
import pyinputplus as pyip
from colorama import Fore
import colorama
import subprocess
import getStudents
import rename

STUDENT_NAMES_CSV = "gc_41672.202045_fullgc_2021-07-16-11-33-22.csv"
GRADES_CSV = "gc_41672.202045_column_2021-07-16-07-55-59.csv"

def main():
    getStudents.main(STUDENT_NAMES_CSV)
    rename.main()
    colorama.init(autoreset=True)
    checker(GRADES_CSV)
    colorama.deinit()

class checker:
    def __init__(self, csv_file_name, submissions_directory="hw", student_data_file="students.json", main_dir_name="students", report_file="grade_report.json", save_file="save_file.json", key_dir="key", key_answers_dir="answers", key_comments_dir="comments", rkt_report_file="rkt_output.txt"):
        self.csv_file_name = csv_file_name
        self.submissions_directory = submissions_directory
        self.student_data_file = student_data_file
        self.main_dir_name = main_dir_name
        self.report_file = report_file
        self.save_file = save_file
        self.key_dir = key_dir
        self.key_answers_dir = key_answers_dir
        self.key_comments_dir = key_comments_dir
        self.rkt_report_file = rkt_report_file

        self.total_questions = self.get_total_questions()
        self.all_student_names = self.get_all_students()
        self.submitted_student_names = self.get_submitted_students()
        self.unsubmitted_student_names = self.get_unsubmitted_students()
        self.create_student_dirs()
        self.questions = [i for i in range(self.total_questions+1)]
        self.copy_student_answers()
        self.run_all_rkt_files()
        self.initialize_files()
        
        self.welcome_screen()

        self.options()



    def get_total_questions(self):
        return len(os.listdir("{}/{}".format(self.key_dir, self.key_answers_dir)))

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
            for question in self.questions[1:]:
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


    def run_all_rkt_files(self):
        for student in self.submitted_student_names:
            rkt_report_path = "{}/{}/{}".format(self.main_dir_name, student, self.rkt_report_file)
            if os.path.isfile(rkt_report_path):
                continue
            print(Fore.YELLOW + "Running {}.rkt... ".format(student), end='')
            process = subprocess.run(["Racket.exe", "{}/{}.rkt".format(self.submissions_directory, student)], capture_output=True)
            output = process.stdout.decode("utf-8")
            print(Fore.GREEN + "Done")

            with open(rkt_report_path, "w") as f:
                f.write(output)


    def initialize_files(self):
        if not os.path.isfile(self.save_file):
            self.ungraded_questions = {}
            for question in self.questions[1:]:
                self.ungraded_questions[str(question)] = self.submitted_student_names.copy()

            with open(self.save_file, "w") as f:
                f.write(json.dumps(self.ungraded_questions, indent=4))
            
            questions = {}
            for i in self.questions:
                questions[i] = 0
            self.data = [{"id": student, "questions": questions, "total_score": 0, "comments": [
                "Not submitted."]} for student in self.unsubmitted_student_names]

            with open(self.report_file, "w") as f:
                f.write(json.dumps(self.data, indent=4))
            
            self.names_graded = False
        else:
            with open(self.save_file, "r") as f:
                self.ungraded_questions = json.load(f)
            
            with open(self.report_file, "r") as f:
                self.data = json.load(f)
            self.names_graded = True

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
        options = ["Start Grading", "Print Grade Report", "View Grading Status", "Save report as .csv for Blackboard","Save and Exit"]
        
        choice = pyip.inputMenu(options, numbered=True)
        print()
        
        if choice == "Start Grading":
            self.grading()
            print(Fore.GREEN + "Finished Grading!")
            self.options()
        
        elif choice == "Print Grade Report":
            save_to_file = pyip.inputYesNo(prompt="Save to file? (yes/no): ")
            if save_to_file == "yes":
                save_to_file = True
            else:
                save_to_file = False
            self.print_report(save_to_file)
            self.options()
        
        elif choice == "View Grading Status":
            self.print_grading_status()
            self.options()
        
        elif choice == "Save report as .csv for Blackboard":
            self.save_as_csv()
            print(Fore.GREEN + "Done!")
            self.options()

        elif choice == "Save and Exit":
            self.end_program()
        else:
            print(Fore.RED + "Oops - error :o")
    
    def grading(self):
        if not self.names_graded:
            self.auto_grade_names()
            self.names_graded = True

        while len(self.ungraded_questions) != 0:
            int_ungraded_questions = [int(i) for i in self.ungraded_questions]
            self.current_question = min(int_ungraded_questions)
            self.current_question = str(self.current_question)

            while len(self.ungraded_questions[self.current_question]) != 0:
                student = self.ungraded_questions[self.current_question][0]
                with open("{}/{}/{}.txt".format(self.key_dir, self.key_answers_dir, self.current_question)) as f:
                    correct_answer = f.read()
                
                with open("{}/{}/{}.txt".format(self.main_dir_name, student, self.current_question)) as f:
                    student_answer = f.read()

                self.auto_feedback = self.auto_grader(student)

                if self.auto_feedback:
                    self.score = int(self.auto_feedback.group(2))

                self.comments = []
                while True:
                    print(Fore.CYAN + "======================================================")
                    print()
                    print(Fore.CYAN +
                            "Grading {}".format(self.all_student_names[student]))
                    print(
                        Fore.CYAN + "Currently grading Question {}".format(self.current_question))
                    print()
                    print(Fore.CYAN + "Correct Answer:")
                    print()
                    print(Fore.YELLOW + correct_answer)
                    print()
                    print(Fore.CYAN + "Student Answer:")
                    print()
                    print(Fore.YELLOW + student_answer)
                    print()

                    if self.auto_feedback:
                        if self.auto_feedback.group(1) == self.auto_feedback.group(2):
                            print(Fore.GREEN + self.auto_feedback.group())
                        else:
                            print(Fore.RED + self.auto_feedback.group())
                    else:
                        print(Fore.RED + "Auto grader unable to check rkt file automatically")

                    if len(self.comments) > 0:
                        print(Fore.CYAN + "Comments Added:")
                        for comment in self.comments:
                            print(Fore.CYAN + comment)
                    print()


                    options = ["Add comment", "Remove comment", "Confirm score", "Skip student", "Exit to main menu"]
                    choice = pyip.inputMenu(options, numbered=True)
                    print()

                    if choice == "Add comment":
                        comment = self.add_comment()
                        if comment:
                            num = self.extract_score(comment)
                            if not num:
                                continue
                            self.score += num
                            self.comments.append(comment)
                            self.save_comment(comment, student)

                    elif choice == "Remove comment":
                        if not comment:
                            print(Fore.RED + "No comments to remove")
                            continue
                        num = self.extract_score(comment)
                        self.score -= self.extract_score(comment)
                        comment = self.delete_comment(student)
                        self.comments.remove(comment)

                    elif choice == "Confirm score":
                        res = self.save_score(student)
                        if not res:
                            continue
                        self.remove_student(student)
                        print(Fore.YELLOW + "Autosaving..")
                        self.save_files()
                        print(Fore.GREEN + "Saved.")
                        print(Fore.CYAN + "Next student..")
                        break

                    elif choice == "Skip student":
                        first = student
                        self.remove_student(student)
                        self.ungraded_questions[self.current_question].append(first)
                        break

                    elif choice == "Exit to main menu":
                        print(Fore.CYAN + "Main Menu")
                        self.options()

                    else:
                        print(Fore.RED + "Oops - error :o")

            self.ungraded_questions.pop(self.current_question)
    
    def auto_grade_names(self):
        print(Fore.YELLOW + "Automatically grading student names...")
        for student in self.submitted_student_names:
            with open("{}/{}.rkt".format(self.submissions_directory, student), "r") as f:
                submission = f.read()
            search_string = ";type your name after the colon: ?[\w -]+$"
            match = re.search(search_string, submission, re.MULTILINE)
            if not match:
                print(Fore.RED + "{} did not enter name".format(student))
                comment = "#0: -5 no name"
                # self.save_comment(comment, student)
                # grade = self.search_json("id", student)
                # grade.append()
                self.data.append({"id": student, "questions": {"0": -5}, "total_score": -5, "comments": [comment]})
                self.save_files()
            else:
                print(Fore.GREEN + "{} entered name".format(student))
        print(Fore.GREEN + "Done!")

    def auto_grader(self, student):
        with open("{}/{}/{}".format(self.main_dir_name, student, self.rkt_report_file), "r") as f:
            output = f.read()
        search_string = "Q{} passed (\d+)/(\d+)".format(self.current_question)
        match = re.search(search_string, output)
        if match:
            return match
        else:
            return None


    def add_comment(self):
        with open("{}/{}/{}.txt".format(self.key_dir, self.key_comments_dir, self.current_question)) as f:
            comments = f.read()
        comments_list = comments.split("\n")
        comments_list.append("Custom comment")
        comments_list.append("No comment")

        while True:
            choice = pyip.inputMenu(comments_list, numbered=True)
            if choice == "Custom comment":
                while True:
                    comment = "#{}: -".format(self.current_question)
                    comment += pyip.inputStr("Enter custom comment: {}".format(comment))
                    
                    search_string = "#{}: -\d+".format(self.current_question)
                    match = re.search(search_string, comment)
                    if match:
                        break
                    print(Fore.RED + "Comment must be in the format:")
                    print(Fore.YELLOW + "\t#1: -1 this is a sample comment")
                with open("{}/{}/{}.txt".format(self.key_dir, self.key_comments_dir, self.current_question), "a") as f:
                    f.write("\n" + comment)
            elif choice == "No comment":
                return None
            else:
                comment = choice

            if comment in self.comments:
                print(Fore.RED + "The same comment can't be added twice. Try again.")
                continue
            else:
                break
        
        return comment

    def extract_score(self, comment):
        search_string = "#{}: (-?\d+)".format(self.current_question)
        match = re.search(search_string, comment)
        if match:
            s = int(match.group(1))
            if s >= 0:
                print(Fore.RED + "Positive values not accepted. Please change comment to negative value")
                return None
        else:
            print(Fore.RED + "Unable to extract score from comments")
            print(Fore.YELLOW + "Make sure comment follows the syntax:\n\t#1: -1 use (zero? a) instead of (equal? a 0)")
            sys.exit()
        return s

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
    
    def delete_comment(self, id):
        comment = pyip.inputMenu(self.comments, numbered=True, prompt="Select which comment to delete\n", blank=True)
        if comment == "":
            comment = self.comments[0]

        for grade in self.data:
            if grade['id'] == id:
                if ('comments' in grade) and (comment in grade['comments']):
                    grade['comments'].remove(comment)
                    return comment

        

    def save_score(self, id):
        if not self.auto_feedback:
            self.score = pyip.inputInt(prompt="Score: ")
        else:
            print(Fore.GREEN + "Score: {}/{}".format(self.score, self.auto_feedback.group(2)))
            if input("Input blank to confirm: ") != "":
                return False

        found = False
        
        for grade in self.data:
            if grade['id'] == id:
                found = True
                if 'questions' not in grade:
                    grade['questions'] = dict()

                grade['questions'][self.current_question] = self.score 
                
                if 'total_score' in grade:
                    grade['total_score'] += self.score
                else:
                    grade['total_score'] = self.score

        if not found:
            self.data.append({"id": id, "questions": {self.current_question: self.score}, "total_score": self.score})
        return True
    
    def remove_student(self, id):
        try:
            self.ungraded_questions[self.current_question].remove(id)
        except KeyError as e:
            print(e)
            raise
    


    def print_report(self, save):
        report = ""
        for grade in self.data:
            report += (self.all_student_names[grade['id']]) + "\n"
            report += "\n"
            for question, score in grade['questions'].items():
                report += ("Question {}: {}".format(question, score)) + "\n"
            report += "\n"
            report += ("Total Score: {}".format(grade['total_score'])) + "\n"
            report += "\n"
            if 'comments' in grade:
                report += ("Comments:") + "\n"
                for comment in grade['comments']:
                    report += (comment) + "\n"
            else:
                report += ("No comments") + "\n"

            report += "\n"

            report += ("==================================") + "\n"
        
        if save:
            with open("hr_grade_report.txt", "w") as f:
                f.write(report)
        else:
            print(report)

    def print_grading_status(self):
        int_ungraded_questions = [int(i) for i in self.ungraded_questions]
        self.current_question = 0
        if len(int_ungraded_questions) != 0:
            self.current_question = min(int_ungraded_questions)
        total_questions = self.total_questions * len(self.all_student_names)
        remaining_questions = 0
        
        for students in self.ungraded_questions.values():
            remaining_questions += len(students)

        graded_questions = total_questions - remaining_questions

        print(Fore.YELLOW + "Currently grading question {}".format(self.current_question))
        print(Fore.YELLOW + "Graded {} questions".format(graded_questions))
        print(Fore.YELLOW + "{} questions remaining".format(remaining_questions))
        print()
        print(Fore.GREEN + "{}% completed".format(round(graded_questions/total_questions * 100, 1)))
        print()

    def save_as_csv(self):
        file = self.csv_file_name

        csv_data = []
        with open(file, "r", encoding="utf-8-sig") as f:
            csvFile = csv.reader(f)
            header = next(csvFile)
            for lines in csvFile:
                csv_data.append(lines)
        
        for record in csv_data:
            student_grade = self.search_json("id", record[2])
            if not student_grade:
                print(Fore.RED + "Grade for {} not found. Skipping..".format(record[2]))
                continue
            if "total_score" not in student_grade:
                record[4] = pyip.inputInt( prompt= Fore.YELLOW + "Total score for {} not found. Please enter score manually: ".format(record[2]))
            else:
                record[4] = student_grade["total_score"]

            comments = ""
            if "comments" in student_grade:
                for comment in student_grade["comments"]:
                    comments += "<p>" + comment + "<\p>\n"
            record[7] = comments
        
        with open("output.csv", "w", newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            csvwriter.writerows(csv_data)
        
    def search_json(self, field, search):
        for student in self.data:
            if student[field] == search:
                return student
        return None

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
    main()
