#!/usr/bin/env python3

import sys
import os
import re
import argparse

def main():
    args = argparser()
    cwd = getcwd()
    # print("mypathis: " + cwd)


def argparser():
# Arge Parser Setup
    parser = argparse.ArgumentParser(description='Finds and replaces all instances of a User Id passed as an positional argument in Dolphin data folders, file names, as well as .txts recursively')
    # parser.add_argument('--match', 'm', required='True', help='UserId to match (Required)')

    args = parser.parse_args()
    return args


# Gets current workding dir 
def getcwd():
    # get current working dir
    cwd = os.getcwd()
    return cwd


if __name__ == "__main__":
    sys.exit(main())