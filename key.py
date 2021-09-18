import re

class Key:
    def __init__(self, file_name):
        self.file_name = file_name
        self.key_string = self.get_key_string()
        self.question_to_answer = self.get_questions_and_answers()

    def get_key_string(self):
        with open(self.file_name, "r") as f:
            key_string = f.read()
        return key_string

    # returns a dictionary mapping question to answer
    def get_questions_and_answers(self):
        search_string = r"; ?Question (\w*?):.*?(\(define.*?)^;end$"
        # returns a list of lists with 2 elements, the first containing
        # the question name and the second containing the answer
        matches = re.findall(search_string, self.key_string,
                             re.DOTALL | re.MULTILINE)
        data = dict()
        for match in matches:
            data[match[0]] = match[1]
        return data

    # returns the total points for this assignment as an integer
    # by extracting its value from the key
    def get_total_points(self):
        search_string = r"; ?Total Points: ?(\d+)" # searches for one or more digit after total points
        match = re.search(search_string, self.key_string)
        if match:
            return int(match.group(1))
        else:
            Exception("Total Points: [0-9]* string not found in key file {}.".format(self.file_name))

    # returns a dictionary mapping question to total points of that quesiton
    def get_individual_points(self):
        individual_points = dict()
        questions = self.get_all_questions()
        for question in questions:
            search_string = r"; ?Question {} points: ?(\d+)".format(question)
            match = re.search(search_string, self.key_string)
            if match:
                individual_points[question] = int(match.group(1))
            else:
                Exception("Question {} points: [0-9]+ string not found in key file {}".format(question, self.file_name))
        return individual_points




    # returns all the question names as a list of strings
    def get_all_questions(self):
        questions = []
        for answer in self.question_to_answer:
            questions.append(answer)
        return questions

    # given a question, returns the corresponding answer as a string
    # if no answer is found for given question, returns None
    def get_answer(self, question):
        return self.question_to_answer[question]

    # get a dictionary of questions mapped to answers
    def get_question_to_answer(self):
        return self.question_to_answer
