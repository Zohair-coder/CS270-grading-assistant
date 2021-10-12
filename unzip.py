# Download all homework files by clicking on the homework column in Blackboard
# and selecting "Assignment File Download"
# Unzip files to a folder inside current directory
# change directory variable to the name of the new directory
# change homework_number to homework number
# script will remove all text files and rename all rkt files to student ids

import os
import re
import zipfile


def main(zipfile, directory="hw"):
    
    os.mkdir(directory)
    unzip(zipfile, directory)
    os.chdir(directory)
    rename()
    os.chdir("..")

def move_txt():
    files_in_directory = os.listdir()
    filtered_files = [
        file for file in files_in_directory if file.endswith(".txt")]

    for file in filtered_files:
        os.replace(file, "../")

def rename():
    for file in os.listdir():
        name, ext = os.path.splitext(file)
        search_string = ".*?_(\w*?)_"
        match = re.search(search_string, name)
        if match:
            new_name = "{}{}".format(match.group(1), ext)
            os.rename(file, new_name)

def unzip(zip, dir):
    with zipfile.ZipFile(zip, 'r') as zip_ref:
        zip_ref.extractall(dir)

if __name__ == "__main__":
    main("gradebook_41672.202045_HW5.Su21_2021-08-06-15-08-15.zip")
