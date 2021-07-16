import re

def main(key_file, key_dir="key", key_answers_dir="answers"):
    with open(key_file, "r") as f:
        key_string = f.read()

    search_string = r"; ?Question \d+.*?(\(define.*?)(^;end$)"
    matches = re.finditer(search_string, key_string, re.DOTALL | re.MULTILINE)
    
    for index, match in enumerate(matches):
        with open("key/answers/{}.txt".format(index+1), "w") as f:
            f.write(match.group(1))

if __name__ == "__main__":
    key_file = "hw3k (2).rkt"
    main(key_file)
