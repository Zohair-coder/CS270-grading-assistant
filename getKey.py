import re

def main(key_file, key_dir="key", key_answers_dir="answers"):
    with open(key_file, "r") as f:
        key_string = f.read()

    matches = []
    search_string = r"; ?Question 6.*?(\(define.*?)(^;end$)"
    match = re.search(search_string, key_string, re.DOTALL | re.MULTILINE)
    if match:
        matches.append(match)

    for index, match in enumerate(matches):
        with open("{}/{}/{}.txt".format(key_dir, key_answers_dir, index+1), "w") as f:
            f.write(match.group(1))

if __name__ == "__main__":
    key_file = "hw3k (2).rkt"
    main(key_file)
