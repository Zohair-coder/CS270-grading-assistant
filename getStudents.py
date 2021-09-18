# DEPRECATED: roster.py now has the same functionality so this file needs to be delelted

# Download all student names by going to Blackboard grade center
# and selecting work offline => Download
# Make sure to select comma delimiter and place file in current directory
# Replace the read_filename variable with the downloaded file name
# A dictionary mapping student id's to student names will be returned 

import csv

def main(read_filename):
    rows = []
    
    with open(read_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        next(csvreader) # skip the header row
    
        for row in csvreader:
            rows.append(row)
    
    data_dict = {}
    for row in rows:
        key = row[2] # student id
        value = "{} {}".format(row[1], row[0]) # First name followed by last name
        data_dict[key] = value
    
    return data_dict
    
if __name__ == "__main__":
    main()
