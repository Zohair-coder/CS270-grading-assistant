# Stores and gets information about entire roster
# Download all student names by going to Blackboard grade center
# and selecting work offline => Download
# Make sure to select comma delimiter and place file in current directory
# Replace the read_filename variable with the downloaded file name

from student import Student
import csv
import random

class Roster:
    def __init__(self, key_file, animals_file, id_to_animals_file="id_to_animals.json"):
        self.key_file = key_file
        self.animals_file = animals_file
        self.id_to_animals_file = id_to_animals_file

        self.id_to_name = self.get_student_data()
        self.id_to_animals = self.get_id_to_animals()
        
        self.students = dict()
        for id, name in self.id_to_name.items():
            self.students[id] = Student(id, name, self.id_to_animals[id])
    
    def get_student_data(self):
        rows = []

        with open(self.key_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            next(csvreader)  # skip the header row

            for row in csvreader:
                rows.append(row)

        data_dict = {}
        for row in rows:
            key = row[2]  # student id
            # First name followed by last name
            value = "{} {}".format(row[1], row[0])
            data_dict[key] = value

        return data_dict
    
    # returns Student object given an id
    def get_student(self, id):
        return self.students[id]
    
    def get_name(self, id):
        return self.students[id].get_name()
        
    def get_all_ids(self):
        return [id for id in self.students]
    
    # returns a set of students who did not submit anything given a list
    # of students who submitted their homework
    def get_unsubmitted_students(self, submitted_students):
        return set(self.get_all_ids()) - set(submitted_students)
    
    # read the animals file and return the list of animals
    def get_anonymous_animal_names(self):
        with open(self.animals_file, "r") as f:
            animals_s = f.read()
        animals_list = animals_s.split("\n")
        return animals_list
    
    # returns a dictionary of ids mapped to random animal names
    def get_id_to_animals(self):
        all_animals = self.get_anonymous_animal_names()
        ids = self.id_to_name.keys()
        id_to_animals = dict()
        for id in ids:
            random_num = random.randint(0, len(all_animals)-1)
            id_to_animals[id] = "Anonymous " + all_animals[random_num]
            all_animals.remove(all_animals[random_num])
        return id_to_animals
