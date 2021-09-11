import re
from answer import Answer


class Key:
    def __init__(self, file_name):
        self.file_name = file_name
        self.key_data = self.get_key_data()

    # returns a list of Answer objects containing the question
    # name and the corresponding answer
    def get_key_data(self):
        with open(self.file_name, "r") as f:
            key_string = f.read()
        search_string = r"; ?Question (.*?):.*?(\(define.*?)^;end$"
        matches = re.findall(search_string, key_string,
                             re.DOTALL | re.MULTILINE)
        data = []
        for match in matches:
            data.append(Answer(match[0], match[1]))
        return data

    # returns all the question names as a list of strings
    def get_all_questions(self):
        questions = []
        for answer in self.key_data:
            questions.append(answer.get_question())
        return questions

    # given a question, returns the corresponding answer
    # if no answer is found for given question, returns None
    def get_answer(self, question):
        for data in self.key_data:
            if data.get_question() == question:
                return data.get_answer()

        return None
