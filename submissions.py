import os
import re


class Submissions:
    def __init__(self, src_dir, dest_dir, questions):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.questions = questions
        self.extract_data()
    
    # gets every students answer and places it in answers/abc123/question_name.txt file
    def extract_data(self):
        for file in os.listdir(self.src_dir):
            # gets file name and extension. name of rkt file is going to be student id
            id, ext = os.path.splitext(file)
            if ext == ".rkt":
                os.makedirs("./{}/{}".format(self.dest_dir, id), exist_ok=True)
                with open("{}/{}".format(self.src_dir, file), "r") as f:
                    submission = f.read()
                for question in self.questions:
                    search_string = r"; ?Question {}:.*?(\(define.*?)^;end$".format(question)
                    match = re.search(search_string, submission,
                            re.DOTALL | re.MULTILINE)
                    if match:
                        answer = match.group(1)
                        with open("{}/{}/{}.txt".format(self.dest_dir, id, question), "w") as f:
                            f.write(answer)
                    else:
                        Exception("Question {} not found in {}".format(question, file))
            else: # if file isn't rkt file, it must be a txt file with student info
                os.replace("{}/{}".format(self.src_dir, file), "{}/{}/{}".format(self.dest_dir, id, file))

    def get_answer(self, id, question):
        submitted_students = self.get_submitted_ids()
        for student in submitted_students:
            if student == id:
                with open("{}/{}/{}.txt".format(self.dest_dir, id, question)) as f:
                    answer = f.read()
                return answer
        Exception("Answer not found for {}, question {}".format(id, question))

    def get_submitted_ids(self):
        return os.listdir(self.dest_dir)
    
