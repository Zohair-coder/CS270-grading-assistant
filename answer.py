"""
Stores the question name and its corresponding answer
"""

class Answer:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    
    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer