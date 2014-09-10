#!/usr/bin/env python

"""
file comparator

compare two file iteratively to list all file1 lines excluded from file2
"""

#
## Code goes here.
#
import sys

file1 = str(sys.argv[1])
file2 = str(sys.argv[2])

def file_compare(filename1, filename2):
    count = 0
    with open (filename1, 'r') as big:
        with open(filename2, 'r') as small:
            exclusions = [line.rstrip('\n') for line in small]
            for line in big:
                if not any(exclusion in line for exclusion in exclusions):
                    count += 1
    print count

def file_compare2(file1, file2):
    list1 = [line.rstrip() for line in open(file1)]
    list2 = [line.rstrip() for line in open(file2)]
    #if list1 > list2:
    missing_list = list(set(list1)-set(list2))
    why_list = list(set(list2)-set(list1))
    f_write1 = open(str(file1)+'--minus--'+str(file2), 'w+')
    f_write2 = open(str(file2)+'--minus--'+str(file1), 'w+')
    for name in missing_list:
        f_write1.write(name + '\n')
    for name in why_list:
        f_write2.write(name + '\n')
    print '###Output File Name:###\n', f_write1, '\n', f_write2

if __name__=='__main__':
    file_compare2(file1, file2)
