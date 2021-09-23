"""
CS270 Autograder
Author: Zohair ul Hasan
Summer 2021

This program helps me grade racket files. To learn more about how to use the program,
visit the GitHub repository at https://github.com/Zohair-coder/CS270-grading-assistant/
"""

import os
import shutil
import sys
import json
import re
import csv
import random
import math
import pyinputplus as pyip
# used to get colored output. Read the docs here: https://pypi.org/project/colorama/
from colorama import Fore
import colorama
from tabulate import tabulate
import subprocess
import datetime
import argparse
import pickle
import getStudents
import unzip
import getKey
from key import Key
from submissions import Submissions
from roster import Roster
from gradebook import Gradebook


def main():
    colorama.init(autoreset=True)  # required for colored output

    submissions_dir = "submissions"
    answers_dir = "answers"
    grade_report_file = "grade_report.json"
    key_dir = "key"
    key_answers_dir = "answers"
    key_comments_dir = "comments"
    rkt_output_file = "rkt_output.txt"
    animals_txt_file = "animals.txt"
    useAnonymousNames = True

    # get the filenames for the user data files
    roster_file, grades_file, submissions_file, key_file = get_filenames()

    # Initialize Roster object containing basic information about every student
    roster = Roster(roster_file, animals_txt_file)

    # if submission files haven't been unzipped, unzip them
    if not os.path.isdir(submissions_dir):
        unzip.main(submissions_file, submissions_dir)

    # make sure pickles directory exists
    if not os.path.isdir("pickles"):
        os.mkdir("pickles")

    # REVISIT: See if key object needs to be pickled or not
    # if a key object hasn't already been saved, save it
    if not os.path.isfile("pickles/key.pkl"):
        key = Key(key_file)
        with open("pickles/key.pkl", "wb") as f:
            pickle.dump(key, f)
    else:
        with open("pickles/key.pkl", "rb") as f:
            key = pickle.load(f)

    # Initialize Submissions object that contains information about every students answer for every question
    submissions = Submissions(
        submissions_dir, answers_dir, key.get_all_questions())

    # if a gradebook object hasn't already been saved, save it
    if not os.path.isfile("pickles/gradebook.pkl"):
        gradebook = Gradebook(roster.get_all_ids(), key.get_all_questions())
        with open("pickles/gradebook.pkl", "wb") as f:
            pickle.dump(gradebook, f)
    else:
        with open("pickles/gradebook.pkl", "rb") as f:
            gradebook = pickle.load(f)
    # checker(grades_file, key_file)

    all_students = roster.get_all_ids()
    submitted_students = submissions.get_submitted_ids()
    unsubmitted_students = roster.get_unsubmitted_students(submitted_students)

    # prints the welcome screen, showing which students submitted and which didn't
    welcome_screen(roster, submitted_students)
    options()

    colorama.deinit()


class checker:
    def __init__(self, csv_file_name, key_file, submissions_directory="hw", student_data_file="students.json", main_dir_name="students", report_file="grade_report.json", save_file="save_file.json", key_dir="key", key_answers_dir="answers", key_comments_dir="comments", rkt_report_file="rkt_output.txt", animals_txt_file="animals.txt", id_to_animals_file="id_to_animals.json", useAnonymousNames=True):
        self.csv_file_name = csv_file_name
        self.key_file = key_file
        self.submissions_directory = submissions_directory
        self.student_data_file = student_data_file
        self.main_dir_name = main_dir_name
        self.report_file = report_file
        self.save_file = save_file
        self.key_dir = key_dir
        self.key_answers_dir = key_answers_dir
        self.key_comments_dir = key_comments_dir
        self.rkt_report_file = rkt_report_file
        self.animals_txt_file = animals_txt_file
        self.id_to_animals_file = id_to_animals_file
        self.useAnonymousNames = useAnonymousNames

        self.total_questions = self.get_total_questions()
        self.all_student_names = self.get_all_students()
        self.submitted_student_names = self.get_submitted_students()
        self.unsubmitted_student_names = self.get_unsubmitted_students()

        if self.useAnonymousNames:
            self.all_animal_names = self.get_all_animal_names()
            self.id_to_animals = self.create_id_to_animals_file()

        self.create_student_dirs()
        self.questions = [i for i in range(self.total_questions+1)]
        self.copy_student_answers()
        self.move_txt_files()
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
        files_in_directory = os.listdir(self.submissions_directory)
        filtered_files = [
            file for file in files_in_directory if file.endswith(".rkt")]
        for file in filtered_files:
            s.append(file.split(".")[0])
        return s

    def get_unsubmitted_students(self):
        return [student for student in self.all_student_names if student not in self.submitted_student_names]

    def get_all_animal_names(self):
        with open(self.animals_txt_file, "r") as f:
            animals_s = f.read()
        animals_list = animals_s.split("\n")
        return animals_list

    def create_id_to_animals_file(self):
        id_to_animals = dict()
        for student in self.all_student_names:
            random_num = random.randint(0, len(self.all_animal_names)-1)
            id_to_animals[student] = "Anonymous " + \
                self.all_animal_names[random_num]
        with open(self.id_to_animals_file, "w") as f:
            f.write(json.dumps(id_to_animals, indent=4))
        return id_to_animals

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
                submission_file = "{}/{}.rkt".format(
                    self.submissions_directory, student)
                answer = self.get_answer(question, submission_file)
                with open("{}/{}/{}.txt".format(self.main_dir_name, student, question), "w") as f:
                    f.write(answer)

    def get_answer(self, question, file):
        with open(file, "r") as f:
            rkt = f.read()

        search_string = r"; ?Question [\d, ]*{}.*?(\(define.*?)(^;end$)".format(
            question)
        match = re.search(search_string, rkt, re.DOTALL | re.MULTILINE)
        if match:
            return match.group(1)
        else:
            print(Fore.RED + "match not found for {}, question {}".format(file, question))
            shutil.rmtree("./students")
            sys.exit()

    def move_txt_files(self):
        files = os.listdir(self.submissions_directory)
        filtered_files = [
            file for file in files if file.endswith(".txt")]
        for file in filtered_files:
            student_name = file.split(".")[0]
            source = "{}/{}".format(self.submissions_directory, file)
            destination = "{}/{}/{}".format(
                self.main_dir_name, student_name, file)
            os.replace(source, destination)

    def run_all_rkt_files(self):
        for student in self.submitted_student_names:
            rkt_report_path = "{}/{}/{}".format(
                self.main_dir_name, student, self.rkt_report_file)
            if os.path.isfile(rkt_report_path):
                continue
            print(Fore.YELLOW + "Running {}.rkt... ".format(student), end='')
            process = subprocess.run(
                ["racket", "{}/{}.rkt".format(self.submissions_directory, student)], capture_output=True)
            output = process.stdout.decode("utf-8")
            print(Fore.GREEN + "Done")

            with open(rkt_report_path, "w") as f:
                f.write(output)

    def initialize_files(self):
        if not os.path.isfile(self.save_file):
            self.ungraded_questions = {}
            for question in self.questions[1:]:
                self.ungraded_questions[str(
                    question)] = self.submitted_student_names.copy()

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
            self.late_checked = False
        else:
            with open(self.save_file, "r") as f:
                self.ungraded_questions = json.load(f)

            with open(self.report_file, "r") as f:
                self.data = json.load(f)
            self.names_graded = True
            self.late_checked = True

        self.graded_questions = {}
        for question in self.questions[1:]:
            # if the whole question isn't in ungraded_questions
            if str(question) not in self.ungraded_questions.keys():
                self.graded_questions[str(
                    question)] = self.submitted_student_names.copy()
                continue

            for student in self.submitted_student_names:
                if student not in self.ungraded_questions[str(question)]:
                    if str(question) not in self.graded_questions:
                        self.graded_questions[str(question)] = []
                    self.graded_questions[str(question)].append(student)

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
        options = ["Start Grading", "Print Grade Report", "View Grading Status", "Edit grade manually", "Toggle anonymous names",
            "Save report as .csv for Blackboard", "Comment Analysis", "Plagarism Analysis", "Delete data", "Save and Exit"]

        choice = pyip.inputMenu(options, numbered=True)
        print()

        if choice == "Start Grading":
            self.grading()
            self.remove_negatives()
            print()
            print(Fore.GREEN + "Finished Grading!")
            print()
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

        elif choice == "Edit grade manually":
            self.edit_grade()
            self.options()

        elif choice == "Toggle anonymous names":
            self.useAnonymousNames = not self.useAnonymousNames
            if self.useAnonymousNames:
                print(Fore.GREEN + "Anonymous Names ON")
            else:
                print(Fore.RED + "Anonymous Names OFF")
            self.options()

        elif choice == "Save report as .csv for Blackboard":
            self.save_as_csv()
            print(Fore.GREEN + "Done!")
            self.options()

        elif choice == "Comment Analysis":
            self.comment_analysis()
            self.options()

        elif choice == "Plagarism Analysis":
            self.plagarism_analysis()
            self.options()

        elif choice == "Delete data":
            self.delete_data()
            self.options()

        elif choice == "Save and Exit":
            self.end_program()
        else:
            print(Fore.RED + "Oops - error :o")

    def grading(self):
        if not self.names_graded:
            self.auto_grade_names()
            self.names_graded = True

        if not self.late_checked:
            self.check_late()
            self.late_checked = True

        while len(self.ungraded_questions) != 0:
            int_ungraded_questions = [int(i) for i in self.ungraded_questions]
            self.current_question = min(int_ungraded_questions)
            self.current_question = str(self.current_question)
            self.search_terms = dict()

            while len(self.ungraded_questions[self.current_question]) != 0:
                student = self.ungraded_questions[self.current_question][0]
                self.clear_comments(student)
                with open("{}/{}/{}.txt".format(self.key_dir, self.key_answers_dir, self.current_question)) as f:
                    correct_answer = f.read()

                with open("{}/{}/{}.txt".format(self.main_dir_name, student, self.current_question)) as f:
                    student_answer = f.read()

                self.auto_feedback = self.auto_grader(student)

                if self.auto_feedback:
                    self.score = float(self.auto_feedback.group(2))
                else:
                    self.score = 0.0

                self.comments = []
                while True:
                    print(
                        Fore.CYAN + "======================================================")
                    print()
                    if self.useAnonymousNames:
                        print(Fore.CYAN +
                              "Grading {}".format(self.id_to_animals[student]))
                    else:
                        print(
                            Fore.CYAN + "Grading {}".format(self.all_student_names[student]))
                    total_submissions = len(self.submitted_student_names)
                    submissions_left = len(
                        self.ungraded_questions[self.current_question]) - 1
                    submission_num = total_submissions - submissions_left
                    print(Fore.CYAN + "Grading submission {}/{} for Question {}".format(
                        submission_num, total_submissions, self.current_question))
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
                        print(
                            Fore.RED + "Auto grader unable to check rkt file automatically")

                    search_results = self.get_search_results(student_answer)
                    for index, (search_term, found) in enumerate(search_results.items()):
                        if found[0]:
                            if found[1]:
                                print(
                                    Fore.GREEN + "Search #{}: {} FOUND".format(index, search_term.pattern))
                            else:
                                print(
                                    Fore.RED + "Search #{}: {} FOUND".format(index, search_term.pattern))
                        else:
                            if found[1]:
                                print(
                                    Fore.RED + "Search #{}: {} NOT FOUND".format(index, search_term.pattern))
                            else:
                                print(
                                    Fore.GREEN + "Search #{}: {} NOT FOUND".format(index, search_term.pattern))

                    if len(self.comments) > 0:
                        print(Fore.CYAN + "Comments Added:")
                        for comment in self.comments:
                            print(Fore.CYAN + comment)
                    print()

                    options = ["Add comment", "Remove comment", "Confirm score",
                        "Skip student", "Previous submission", "Search Menu"]
                    if self.useAnonymousNames:
                        options.append("Reveal real name")
                    options.append("Exit to main menu")

                    choice = pyip.inputMenu(options, numbered=True)
                    print()

                    if choice == "Add comment":
                        comment = self.add_comment()
                        if comment:
                            num = self.extract_score(comment)
                            if num is None:
                                continue
                            self.score += num
                            self.comments.append(comment)
                            self.save_comment(comment, student)

                    elif choice == "Remove comment":
                        if len(self.comments) == 0:
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
                        if self.current_question not in self.graded_questions.keys():
                            self.graded_questions[self.current_question] = []
                        self.graded_questions[self.current_question].append(
                            student)
                        self.remove_student(student)
                        print(Fore.YELLOW + "Autosaving..")
                        self.save_files()
                        print(Fore.GREEN + "Saved.")
                        print(Fore.CYAN + "Next student..")
                        break

                    elif choice == "Skip student":
                        first = student
                        self.remove_student(student)
                        self.ungraded_questions[self.current_question].append(
                            first)
                        break

                    elif choice == "Previous submission":
                        if self.current_question in self.graded_questions.keys():
                            if len(self.graded_questions[self.current_question]) == 0:
                                self.graded_questions.pop(
                                    self.current_question)

                        if not self.graded_questions:
                            print(Fore.RED + "Can not go further back!")
                            continue

                        int_graded_questions = [
                            int(i) for i in self.graded_questions.keys()]
                        self.current_question = str(max(int_graded_questions))
                        last_student = self.graded_questions[self.current_question].pop(
                        )
                        if self.current_question not in self.ungraded_questions.keys():
                            self.ungraded_questions[self.current_question] = []
                        self.ungraded_questions[self.current_question].insert(
                            0, last_student)
                        break

                    elif choice == "Search Menu":
                        self.search_menu()

                    elif choice == "Reveal real name":
                        print(Fore.YELLOW + self.all_student_names[student])

                    elif choice == "Exit to main menu":
                        print(Fore.CYAN + "Main Menu")
                        self.options()

                    else:
                        print(Fore.RED + "Oops - error :o")

            self.ungraded_questions.pop(self.current_question)

    def clear_comments(self, id):
        for grade in self.data:
            if grade["id"] == id:
                if not "comments" in grade:
                    return
                for comment in grade["comments"]:
                    if "#{}".format(self.current_question) in comment:
                        grade["comments"].remove(comment)

    def auto_grade_names(self):
        print(Fore.YELLOW + "Automatically grading student names...")
        for student in self.submitted_student_names:
            with open("{}/{}.rkt".format(self.submissions_directory, student), "r") as f:
                submission = f.read()
            search_string = ";type your name after the colon:\s*$"
            empty = re.search(search_string, submission, re.MULTILINE)
            if empty:
                print(Fore.RED + "{} did not enter name".format(student))
                comment = "#0: -5 no name"
                self.data.append({"id": student, "questions": {
                                 "0": -5}, "total_score": -5, "comments": [comment]})
                self.save_files()
            else:
                print(Fore.GREEN + "{} entered name".format(student))
        print(Fore.GREEN + "Done!")

    def check_late(self):
        late_students = dict()  # dictionary of late students
        with open(self.key_file, "r") as f:
            key = f.read()
        search_string = r"; put the due date here in MM\/DD\/YYYY HH:MM \(24hrs\) format after the colon:\s*(.*)$"
        match = re.search(search_string, key, re.MULTILINE)
        if match:
            due_date_s = match.group(1)
            due_date = datetime.datetime.strptime(due_date_s, "%m/%d/%Y %H:%M")
        else:
            print(Fore.RED + "Due date not found in key")
            os.remove(self.report_file)
            os.remove(self.save_file)
            sys.exit()

        for student in self.submitted_student_names:
            with open("{}/{}/{}.txt".format(self.main_dir_name, student, student), "r") as f:
                report = f.read()
            search_string = "Date Submitted: (.+) EDT"
            match = re.search(search_string, report, re.MULTILINE)
            if match:
                date_s = match.group(1)
                date = datetime.datetime.strptime(
                    date_s, "%A, %B %d, %Y %I:%M:%S %p")
            else:
                print(Fore.RED + "Date submitted not found for {}: ".format(student,
                      self.all_student_names[student]))
                continue

            delta = (due_date - date).total_seconds()
            if delta < 0:
                late_students[student] = {"delta": delta * -1, "pass": False}

        if len(late_students) == 0:
            return
        late_students = self.apply_late_pass(late_students)
        for student, info in late_students.items():
            penalty = info["penalty"] * -1
            if info["pass"]:
                comment = "#00: -{} late submission but late pass used".format(
                    penalty)
            else:
                comment = "#00: -{} late submission".format(penalty)
            found = False
            for data in self.data:
                if data["id"] == student:
                    found = True
                    if "questions" not in data:
                        data["questions"] = dict()
                    data["questions"]["00"] = penalty * -1
                    if "total_score" not in data:
                        data["total_score"] = 0
                    data["total_score"] -= penalty
                    if "comments" not in data:
                        data["comments"] = []
                    data["comments"].append(comment)
            if not found:
                self.data.append({"id": student, "questions": {
                                 "00": penalty * -1}, "total_score": penalty * -1, "comments": [comment]})

            self.save_files()

    def apply_late_pass(self, late_students):
        for student, info in late_students.items():
            days = math.ceil(info["delta"] / 60 / 60 / 24)
            print(
                Fore.RED + "{} {} Days LATE!".format(self.all_student_names[student], days))
            if days == 1:
                penalty = -20
            elif days == 2:
                penalty = -40
            elif days > 2:
                penalty = -60
            choice = pyip.inputYesNo(
                prompt=Fore.YELLOW + "Apply late pass? (yes/no): ")
            if choice == "yes":
                penalty += 20
                late_students[student]["pass"] = True
            late_students[student]["penalty"] = penalty
        return late_students

    def auto_grader(self, student):
        with open("{}/{}/{}".format(self.main_dir_name, student, self.rkt_report_file), "r") as f:
            output = f.read()
        search_string = "Q{}[A-Za-z.]* [Pp]assed (\d+)/(\d+)".format(
            self.current_question)
        match = re.search(search_string, output)
        if match:
            return match
        else:
            return None

    def get_search_results(self, answer):
        results = dict()
        for term, isGreen in self.search_terms.items():
            match = term.search(answer, re.DOTALL | re.MULTILINE)
            if match:
                results[term] = [True, isGreen]
            else:
                results[term] = [False, isGreen]
        return results

    def add_comment(self):
        comments_list = []
        file = "{}/{}/{}.txt".format(self.key_dir,
                                     self.key_comments_dir, self.current_question)
        if os.path.isfile(file):
            with open(file, "r") as f:
                for comment in f:
                    comment = comment.strip()
                    if comment:
                        comments_list.append(comment)

        comments_list.append("Custom comment")
        comments_list.append("No comment")

        while True:
            choice = pyip.inputMenu(comments_list, numbered=True)
            if choice == "Custom comment":
                while True:
                    comment = "#{}: -".format(self.current_question)
                    comment += pyip.inputStr(
                        "Enter custom comment: {}".format(comment))

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
        search_string = "#{}: (-?[\d.]+)".format(self.current_question)
        match = re.search(search_string, comment)
        if match:
            s = float(match.group(1))
            if s > 0:
                print(
                    Fore.RED + "Positive values not accepted. Please change comment to negative value")
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
        comment = pyip.inputMenu(self.comments, numbered=True,
                                 prompt="Select which comment to delete\n", blank=True)
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
            if self.score < 0:
                self.score = 0
            print(Fore.GREEN + "Score: {}/{}".format(self.score,
                  float(self.auto_feedback.group(2))))
            if input("Input blank to confirm: ") != "":
                return False

        found = False

        for grade in self.data:
            if grade['id'] == id:
                found = True
                if 'questions' not in grade:
                    grade['questions'] = dict()

                grade['questions'][self.current_question] = self.score
                total = 0
                for score in grade['questions'].values():
                    total += score

                grade['total_score'] = total

        if not found:
            self.data.append({"id": id, "questions": {
                             self.current_question: self.score}, "total_score": self.score})
        return True

    def remove_student(self, id):
        try:
            self.ungraded_questions[self.current_question].remove(id)
        except KeyError as e:
            print(e)
            raise

    def search_menu(self):
        choices = ["Add search term", "Remove search term"]
        choice = pyip.inputMenu(choices, numbered=True)
        if choice == "Add search term":
            term = pyip.inputRegexStr(prompt="Enter regex search term: ")
            new_choice = pyip.inputYesNo(
                prompt=Fore.YELLOW + "If found, display result in green? (yes/no): ")
            if new_choice == "yes":
                self.search_terms[term] = True
            elif new_choice == "no":
                self.search_terms[term] = False
        elif choice == "Remove search term":
            choices = self.search_terms.keys()
            choices = [choice.pattern for choice in choices]
            choice = pyip.inputMenu(choices, numbered=True, blank=True)
            if choice == "":
                choice = choices[0]
            self.search_terms.pop(re.compile(choice))

    def remove_negatives(self):
        for data in self.data:
            if data["total_score"] < 0:
                data["total_score"] = 0
        self.save_files()

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
        print(Fore.GREEN + "{}% completed".format(round(graded_questions /
              total_questions * 100, 1)))
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
                print(
                    Fore.RED + "Grade for {} not found. Skipping..".format(record[2]))
                continue
            if "total_score" not in student_grade:
                record[4] = pyip.inputInt(
                    prompt=Fore.YELLOW + "Total score for {} not found. Please enter score manually: ".format(record[2]))
            else:
                record[4] = student_grade["total_score"]

            comments = ""
            if "comments" in student_grade:
                for comment in student_grade["comments"]:
                    comments += "<p>" + comment + "</p>"
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

    def edit_grade(self):
        for id, student in self.all_student_names.items():
            print(Fore.CYAN + "{}: {}".format(student, id))
        print()
        print(Fore.YELLOW + "Enter -1 to go back to main menu")
        id = pyip.inputStr(prompt=Fore.YELLOW + "Enter student ID: ")
        if id == "-1":
            return
        grade = self.search_json("id", id)
        if grade is None:
            print(Fore.RED + "Student not found!")
            self.edit_grade()

        while True:
            print(Fore.YELLOW + json.dumps(grade, indent=4))
            choices = ["id", "questions", "total_score", "comments", "go back"]
            choice = pyip.inputMenu(choices, numbered=True)
            if choice == "id":
                self.edit_id(grade)
            elif choice == "questions":
                self.edit_questions(grade)
            elif choice == "total_score":
                self.edit_total_score(grade)
            elif choice == "comments":
                self.edit_comments(grade)
            elif choice == "go back":
                break
        self.edit_grade()

    def edit_id(self, grade):
        grade["id"] = pyip.inputStr(prompt=Fore.YELLOW + "Enter new ID: ")
        self.save_files()

    def edit_questions(self, grade):
        if "questions" not in grade:
            grade["questions"] = dict()
        questions = [key for key in grade["questions"].keys()]
        question = pyip.inputMenu(
            questions, prompt=Fore.YELLOW + "What question would you like to edit?\n")
        grade["questions"][question] = pyip.inputInt(
            prompt=Fore.YELLOW + "Enter marks for this question: ")
        self.save_files()

    def edit_total_score(self, grade):
        grade["total_score"] = pyip.inputInt(
            prompt=Fore.YELLOW + "Enter new total_score: ")
        self.save_files()

    def edit_comments(self, grade):
        if "comments" not in grade:
            grade["comments"] = []
        choices = ["Add new comment", "Remove existing comment"]
        choice = pyip.inputMenu(choices, numbered=True)
        if choice == "Add new comment":
            comment = pyip.inputStr(Fore.YELLOW + "Enter new comment: ")
            grade["comments"].append(comment)
            print(Fore.GREEN + "Comment added!")
            self.save_files()
        elif choice == "Remove existing comment":
            comment = pyip.inputMenu(
                grade["comments"], prompt=Fore.YELLOW + "What comment would you like to remove?\n", numbered=True)
            grade["comments"].remove(comment)
            print(Fore.GREEN + "Comment removed!")
            self.save_files()

    def comment_analysis(self):
        comment_freq = dict()
        comment_to_students = dict()
        for data in self.data:
            if "comments" in data:
                for comment in data["comments"]:
                    if comment not in comment_freq:
                        comment_freq[comment] = 0
                    comment_freq[comment] += 1

                    if comment not in comment_to_students:
                        comment_to_students[comment] = set()
                    if data["id"] not in comment_to_students[comment]:
                        comment_to_students[comment].add(
                            self.all_student_names[data["id"]])

        sorted_comment_freq = sorted(
            comment_freq.items(), key=lambda kv: kv[1])
        sorted_comment_freq.reverse()
        print(tabulate(sorted_comment_freq, headers=[
              "Comment", "Frequency"], showindex=True))
        print()
        while True:
            print(Fore.YELLOW + "Enter -2 to show comments analysis again")
            print(Fore.YELLOW + "Enter -1 to go back to main menu")
            choice = pyip.inputInt(
                Fore.YELLOW + "Select a comment to find out which students made the same mistake:\n")
            if choice == -2:
                print(tabulate(sorted_comment_freq, headers=[
                      "Comment", "Frequency"], showindex=True))
                print()
            elif choice == -1:
                return
            elif choice >= 0 and choice < len(sorted_comment_freq):
                comment = sorted_comment_freq[choice][0]

                for student in comment_to_students[comment]:
                    print(Fore.CYAN + student)
                print()
            else:
                print(Fore.RED + "Invalid choice. Try again!")

    def plagarism_analysis(self):
        matches = dict()
        for question in self.questions[1:]:
            print(Fore.YELLOW + "Checking Q{}".format(question))
            for first_student in self.submitted_student_names:
                for second_student in self.submitted_student_names:
                    if first_student != second_student:
                        with open("{}/{}/{}.txt".format(self.main_dir_name, first_student, question), "r") as f:
                            answer1 = f.read()
                        answer1 = self.remove_whitespace(answer1)
                        with open("{}/{}/{}.txt".format(self.main_dir_name, second_student, question), "r") as f:
                            answer2 = f.read()
                        answer2 = self.remove_whitespace(answer2)
                        if answer1 == answer2:
                            null_answer = r"(0|null|'\(\))\)?;ImplementMe"
                            match = re.search(null_answer, answer1)
                            if match:
                                continue
                            if answer1 in matches:
                                if question in matches[answer1]:
                                    matches[answer1][question].add(
                                        first_student)
                                    matches[answer1][question].add(
                                        second_student)
                                    continue

                            matches[answer1] = {question: {
                                first_student, second_student}}

        if len(matches) == 0:
            print(Fore.GREEN + "No matches found.")
            self.options()
        else:
            with open("plagarism.txt", "w") as f:
                for data in matches.values():
                    for question, students in data.items():
                        f.write("Q{}: {}\n".format(question, students))
            print(Fore.GREEN + "Written plagarism report in plagarism.txt")

    def delete_data(self):
        first_option = "Delete {} and {}".format(
            self.save_file, self.report_file)
        options = [first_option, "Delete ALL created data"]
        choice = pyip.inputMenu(options, numbered=True)
        if choice == first_option:
            choice = pyip.inputYesNo(
                prompt=Fore.RED + "Are you sure you want to delete {} and {}? (yes/no) ".format(self.save_file, self.report_file))
            if choice == "yes":
                to_delete = [self.save_file, self.report_file]
                for file in to_delete:
                    if os.path.isfile(file):
                        os.remove(file)
                    elif os.path.isdir(file):
                        shutil.rmtree(file)
                print(Fore.GREEN + "Done. Exiting...")
                sys.exit()
            elif choice == "no":
                return
        elif choice == "Delete ALL created data":
            choice = pyip.inputYesNo(
                prompt=Fore.RED + "Are you sure you want to delete ALL data? (yes/no) ")
            if choice == "yes":
                to_delete = [self.save_file, self.report_file, self.student_data_file,
                    self.id_to_animals_file, self.submissions_directory, self.key_dir, self.main_dir_name]
                for file in to_delete:
                    if os.path.isfile(file):
                        os.remove(file)
                    elif os.path.isdir(file):
                        shutil.rmtree(file)
                print(Fore.GREEN + "Done. Exiting...")
                sys.exit()
            elif choice == "no":
                return

    def end_program(self):
        self.save_files()
        print(Fore.GREEN + "Progress saved. Exiting program.")
        sys.exit()

    def remove_whitespace(self, s):
        s = s.replace(" ", "")
        s = s.replace("\n", "")
        s = s.replace("\t", "")
        return s

    def save_files(self):
        with open(self.save_file, "w") as f:
            f.write(json.dumps(self.ungraded_questions, indent=4))

        with open(self.report_file, "w") as f:
            f.write(json.dumps(self.data, indent=4))

# parses the arguments provided and returns the filenames in the order:
# roster_file, grades_file, submissions_file, key_file
# if no arguments are given, looks through config.json to search for the filenames
# if still no filenames are found, prints usage message and exits program


def get_filenames():
    is_imported = False
    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-r", "--roster", help="Enter the file name of the student roster csv file.")
        parser.add_argument(
            "-g", "--grades", help="Enter the file name of the student grades csv file.")
        parser.add_argument("-s", "--submissions",
                            help="Enter the file name of the student submissions zip file.")
        parser.add_argument(
            "-k", "--key", help="Enter the file name of the grading key rkt file.")
        args = parser.parse_args()
    else:
        is_imported = True

    if is_imported or not args.roster or not args.grades or not args.submissions or not args.key:
        if os.path.isfile("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                try:
                    roster_file = config["rosterFile"]
                    grades_file = config["gradesFile"]
                    submissions_file = config["submissionsFile"]
                    key_file = config["keyFile"]
                except KeyError as e:
                    raise Exception(
                        "Filenames not found in config.json. Enter command line arguments again.")
        else:
            if is_imported:
                print(Fore.RED + "Error: config.json not found")
                sys.exit(1)
            parser.print_help(sys.stderr)
            sys.exit(1)
    else:
        with open("config.json", "w") as f:
            config = dict()
            config["rosterFile"] = args.roster
            config["gradesFile"] = args.grades
            config["submissionsFile"] = args.submissions
            config["keyFile"] = args.key
            json.dump(config, f, indent=4)
        roster_file = args.roster
        grades_file = args.grades
        submissions_file = args.submissions
        key_file = args.key

    return roster_file, grades_file, submissions_file, key_file


# Prints a welcome message after starting the program
def welcome_screen(roster, submitted_students):
    all_students = roster.get_all_ids()
    unsubmitted_students = roster.get_unsubmitted_students(submitted_students)
    print(Fore.CYAN + "Welcome to the CS270 grading assistant")
    print()

    print(Fore.CYAN + "There are {} total students and {} submissions".format(
        len(all_students), len(submitted_students)))

    if len(unsubmitted_students) > 0:
        print(Fore.CYAN + "The following students did not send any submissions: ")

        for id in unsubmitted_students:
                print(Fore.CYAN + roster.get_name(id))

        print()


def options():
    options = ["Start Grading", "Print Grade Report", "View Grading Status", "Edit grade manually", "Toggle anonymous names",
        "Save report as .csv for Blackboard", "Comment Analysis", "Plagarism Analysis", "Delete data", "Save and Exit"]

    choice = pyip.inputMenu(options, numbered=True)
    print()

    if choice == "Start Grading":
        grading()
        remove_negatives()
        print()
        print(Fore.GREEN + "Finished Grading!")
        print()
        options()

    elif choice == "Print Grade Report":
        save_to_file = pyip.inputYesNo(prompt="Save to file? (yes/no): ")
        if save_to_file == "yes":
            save_to_file = True
        else:
            save_to_file = False
        print_report(save_to_file)
        options()

    elif choice == "View Grading Status":
        print_grading_status()
        options()

    elif choice == "Edit grade manually":
        edit_grade()
        options()

    elif choice == "Toggle anonymous names":
        useAnonymousNames = not useAnonymousNames
        if useAnonymousNames:
            print(Fore.GREEN + "Anonymous Names ON")
        else:
            print(Fore.RED + "Anonymous Names OFF")
        options()

    elif choice == "Save report as .csv for Blackboard":
        save_as_csv()
        print(Fore.GREEN + "Done!")
        options()

    elif choice == "Comment Analysis":
        comment_analysis()
        options()

    elif choice == "Plagarism Analysis":
        plagarism_analysis()
        options()

    elif choice == "Delete data":
        delete_data()
        options()

    elif choice == "Save and Exit":
        end_program()
    else:
        print(Fore.RED + "Oops - error :o")
    

def grading():
       if not gradebook.names_graded: # checks if names have been graded
            auto_grade_names()
            names_graded = True

        if not late_checked:
            check_late()
            late_checked = True

        while len(ungraded_questions) != 0:
            int_ungraded_questions = [int(i) for i in ungraded_questions]
            current_question = min(int_ungraded_questions)
            current_question = str(current_question)
            search_terms = dict()

            while len(ungraded_questions[current_question]) != 0:
                student = ungraded_questions[current_question][0]
                clear_comments(student)
                with open("{}/{}/{}.txt".format(key_dir, key_answers_dir, current_question)) as f:
                    correct_answer = f.read()

                with open("{}/{}/{}.txt".format(main_dir_name, student, current_question)) as f:
                    student_answer = f.read()

                auto_feedback = auto_grader(student)

                if auto_feedback:
                    score = float(auto_feedback.group(2))
                else:
                    score = 0.0

                comments = []
                while True:
                    print(
                        Fore.CYAN + "======================================================")
                    print()
                    if useAnonymousNames:
                        print(Fore.CYAN +
                              "Grading {}".format(id_to_animals[student]))
                    else:
                        print(
                            Fore.CYAN + "Grading {}".format(all_student_names[student]))
                    total_submissions = len(submitted_student_names)
                    submissions_left = len(
                        ungraded_questions[current_question]) - 1
                    submission_num = total_submissions - submissions_left
                    print(Fore.CYAN + "Grading submission {}/{} for Question {}".format(
                        submission_num, total_submissions, current_question))
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
                        print(
                            Fore.RED + "Auto grader unable to check rkt file automatically")

                    search_results = get_search_results(student_answer)
                    for index, (search_term, found) in enumerate(search_results.items()):
                        if found[0]:
                            if found[1]:
                                print(
                                    Fore.GREEN + "Search #{}: {} FOUND".format(index, search_term.pattern))
                            else:
                                print(
                                    Fore.RED + "Search #{}: {} FOUND".format(index, search_term.pattern))
                        else:
                            if found[1]:
                                print(
                                    Fore.RED + "Search #{}: {} NOT FOUND".format(index, search_term.pattern))
                            else:
                                print(
                                    Fore.GREEN + "Search #{}: {} NOT FOUND".format(index, search_term.pattern))

                    if len(comments) > 0:
                        print(Fore.CYAN + "Comments Added:")
                        for comment in comments:
                            print(Fore.CYAN + comment)
                    print()

                    options = ["Add comment", "Remove comment", "Confirm score",
                               "Skip student", "Previous submission", "Search Menu"]
                    if useAnonymousNames:
                        options.append("Reveal real name")
                    options.append("Exit to main menu")

                    choice = pyip.inputMenu(options, numbered=True)
                    print()

                    if choice == "Add comment":
                        comment = add_comment()
                        if comment:
                            num = extract_score(comment)
                            if num is None:
                                continue
                            score += num
                            comments.append(comment)
                            save_comment(comment, student)

                    elif choice == "Remove comment":
                        if len(comments) == 0:
                            print(Fore.RED + "No comments to remove")
                            continue
                        num = extract_score(comment)
                        score -= extract_score(comment)
                        comment = delete_comment(student)
                        comments.remove(comment)

                    elif choice == "Confirm score":
                        res = save_score(student)
                        if not res:
                            continue
                        if current_question not in graded_questions.keys():
                            graded_questions[current_question] = []
                        graded_questions[current_question].append(
                            student)
                        remove_student(student)
                        print(Fore.YELLOW + "Autosaving..")
                        save_files()
                        print(Fore.GREEN + "Saved.")
                        print(Fore.CYAN + "Next student..")
                        break

                    elif choice == "Skip student":
                        first = student
                        remove_student(student)
                        ungraded_questions[current_question].append(
                            first)
                        break

                    elif choice == "Previous submission":
                        if current_question in graded_questions.keys():
                            if len(graded_questions[current_question]) == 0:
                                graded_questions.pop(
                                    current_question)

                        if not graded_questions:
                            print(Fore.RED + "Can not go further back!")
                            continue

                        int_graded_questions = [
                            int(i) for i in graded_questions.keys()]
                        current_question = str(max(int_graded_questions))
                        last_student = graded_questions[current_question].pop(
                        )
                        if current_question not in ungraded_questions.keys():
                            ungraded_questions[current_question] = []
                        ungraded_questions[current_question].insert(
                            0, last_student)
                        break

                    elif choice == "Search Menu":
                        search_menu()

                    elif choice == "Reveal real name":
                        print(Fore.YELLOW + all_student_names[student])

                    elif choice == "Exit to main menu":
                        print(Fore.CYAN + "Main Menu")
                        options()

                    else:
                        print(Fore.RED + "Oops - error :o")

            ungraded_questions.pop(current_question)

if __name__ == "__main__":
    main()
