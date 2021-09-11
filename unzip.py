# Download all homework files by clicking on the homework column in Blackboard
# and selecting "Assignment File Download"
# script will remove all text files and rename all rkt files to student ids

import os
import re
import zipfile


def main(zipfile, directory="hw"):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    unzip(zipfile, directory)
    os.chdir(directory)
    rename()
    os.chdir("..")

def rename():
    files = os.listdir()
    for file in files:
        name, ext = os.path.splitext(file) # gets file name and extension
        
        if ext == ".txt":
            with open(file, "r") as f:
                txt_content = f.read()
            search_string = r"Name:.*\((.*)\)" # gets the name of the student from the unzipped text file
            match = re.search(search_string, txt_content)
            if match:
                id = match.group(1)
                search_string = r"{}.*\.rkt".format(id) # check if a rkt file containing the student id is in the directory
                found = False
                for f in files:
                    match = re.search(search_string, f)
                    if match:
                        os.rename(f, id+".rkt") # if found, rename the file to abc123.rkt 
                        found = True
                        break
                if not found:
                    raise Exception("No match found for rkt file containing {} in file name".format(id))
            else:
                raise Exception("Student ID not found in txt file giving information about submission after extracting the submissions zip file. Text file name: {}".format(file))

                

        # search_string = "HW\d+\.Su21_(\w*?)_"
        # match = re.search(search_string, name)
        # if match:
        #     new_name = "{}{}".format(match.group(1), ext)
        #     os.rename(file, new_name)

def unzip(zip, dir):
    with zipfile.ZipFile(zip, 'r') as zip_ref:
        zip_ref.extractall(dir)

if __name__ == "__main__":
    main("gradebook_41672.202045_HW5.Su21_2021-08-06-15-08-15.zip")
