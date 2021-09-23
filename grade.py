from comments import Comments

class Grade:
    def __init__(self, id, questions):
        self.id = id
        self.questions = questions
        self.questions_to_comments = self.initialize_questions_to_comments()
        # dictionary mapping question to its grading status. True for checked, False for unchecked
        self.checked_questions = self.initialize_checked_questions()
    
    def initialize_questions_to_comments(self):
        q2p = dict()
        for question in self.questions:
            q2p[question] = Comments(question)
        return q2p
    
    def initialize_checked_questions(self):
        checked_questions = dict()
        for question in self.questions:
            checked_questions[question] = False
        return checked_questions
    
    def mark_checked_question(self, question):
        self.checked_questions[question] = True
    
    def is_checked(self, question):
        return self.checked_questions[question]
    
    # returns a list of ungraded questions
    def ungraded_questions(self):
        ungraded_questions = []
        for question, status in self.checked_questions.items():
            if status == False:
                ungraded_questions.append(question)
        
        return ungraded_questions
    
    def total_points_deducted(self):
        total_points_deducted = 0
        for comments in self.questions_to_comments.keys():
            total_points_deducted += comments.points_deducted()
        return total_points_deducted
