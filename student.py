# Stores information about a single student

class Student:
    def __init__(self, id, name, animal_name):
        self.id = id
        self.name = name
        self.animal_name = animal_name
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_animal_name(self):
        return self.animal_name
        
    def get_first_name(self):
        return self.name.split()[0]

    def get_last_name(self):
        return self.name.split()[1]
    