"""
Gets the answer of a specific question by reading it from disk
"""

class Answer:
    def __init__(self, id, dir):
        self.id = id
        self.dir = dir

    def get_answer(self, question):
        with open("{}/{}/{}.txt".format(dir, id, question)) as f:
            answer = f.read()
        return answer