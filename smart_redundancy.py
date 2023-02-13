import chardet
import os
#use osgetcwd() to get the current working directory
root_dir = os.getcwd()
def check_files(root_dir):
    '''
    This function takes a root directory as argument
    and checks all files in the subdirectories 
    for redundant lines
    '''
    # walk through the directory
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            # check for the file named 'domainanalysis.md'
            if file == 'nonredundant.md':
                file_path = os.path.join(subdir, file)
                # call the check redundant lines function
                check_redundant_lines(file_path)

def check_redundant_lines(file):
    '''
    This function takes a file as argument
    and checks if the lines in the file are redundant
    '''
    # open the file and read in the lines
    with open(file, 'rb') as f:
        rawdata = f.read()
        # detect the encoding being used
        encoding = chardet.detect(rawdata)['encoding']
    
    # open the file and read in the lines
    with open(file, 'r', encoding=encoding) as f:
        lines = f.readlines()
    
    # create a list to store the checked lines
    checked_lines = []
    # loop through the lines and check for redundancy
    for line in lines:
        # split the line into words
        words = line.split()
        num_words = len(words)
        # set the redundant flag to False initially
        redundant = False
        # print("Checking for redundancy in line: " + line)
        
        # check if the line is empty
        if line.strip() == '':
            redundant = True
        
        # loop through the words and check against other lines
        for checked_line in checked_lines:
            checked_words = checked_line.split()
            num_checked_words = len(checked_words)
            # count the number of similar words
            num_similar_words = 0
            # check if the number of words is greater than zero
            if num_words > 0:
                for word in words:
                    if word in checked_words:
                        num_similar_words += 1
                # compare the number of similar words
                # to the total number of words
                similarity = num_similar_words/num_words
                print("Redundancy found in line: " + line + "; Similarity: " + str(similarity))
                if similarity > 0.28:
                    redundant = True
                    break
        
        # if the line is not redundant, add it
        # to the checked lines
        if not redundant:
            checked_lines.append(line)
    
    # write the checked lines to the file
    with open(file, 'w', encoding=encoding) as f:
        for line in checked_lines:
            f.write(line)
    
    print("File checked for redundancy")
    if len(checked_lines) != len(lines):
        print("Redundant lines found and removed")
    else:
        print("No redundant lines found")

# debug print
print("Redundancy check started")

# call the function
check_files(root_dir)

# debug print
print("Redundancy check finished")