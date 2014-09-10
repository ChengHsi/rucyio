#!/usr/bin/env python

"""
file comparator

compare two file iteratively to list all file1 lines excluded from file2 
"""

#
## Code goes here.
#
import sys

def file_compare():
    filename1 = str(sys.argv[1])
    filename2 = str(sys.argv[2])
    count = 0
    with open (filename1, 'r') as big:
        with open(filename2, 'r') as small:
            exclusions = [line.rstrip('\n') for line in small]
            for line in big:
                if not any(exclusion in line for exclusion in exclusions):
                    count += 1
    print count

if __name__=='__main__':
    file_compare()
