"""
Unit tests for CS270 Autograder
Make sure that config.json is created and the rosterFile, gradesFile, submissionsFile and keyFile fields are set
"""

import unittest
import main


class TestFilenames(unittest.TestCase):
    def test_roster_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertIn(".csv", roster_file)

    def test_grades_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertIn(".csv", grades_file)

    def test_submissions_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertIn(".zip", submissions_file)

    def test_key_file(self):
        roster_file, grades_file, submissions_file, key_file = main.get_filenames()
        self.assertIn(".rkt", key_file)

if __name__ == '__main__':
    unittest.main()
