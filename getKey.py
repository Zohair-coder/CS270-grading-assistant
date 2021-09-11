import re


def main(key_file, key_dir="key", key_answers_dir="answers"):
    with open(key_file, "r") as f:
        key_string = f.read()

    matches = []
    search_string = r"; ?Question (.*?):.*?(\(define.*?)^;end$"
    matches = re.findall(search_string, key_string, re.DOTALL | re.MULTILINE)
    print(matches[0][1])
    # for index, match in enumerate(matches):
    #     with open("{}/{}/{}.txt".format(key_dir, key_answers_dir, index+1), "w") as f:
    #         f.write(match.group(1))


if __name__ == "__main__":
    key_file = "hw5k (1).rkt"
    main(key_file)
