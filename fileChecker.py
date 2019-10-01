#####################################################################
#  Filename:    fileChecker.py                                      #
#  Author:      Nicholas Hebert                                     #
#  Date:        2019-09-30                                          #
#  Description: A simple program which reads a file and determines  #
#               how many lines it has alongside how many comments   #
#               or block comments it has. Intended to demonstrate   #
#               coding capabilities to CapitalOne.                  #
#####################################################################
# Imports
import os
import sys
import re # Regular Expressions

if len(sys.argv)<=1: # If the program is run without input then terminate
    print('No input given... Stopping the program.')
    exit()

# Class used to instantiate objects which hold file information.
# Requires the extension type as an input.
class FileDefs():
    # Upon initialization of class object, determine the language the file is
    # written in.
    def __init__(self, lang):
        self.num_lines = 0
        self.num_comm = 0
        self.num_sing_comm = 0
        self.num_block_line = 0
        self.num_block_comm = 0
        self.num_todo = 0
        if lang == ".pl":     #Perl
            self.comment_pattern = "\#"
            self.start_block_pattern = "=pod"
            self.end_block_pattern = "=cut"

        elif lang == ".sh":    #Shellscript or BASH
            self.comment_pattern = "\#"
            self.start_block_pattern = None
            self.end_block_pattern = None

        elif lang == ".s" or lang == ".asm":    #Assembly
            self.comment_pattern = "\;"
            self.start_block_pattern = "/*"
            self.end_block_pattern = "*/"

        elif lang == ".rb":     #Ruby on rails
            self.comment_pattern = "\#"
            self.start_block_pattern = None
            self.end_block_pattern = None

        elif lang == ".py":     #Python
            self.comment_pattern = "\#"
            self.start_block_pattern = None
            self.end_block_pattern = None

        elif lang == ".css":    #CSS
            self.comment_pattern = None
            self.start_block_pattern = "/*"
            self.end_block_pattern = "*/"

        elif lang == ".html":    #HTML
            self.comment_pattern = None
            self.start_block_pattern = "<!--"
            self.end_block_pattern = "-->"

        elif lang == ".pas" or lang == ".p" or lang == ".pascal":    #Pascal
            self.comment_pattern = "\/\/"
            self.start_block_pattern = "(*"
            self.end_block_pattern = "*)"

        elif lang == ".sql":    #SQL
            self.comment_pattern = "\-\-"
            self.start_block_pattern = "/*"
            self.end_block_pattern = "*/"

        elif lang == ".f90" or lang == ".f95" or lang == ".f03":    #Fortran 1990, 1995, 2003
            self.comment_pattern = "\!"
            self.start_block_pattern = None
            self.end_block_pattern = None

        else:    #The most common comment patterns between languages, and the default
            self.comment_pattern = "\/\/"
            self.start_block_pattern = "/*"
            self.end_block_pattern = "*/"
        # Includes the patterns for: Visal Basic; Swift; Javascript; PHP;
        # C and C++; Java; C#

    def CountComments(self, file):
        comment_block_level = 0 # This variable counts the nestation of the comments
        if self.comment_pattern != None: regex = "(?<!\")(" + self.comment_pattern + ")(?!.*\")"
        for line in file:
            # Count the lines
            self.num_lines+=1
            # Count the comment blocks and their inner components
            if self.start_block_pattern != None:
                if line.find(self.start_block_pattern) != -1 and line.find(self.end_block_pattern) != -1:
                    self.num_block_line += 1
                elif line.find(self.start_block_pattern) != -1:
                    comment_block_level += 1
                    self.num_block_line += 1
                elif line.find(self.end_block_pattern) != -1:
                    comment_block_level -= 1
                    self.num_block_line += 1
                elif (comment_block_level > 0):
                    self.num_block_comm += 1
            # Count the single line comments
            if self.comment_pattern != None:
                m = re.search(regex, line)
                if m != None:
                    self.num_sing_comm += 1
            # Count the TODO's
            if line.find("TODO:") != -1:
                self.num_todo += 1
        self.num_comm = self.num_block_comm + self.num_block_line + self.num_sing_comm

    def PrintStats(self):
        print('\n@@@ Checking file: ', file, '@@@')                 # Assumptions
        print('Total # of lines: ' + str(self.num_lines))           # Total number of lines in the file
        print('Total # of comment lines: ' + str(self.num_comm))    # Total sum of all comments in the file
        print('Total # of single line comments: ' + str(self.num_sing_comm))    # Total single line comments i.e. //
        print('Total # of comment lines within block comments: ' + str(self.num_block_comm)) # Total lines of comment between the block comment patterns
        print('Total # of block line comments: ' + str(self.num_block_line))    # Total number of lines containing a start or end comment block pattern
        print('Total # of TODO\'s: ' + str(self.num_todo))          # Number of instances where TODO is found somewhere in the file

#TODO: Calculate the flux vectors (bogus todo comment to test todo count)
# For each input given, process the file
for file in sys.argv[1:]:
    with open(file) as f:
        extension = os.path.splitext(file)[1]
        if extension == None or extension == "":
            print("File wihout extension found and skipped.")
            continue
        current_file = FileDefs(extension.lower())
        current_file.CountComments(f)
        current_file.PrintStats()

print("\nFinished checking given files. Processed: ", len(sys.argv[1:]), " file(s).")
