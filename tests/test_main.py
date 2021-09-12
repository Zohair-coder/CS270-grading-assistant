"""
Unit tests for CS270 Autograder main.py
Make sure that config.json is created and the rosterFile, gradesFile, submissionsFile and keyFile fields are set.
Copy all the files in the tests directory to the parent directory before running the tests.
"""

import unittest
from unittest import IsolatedAsyncioTestCase
import shutil
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import main
import getStudents
import unzip
from key import Key

# delete code generated files before testing
if os.path.isdir("hw"):
    shutil.rmtree("hw")
if os.path.isdir("key"):
    shutil.rmtree("key")
if os.path.isdir("students"):
    shutil.rmtree("students")
if os.path.isfile("grade_report.json"):
    os.remove("grade_report.json")
if os.path.isfile("id_to_animals.json"):
    os.remove("id_to_animals.json")
if os.path.isfile("plagarism.txt"):
    os.remove("plagarism.txt")
if os.path.isfile("save_file.json"):
    os.remove("save_file.json")
if os.path.isfile("students.json"):
    os.remove("students.json")

test_files = {
    "roster": "gc_41672.202045_fullgc_2021-07-22-17-11-55.csv",
    "grades": "gc_41672.202045_column_2021-07-29-11-56-58.csv",
    "submissions": "gradebook_41672.202045_HW5.Su21_2021-08-06-15-08-15.zip",
    "key": "hw5k (1).rkt"
}

class TestFilenames(unittest.TestCase):
    def test_roster_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertEqual(roster_file, test_files["roster"])

    def test_grades_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertEqual(grades_file, test_files["grades"])

    def test_submissions_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertEqual(submissions_file, test_files["submissions"])

    def test_key_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertEqual(key_file, test_files["key"])


class TestGetStudents(unittest.TestCase):
    def test_main(self):
        result = getStudents.main(
            test_files["roster"])
        self.assertEqual(result, {
            "ha594": "Hasan Almemari",
            "sya33": "Sanam Amin",
            "aa4246": "Atandrila Anuva",
            "aia43": "Alisha Augustin",
            "sa3655": "Sarthak Awasthi",
            "sb4249": "Sara Beinish",
            "dc3339": "Dawood Chaudhry",
            "blc83": "Brandon Crespo",
            "rac364": "Reed Curtis",
            "acd328": "Anthony Dargis",
            "jd3696": "John Dominguez",
            "oae24": "Oroghene Emudainohwo",
            "mjf394": "Mark Fazzolari",
            "rbg63": "Raj Giddi",
            "sg3596": "Sahil Gill",
            "jg3782": "Jaehyun Go",
            "ajh395": "Andrew Hagelthorn",
            "mh3638": "Max Hajduk",
            "ah3548": "Ariel Halpert",
            "ah3589": "Arjun Hawkins",
            "mlh396": "Mark Helminiak",
            "sh3425": "Steven Huang",
            "lfi23": "Luke Ingram",
            "acj58": "Drew Jenkins",
            "tfj33": "Thomas Jordan",
            "al3373": "Anthony Lam",
            "dql28": "Jason Le",
            "nl466": "Nick Lindsay-Abaire",
            "cl3454": "Carlos Luna Sangama",
            "asm437": "Akhil Mohammed",
            "dhn38": "Duong Nguyen",
            "rhn26": "Raymond Nguyen",
            "vp453": "Vistrit Pandey",
            "jmp586": "Jonathan Parlett",
            "jvr38": "Joe Rajasekaran",
            "as5429": "Aneesh Sahu",
            "as5268": "Alfred Saintclair",
            "kts59": "Kayla Savage",
            "rhs58": "Robert Scales",
            "ns3335": "Nikhil Solanki",
            "ngs33": "Nate Stutte",
            "jfs325": "Jack Svetec",
            "ayw32": "Alexander Wang"
        })


class TestUnzip(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unzip.main(test_files["submissions"])

    def test_rkt_files_same_as_student_ids(self):
        result = getStudents.main(
            "gc_41672.202045_fullgc_2021-07-22-17-11-55.csv")
        studentNotFound = False
        for file in os.listdir("hw"):
            name, ext = os.path.splitext(file)
            if ext == ".rkt" and name not in result:
                studentNotFound = True
            
        self.assertFalse(studentNotFound)
    
    def test_txt_files_same_as_student_ids(self):
        result = getStudents.main(
            "gc_41672.202045_fullgc_2021-07-22-17-11-55.csv")
        studentNotFound = False
        for file in os.listdir("hw"):
            name, ext = os.path.splitext(file)
            if ext == ".txt" and name not in result:
                studentNotFound = True
            
        self.assertFalse(studentNotFound)

    def test_hw_dir_files_twice_as_much_as_rkt_files(self):
        isTwice = True
        count = 0
        for file in os.listdir("hw"):
            name, ext = os.path.splitext(file)
            if ext == ".rkt":
                count += 1
        if len(os.listdir("hw")) != 2 * count:
            isTwice = False
        
        self.assertTrue(isTwice)

class TestKey(unittest.TestCase):
    def test_init_key(self):
        key = Key("hw5k (1).rkt")
        self.assertIsInstance(key, Key)
    
    def test_questions_list(self):
        key = Key("hw5k (1).rkt")
        result  = key.get_all_questions()
        self.assertIsInstance(result, list)
    
    def test_questions(self):
        key = Key("hw5k (1).rkt")
        result  = key.get_all_questions()
        self.assertEqual(result, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13a", "13b"])


    def test_total_points(self):
        key = Key("hw5k (1).rkt")
        result = key.get_total_points()
        self.assertEqual(result, 100)
    
    def test_individual_points(self):
        key = Key("hw5k (1).rkt")
        result = key.get_individual_points()
        expected = {
            "1": 7,
            "2": 7,
            "3": 7,
            "4": 7,
            "5": 7,
            "6": 7,
            "7": 7,
            "8": 7,
            "9": 7,
            "10": 7,
            "11": 7,
            "12": 7,
            "13a": 10,
            "13b": 6,
        }
        self.assertEqual(result, expected)
    

    def test_get_answer1(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[0])
        self.assertIn("lookup", result)
        self.assertNotIn("bool-eval", result)

    def test_get_answer2(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[1])
        self.assertIn("dummy1", result)
        self.assertNotIn("dummy2", result)
        self.assertNotIn("bool-eval", result)

    def test_get_answer3(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[2])
        self.assertIn("dummy2", result)
        self.assertNotIn("dummy3", result)
        self.assertNotIn("dummy1", result)

    def test_get_answer4(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[3])
        self.assertIn("dummy3", result)
        self.assertNotIn("dummy4", result)
        self.assertNotIn("dummy2", result)

    def test_get_answer5(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[4])
        self.assertIn("dummy4", result)
        self.assertNotIn("get-variables", result)
        self.assertNotIn("dummy3", result)

    def test_get_answer6(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[5])
        self.assertIn("get-variables", result)
        self.assertNotIn("make_bindings", result)
        self.assertNotIn("dummy4", result)

    def test_get_answer7(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[6])
        self.assertIn("make_bindings", result)
        self.assertNotIn("insert_bindings", result)
        self.assertNotIn("get-variables", result)

    def test_get_answer8(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[7])
        self.assertIn("insert_binding", result)
        self.assertNotIn("insert_multiple_bindings", result)
        self.assertNotIn("make_bindings", result)

    def test_get_answer9(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[8])
        self.assertIn("insert_multiple_bindings", result)
        self.assertNotIn("extend_table", result)

    def test_get_answer10(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[9])
        self.assertIn("extend_table", result)
        self.assertNotIn("make-truth-table", result)

    def test_get_answer11(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[10])
        self.assertIn("make-truth-table", result)
        self.assertNotIn("run-on-truth-table", result)

    def test_get_answer12(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[11])
        self.assertIn("run-on-truth-table", result)
        self.assertNotIn("atleast-one-true", result)

    def test_get_answer13(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[12])
        self.assertIn("atleast-one-true", result)
        self.assertNotIn("is-satisfied", result)

    def test_get_answer14(self):
        key = Key("hw5k (1).rkt")
        questions  = key.get_all_questions()
        result = key.get_answer(questions[13])
        self.assertIn("is-satisfied?", result)

if __name__ == '__main__':
    unittest.main()
