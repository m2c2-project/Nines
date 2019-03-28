#!/usr/bin/env python3

import sys
import os
import re
import argparse

# Global Static Variables:
ROOT_DIRECTORY = os.getcwd()
TEXTEXT = '.txt'

# Global Variables
match = ""
replace = ""


def main():
    global match, replace
    # Collect args from input and create needed data structures
    args = argParser()
    match = args.match
    replace = args.replace

    # Check to see if a match folder currently exists
    matchFolder = matchFolderExists(args.match)
    # Create replace folder
    replaceFolder = makeFolder(args.replace)
    # Switch to replace folder Dir
    os.chdir(replaceFolder)

    # iterate over all files in current dir
    iterateFilesInDir(matchFolder)

    return 0



def makeReplaceTerms():
    # Replacement dictionary {value to find: value to replace} -> Dict
    replaceTerms = {
        "ID:"+match: "ID:"+replace,
        "user_id:"+match: "user_id"+replace,
        "user_ID"+match: "ID:"+replace               
    }

    return replaceTerms


# Iterate over files in a directory
def iterateFilesInDir(directory):
    for file in os.listdir(directory):
        fileName = os.fsdecode(file)
        # if a text file and not a beep_log
        if fileName.endswith(TEXTEXT) and 'beep_log' not in fileName:
            fileUrl = os.path.join(directory, fileName)
            data = openFile(fileUrl)
            scrubbedData = multireplace(data)
            print(scrubbedData)

        

def multireplace(string):
    replaceDict = makeReplaceTerms()
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # {'999': 'AB', 'abc': 'ABC'} against the string 'hey abc' should produce 'hey ABC' and not 'hey ABc'
    substrs = sorted(replaceDict, key=len, reverse=True)

    # Create a regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replaceDict[match.group(0)], string)



# Opens file and reads data, closes file -> data
def openFile(filePath):
    with open(filePath, 'r') as file:
        data = file.read()
    return data
    

# Checks if match folder exists -> directory path
def matchFolderExists(folderName):
    # Create path for folder in correct formatting for OS
    dirPath = os.path.join(getCwd(), folderName)
    # If folder doesn't exist, report and exit
    if not os.path.isdir(dirPath):
        print('Target match folder %s does not exist' % folderName)
        sys.exit()
    # Return folder path otherwise
    return dirPath


# Create new folder -> folder path
def makeFolder(folderName):
    # Create path for folder in correct formatting for OS
    dirPath = os.path.join(getCwd(), folderName)
    # If folder doesn't exist, make it and report
    if not os.path.isdir(dirPath):
        try:
            os.mkdir(dirPath)
        except OSError:
            print('Creation of the replacement directory failed')
            sys.exit()
        else:
            print('Successfully created the directory')
    else:
        print('Cannot create replacement directory, folder already exists')
        sys.exit()
    # Return folder path otherwise
    return dirPath


# Gets current workding dir  -> cwd
def getCwd():
    # get current working dir
    cwd = os.getcwd()
    return cwd


# Arge Parser Setup -> args object
def argParser():
    parser = argparse.ArgumentParser(description='Finds and replaces all instances of a User Id passed as an positional argument in Dolphin data folders, '
    'file names, as well as .txts recursively. Will only work with Alphanumeric Characters')
    
    # Parser match and replace arguments, required fields
    parser.add_argument('match', help='UserId to match and replace (Required)')
    parser.add_argument('replace', help='Replacement string for match values')
    
    args = parser.parse_args()

    # Check validity of arguments before returning
    for key, value in vars(args).items():
        if not value.isalnum():
            print(value + ' is an invalid %s argument.' % key)
            sys.exit()
    return args


# Maincontrol
if __name__ == "__main__":
    sys.exit(main())