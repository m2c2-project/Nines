#!/usr/bin/env python3

import sys
import os
import re
import argparse

def main():
    args = argparser()
    print(args.match)
    print(args.replace)
    cwd = getcwd()
    # print("mypathis: " + cwd)

    return 0


# Arge Parser Setup
def argparser():
    parser = argparse.ArgumentParser(description='Finds and replaces all instances of a User Id passed as an positional argument in Dolphin data folders, file names, as well as .txts recursively')
    # Parser matcha dn replace arguments, required fields
    parser.add_argument('match', help='UserId to match and replace (Required)')
    parser.add_argument('replace', help='Replacement string for match values')
    
    args = parser.parse_args()


    return args


# Gets current workding dir 
def getcwd():
    # get current working dir
    cwd = os.getcwd()
    return cwd


# Maincontrol
if __name__ == "__main__":
    sys.exit(main())