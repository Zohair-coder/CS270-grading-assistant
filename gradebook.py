from grade import Grade

class Gradebook:
    def __init__(self, ids, questions):
        self.ids = ids
        self.questions = questions
        self.id_to_grades = self.initialize_id_to_grades()
        self.names_graded = False

    def initialize_id_to_grades(self):
        grades = dict()
        for id in self.ids:
            grades[id] = Grade(id, self.questions)
        return grades
    
    # returns a dictionary of question numbers mapped to
    # a list of student id's of ungraded questions
    def ungraded(self):
        ungraded = dict()
        for question in self.questions:
            ungraded[question] = []
            for student, grade in self.id_to_grades.items():
                if question in grade.ungraded_questions():
                    ungraded[question].append(student)
        
        return ungraded
