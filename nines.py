#!/usr/bin/env python3

import sys
import os
import argparse

# Global Static Variables:
ROOT_DIRECTORY = os.getcwd()
TEXTEXT = '.txt'

def main():
    # Collect args from input
    args = argParser()
    # Check to see if a match folder currently exists
    oldFolder = matchFolderExists(args.match)
    # Create replace folder
    newFolder = makeFolder(args.replace)
    # Switch to replace folder Dir
    os.chdir(newFolder)
    # iterate over all files in current dir
    iterateFilesInDir(oldFolder)

    return 0

def iterateFilesInDir(directory):
    for file in os.listdir(directory):
        fileName = os.fsdecode(file)
        # if a text file and not a beep_log
        if fileName.endswith(TEXTEXT) and 'beep_log' not in fileName:
            print(fileName)
    


# Check if match folder exists
def matchFolderExists(folderName):
    # Create path for folder in correct formatting for OS
    dirPath = os.path.join(getCwd(), folderName)
    # If folder doesn't exist, report and exit
    if not os.path.isdir(dirPath):
        print('Target match folder %s does not exist' % folderName)
        sys.exit()
    # Return folder path otherwise
    return dirPath


# Create new folder
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


# Gets current workding dir 
def getCwd():
    # get current working dir
    cwd = os.getcwd()
    return cwd


# Arge Parser Setup
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