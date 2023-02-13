import os
import re

# define a function to read the file and return the file content
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# define a function to write content to the file
def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# define a function to find all the files in the directory
def find_files(directory):
    # Use os.walk to get all the files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        # Iterate through each file
        for file in files:
            # Check if the file name is "analysis.md" or "domainanalysis.md"
            if(file == "analysis.md" or file == "domainanalysis.md"):
                # If it is, return the full path of the file
                yield os.path.join(root, file)

# define a function to process the file
def process_file(file):
    # Read the file
    content = read_file(file)
    # Split the content by the subtitles
    sections = content.split('##')
    # Initialize a dictionary
    sections_dict = {}
    # Iterate through each section
    for section in sections:
        # Split the section by the new line character
        lines = section.split('\n')
        # Get the first line of the section
        section_title = lines[0]
        # Remove whitespaces
        section_title = section_title.strip()
        # Initialize an empty list
        section_content = []
        # Iterate through the remaining lines
        for line in lines[1:]:
            # Remove whitespaces
            line = line.strip()
            # Skip blank lines
            if line == '':
                continue
            # Remove the bullet points
            line = re.sub('^-\s', '', line)
            # Append the line to the section content
            section_content.append(line)
        # Add the section title and content to the dictionary
        sections_dict[section_title] = section_content
    # Initialize the output
    output = ''
    # Iterate through the dictionary
    for section_title, section_content in sections_dict.items():
        # Write the section title
        output += '## {}\n'.format(section_title)
        # Write the section content
        for line in section_content:
            output += '- {}\n'.format(line)
        output += '\n'
    # Write the output to the file
    write_file(file, output)

# Define the directory to be processed
directory = '.'
# Find the files in the directory
files = find_files(directory)
# Iterate through each file
for file in files:
    # Process the file
    process_file(file)
    print('Processed file: {}'.format(file))
print('Done!')