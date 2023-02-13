import os
import chardet
# Set up the base directory
base_dir = os.getcwd()

# Loop through each subdirectory
for root, dirs, files in os.walk(base_dir):
    print("Current directory: {}".format(root))
    # Loop through each file in the subdirectory
    for file in files:
        # Check for .md files
        if file == 'prettyanalysis.md':
            try:
                print("Processing file: {}".format(file))
                # Detect the encoding of the file
                with open(os.path.join(root, file), 'rb') as f:
                    encoding = chardet.detect(f.read())['encoding']
                # If no encoding is detected, set it to UTF-8
                if encoding is None:
                    encoding = 'utf-8'
                    print("Encoding of file is None, setting to UTF-8")
                else:
                    print("Encoding of file is {}".format(encoding))
                # Open the .md file
                try:
                    with open(os.path.join(root, file), encoding=encoding) as f:
                        # Read the .md file
                        lines = f.readlines()
                        # Loop through each line
                        for line in lines:
                            # if line == '\n' and lines[lines.index(line) + 1] == '\n' and lines[lines.index(line) + 2] == '\n':
                            #     # Remove the line if there is more than one blank lines
                            #     lines[lines.index(line)] = ''
                            #     lines[lines.index(line) + 1] = ''
                            # Check if line starts with 'Plugins:', 'Frameworks:', 'License information:', 'Vulnerability and security issues:', or 'Poor practices:'
                            # if lines.index(line) == 0:
                            #     #check if line starts with '# ' and if that line has a text in it, if it doesnt have text, remove the '# '
                            #if line.startswith('- id') or in line only there is # and nothing else then remove the # and the line

                            if line.startswith('- id') or (line == ('# ')):
                                # line = ''
                                #delete the line
                                lines[lines.index(line)] = ''
                                    # if line.strip() == '# ':
                                    #     lines[lines.index(line)] = ''
                                    #     print("Removed '# ' from start of line")
                            
                            #     if not line.startswith('# '):
                            #         lines[lines.index(line)] = '# ' + line
                            #         print("Added '# ' to start of line")
                            # if line.lower().startswith('plugins:') or line.lower().startswith('file hashes used:') or line.lower().startswith('frameworks:') or line.lower().startswith('license information:') or line.lower().startswith('vulnerability and security issues:') or line.lower().startswith('poor practices:'):
                            #     # append # to the start of the line
                            #     lines[lines.index(line)] = '## ' + line
                            
                            if line.lower().startswith('Analysis of') or line.lower().startswith('- file hashes used:') or line.lower().startswith('- frameworks:') or line.lower().startswith('- license information:') or line.lower().startswith('- vulnerability and security issues:') or line.lower().startswith('- poor practices:') or line.lower().startswith('- plugins:') or line.lower().startswith('file hashes used:') or line.lower().startswith('frameworks:') or line.lower().startswith('license information:') or line.lower().startswith('vulnerability and security issues:') or line.lower().startswith('poor practices:'):
                                # remove - to the start of the line
                                lines[lines.index(line)] = line.lstrip('- ')
                                #then append '## ' to the start of the line
                                lines[lines.index(line)] = '## ' + line

                            # if not line.lower().startswith('## plugins:') or line.lower().startswith('## file hashes used:') or line.lower().startswith('## frameworks:') or line.lower().startswith('## license information:') or line.lower().startswith('## vulnerability and security issues:') or line.lower().startswith('## poor practices:'):
                            #     # print("Found line: {}".format(line))
                            #     # remove ## from the start of the line
                            #     lines[lines.index(line)] = line.lstrip('## ')
                                # Get the index of the :
                                # index = line.index(':')
                                # # Check if the content after the : is letters or characters
                                # if line[index+1:].strip() != ' ':
                                #     # Add a blank line after the :
                                #     lines.insert(lines.index(line), line[:index+1] + '\n')
                                #     print("Added blank line after ':'")
                                    # Remove any extra '## ' before the start of the word
                            # elif line.startswith('## ##'):
                            #             lines[lines.index(line)] = line.lstrip('## ')
                            #             print("Removed extra '## ' before word")
                            # elif not line.lower().startswith('## plugins:') or line.lower().startswith('## file hashes used:') or line.lower().startswith('## frameworks:') or line.lower().startswith('## license information:') or line.lower().startswith('## vulnerability and security issues:') or line.lower().startswith('## poor practices:'):
                            #             lines[lines.index(line)] = line.lstrip('## ')
                            #             print("Removed extra '## ' before word")
                        print("Writing lines to file" + os.path.join(root, file))
                    # Write the lines to the .md file
                    with open(os.path.join(root, file), 'w', encoding=encoding) as f:
                        f.writelines(lines)
                except UnicodeError:
                    # If the encoding fails, try using 'ignore' or 'replace' error handling
                    with open(os.path.join(root, file), encoding=encoding, errors='ignore') as f:
                        # Read the .md file
                        lines = f.readlines()
                        # Loop through each line
                        for line in lines:

                            
                            # Check if line starts with 'Plugins:', 'Frameworks:', 'License information:', 'Vulnerability and security issues:', or 'Poor practices:'
                            # if lines.index(line) == 0:
                            #     #check if line starts with '# ' if not add it
                            #     if not line.startswith('# '):
                            #         lines[lines.index(line)] = '# ' + line
                            #         print("Added '# ' to start of line")
                            if 'plugins:' in line.lower() or 'file hashes used:' in line.lower() or 'frameworks:' in line.lower() or 'license information:' in line.lower() or 'vulnerability and security issues:' in line.lower() or 'poor practices:' in line.lower():
                                #get the index of the :
                                index = line.index(':')
                                # append a new line after the : in the word
                                lines.insert(lines.index(line), line[:index+1] + '\n')
                            # if line == '\n' and lines[lines.index(line) + 1] == '\n' and lines[lines.index(line) + 2] == '\n':
                            #     lines[lines.index(line) + 2] = ''
                            #     print("Removed more than two continuous blank lines")
                            if line == '\n' and lines[lines.index(line) + 1] == '\n':
                                lines[lines.index(line) + 1] = ''
                                print("Removed two continuous blank lines")
                            if line.lower().startswith('plugins:') or line.lower().startswith('file hashes used:') or line.lower().startswith('frameworks:') or line.lower().startswith('license information:') or line.lower().startswith('vulnerability and security issues:') or line.lower().startswith('poor practices:'):
                                # append # to the start of the line
                                lines[lines.index(line)] = '## ' + line
                            
                            if line.lower().startswith('- plugins:') or line.lower().startswith('- file hashes used:') or line.lower().startswith('- frameworks:') or line.lower().startswith('- license information:') or line.lower().startswith('- vulnerability and security issues:') or line.lower().startswith('- poor practices:'):
                                # remove - to the start of the line
                                lines[lines.index(line)] = line.lstrip('- ')
                                #then append '## ' to the start of the line
                                lines[lines.index(line)] = '## ' + line
                                # remove ## from the start of the line
                               # lines[lines.index(line)] = line.lstrip('## ')
                                # Get the index of the :
                                # index = line.index(':')
                                # Check if the content after the : is letters or characters
                                # if line[index+1:].strip() != ' ':
                                    # Add a blank line after the :
                                    # lines.insert(lines.index(line), line[:index+1] + '\n')
                                    # print("Added blank line after ':'")
                                    # Remove any extra '## ' before the start of the word
                            # elif line.startswith('## ##'):
                            #             lines[lines.index(line)] = line.lstrip('## ')
                            #             print("Removed extra '## ' before word")
                            # elif not line.lower().startswith('## plugins:') or line.lower().startswith('## file hashes used:') or line.lower().startswith('## frameworks:') or line.lower().startswith('## license information:') or line.lower().startswith('## vulnerability and security issues:') or line.lower().startswith('## poor practices:'):
                            #             lines[lines.index(line)] = line.lstrip('## ')
                            #             print("Removed extra '## ' before word")

                    # Write the lines to the .md file
                    with open(os.path.join(root, file), 'w', encoding=encoding, errors='ignore') as f:
                        f.writelines(lines)
            except Exception as e:
                print("Error processing file: {}".format(file))
                print(e)

print("Done!")