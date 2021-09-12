import os
import re


class Submissions:
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.extract_data()
    
    def extract_data(self):
        for file in os.listdir(self.src_dir):
            # gets file name and extension. name of rkt file is going to be student id
            id, ext = os.path.splitext(file)
            if ext == ".rkt":
                os.makedirs("./{}/{}".format(self.dest_dir, id), exist_ok=True)
                with open("{}/{}".format(self.src_dir, file), "r") as f:
                    submission = f.read()  
                search_string = r"; ?Question (.*?):.*?(\(define.*?)^;end$"
                # returns a list of lists with 2 elements, the first containing
                # the question name and the second containing the answer
                matches = re.findall(search_string, submission,
                            re.DOTALL | re.MULTILINE)
                for match in matches:
                    question_name = match[0]
                    answer = match[1]
                    with open("{}/{}/{}.txt".format(self.dest_dir, id, question_name), "w") as f:
                        f.write(answer)
            else: # if file isn't rkt file, it must be a txt file with student info
                os.replace("{}/{}".format(self.src_dir, file), "{}/{}/{}".format(self.dest_dir, id, file))


    
