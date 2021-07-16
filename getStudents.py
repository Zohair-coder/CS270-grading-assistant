# Download all student names by going to Blackboard grade center
# and selecting work offline => Download
# Make sure to select comma delimiter and place file in current directory
# Replace the read_filename variable with the downloaded file name
# Student names will be written to students.json file

import csv
import json
from os import write

def main(read_filename, write_filename="students.json"):
    rows = []
    
    with open(read_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        next(csvreader)
    
        for row in csvreader:
            rows.append(row)
    
    data_dict = {}
    for row in rows:
        key = row[2]
        value = "{} {}".format(row[1], row[0])
        data_dict[key] = value

    with open(write_filename, 'w') as f:
        f.write(json.dumps(data_dict, indent=4))

if __name__ == "__main__":
    main()
