import chardet
import os


def check_file(file_contents):
    # check for duplicates
    dups = set()
    contents = ""
    for line in file_contents.split("\n"):
        if line in dups:
            # found a duplicate
            print("Found a duplicate: " + line)
            # do not add it to the new contents
            pass
        else:
            dups.add(line)
            contents += line + "\n"
    
    return contents

# walk through the directory
dups = set()
for root, dirs, files in os.walk("."):
    # create a list of filenames
    filenames = [os.path.join(root, file) for file in files if file == "prettyanalysis.md"]
    
    # map filenames to the check_file function
    file_contents = []
    for filename in filenames:
        with open(filename, 'rb') as f:
            enc = chardet.detect(f.read())
            if enc['encoding'] is None:
                enc['encoding'] = 'utf-8'
            file_contents.append(open(filename, encoding=enc['encoding'], errors='ignore').read())
    
    contents = [check_file(f) for f in file_contents]
    
    # overwrite the files with the new contents
    for i, filename in enumerate(filenames):
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(contents[i])
    
    print("Finished processing files.")