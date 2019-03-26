#!/usr/bin/env python3

import sys
import os
import re
import argparse

def main():
    args = argparser()
    folder = makeFolder(args.replace)

    return 0


# Arge Parser Setup
def argparser():
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


# Create new folder
def makeFolder(folderName):
    # Create path for folder in correct formatting for OS
    dirFolder = os.path.join(getcwd(), folderName)
    # If folder doesn't exist, make it and report
    if not os.path.isdir(dirFolder):
        try:
            os.mkdir(dirFolder)
        except OSError:
            print("Creation of the replacement directory failed")
        else:
            print("Successfully created the directory")

    return dirFolder


# Gets current workding dir 
def getcwd():
    # get current working dir
    cwd = os.getcwd()
    print("The current working directory is %s" % cwd)
    return cwd


# Maincontrol
if __name__ == "__main__":
    sys.exit(main())