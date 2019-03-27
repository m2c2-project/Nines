#!/usr/bin/env python3

import sys
import os
import argparse

def main():
    args = argParser()
    oldFolder = folderExists(args.replace)
    newFolder = makeFolder(args.replace)

    return 0


# Check if replace folder exists
def folderExists(folderName):
    folderPath = os.path.join(getCwd(), folderName)
    if not os.path.isdir(folderPath):
        print("Target folder %s does not exist" % folderName)
        sys.exit()
    
    return folderPath


# Create new folder
def makeFolder(folderName):
    # Create path for folder in correct formatting for OS
    folderPath = os.path.join(getCwd(), folderName)
    # If folder doesn't exist, make it and report
    if not os.path.isdir(folderPath):
        try:
            os.mkdir(folderPath)
        except OSError:
            print("Creation of the replacement directory failed")
            sys.exit()
        else:
            print("Successfully created the directory")
    else:
        print("Cannot created directory, folder exists")
        sys.exit()

    return folderPath

# Gets current workding dir 
def getCwd():
    # get current working dir
    cwd = os.getcwd()
    print("The current working directory is %s" % cwd)
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
            print(value + " is an invalid " + key + " argument.")
            sys.exit()
    return args


# Maincontrol
if __name__ == "__main__":
    sys.exit(main())