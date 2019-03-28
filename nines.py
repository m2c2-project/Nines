#!/usr/bin/env python3

import sys
import os
import re
import argparse

# Global Static Variables:
ROOT_DIRECTORY = os.getcwd()
TEXTEXT = '.txt'
READ = 'r'
MAKE = 'x'

# Global Variables
match = None
replace = None
folder = None 


def main():
    global match, replace, folder
    # Collect args from input and create needed data structures
    args = argParser()
    match = args.match
    replace = args.replace
    folder = args.folder

    # Check to see if a match folder currently exists
    matchFolderExists(folder)

    # Create replace folder
    replaceFolder = makeFolder(replace + '-new')

    # Switch to replace folder Dir
    os.chdir(replaceFolder)

    # MARK: Data replacement begins
    seekAndDestroy()
    print("Success! Results have been updated")

    return 0


# Creates a dictonary from the match and replace terms passed in as args and parses it with the Dolphin substrings
def makeReplaceTerms():
    # Replacement dictionary {value to find: value to replace} -> Dict
    replaceTerms = {
        "ID:"+match: "ID:"+replace,
        "user_id:"+match: "user_id:"+replace,
        "user_ID"+match: "user_ID:"+replace,
        #food_log pattern uses 2 of year to avoid issues with count column
        match+"|201" : replace+"|201"             
    }

    return replaceTerms


def seekAndDestroy():
    targetDir = os.path.join(ROOT_DIRECTORY, folder)
    for root, dirs, files in os.walk(targetDir):
        # Ignore hidden files and folders (i.e. git stuff)
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for f in files:
            # Ignores beep_log files ONLY!!!!!!!!
            if 'beep_log' not in f:
                # Change to correct new directory for saving purposes
                os.chdir(root.replace(folder, replace+'-new'))
                # URL of the old file to be scrubbed
                fileURL = os.path.join(root, f)
                # Scrub file
                scrubFile(fileURL, f)
        for d in dirs:
            # Create Subfolder
            makeFolder(d)


# Parse/Replace/SaveNew files from a directory
def scrubFile(fileURL, fileName):
    # Read file into mem
    data = readFile(fileURL)
    # Multireplace all instances of the substrings in data
    scrubbedData = multiReplace(data)
    # Replace match term in file name
    newFileName = simpleMatchReplace(fileName)
    # Create new File URL
    newFileUrl = os.path.join(getCwd(), newFileName)
    # Write to file
    writeFile(newFileUrl, scrubbedData)


# Simple .replace on a string passed in using the match and replace arguments
def simpleMatchReplace(string):
    newFileName = string.replace(match, replace)
    return newFileName

        
# Replace various substrings from a string in one pass
def multiReplace(string):
    # Grab replacement dict
    replaceDict = makeReplaceTerms()
    # Order from short len to longest for replacement control
    # {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc' will produce 'hey ABC' and not 'hey ABc'
    substrs = sorted(replaceDict, key=len, reverse=True)
    # Create a regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))
    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replaceDict[match.group(0)], string)


# Opens file and reads data, closes file -> data
def readFile(filePath):
    with open(filePath, READ) as file:
        data = file.read()
    return data


# Makes file, closes file
def writeFile(filePath, data):
    with open(filePath, MAKE) as file:
        file.write(data)
    

# Checks if match folder exists -> directory path
def matchFolderExists(folderName):
    # Create path for folder in correct formatting for OS
    dirPath = os.path.join(getCwd(), folderName)
    # If folder doesn't exist, report and exit
    if not os.path.isdir(dirPath):
        print('Target folder %s does not exist' % folderName)
        sys.exit()
    # Return folder path otherwise
    return dirPath


# Create new folder -> folder path
def makeFolder(folderName):
    # Create path for folder in correct formatting for OS
    dirPath = os.path.join(getCwd(), folderName)

    # If folder doesn't exist, make it and report
    if not folderExists(dirPath):
        try:
            os.mkdir(dirPath)
        except OSError:
            print('Creation of the replacement directory failed')
            sys.exit()
    else:
        print('Cannot create replacement directory, folder already exists')
        sys.exit()
    # Return folder path otherwise
    return dirPath


# Take a Directory URL and check to see if it exists -> Bool
def folderExists(folderURL):
    if not os.path.isdir(folderURL):
        return False
    else:
        return True


# Gets current workding dir  -> cwd
def getCwd():
    # get current working dir
    cwd = os.getcwd()
    return cwd


# Arge Parser Setup -> args object
def argParser():
    parser = argparse.ArgumentParser(description='Finds and replaces all instances of a user Id in a Dolphin user data folder, '
    'file names, as well as .txts, recursively. Will only work with Alphanumeric Characters. New folder will be named replace-new. This'
    'There are three positional arguments, and this script should be run from the directory which contains the user folder')
    # Parser match and replace arguments, required fields
    parser.add_argument('folder', help='Target Folder Name')
    parser.add_argument('match', help='UserId to match and replace')
    parser.add_argument('replace', help='Replacement string for match values')
    args = parser.parse_args()

    # Check validity of arguments before returning
    for key, value in vars(args).items():
        # Allow only Alphanumeric characters in arguments
        if not value.isalnum():
            print(value + ' is an invalid %s argument.' % key)
            sys.exit()
    return args


# Maincontrol
if __name__ == "__main__":
    sys.exit(main())