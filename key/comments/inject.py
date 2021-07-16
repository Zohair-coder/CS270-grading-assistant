import os

files = os.listdir() 

for file in files:
    num = file.strip(".txt")
    if num == '8':
        string = '#{}: -1 your lambda is just andi!'.format(
            num)
        with open(file, "a") as f:
            f.write("\n" + string)
