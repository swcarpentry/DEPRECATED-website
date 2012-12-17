#!/usr/bin/env python

"""
Report non-ASCII characters and tabs in files.
"""

import sys

for filename in sys.argv[1:]:
    reader = open(filename, 'r')
    lines = reader.readlines()
    reader.close()
    tabs = True
    for (i, line) in enumerate(lines):
        if tabs and ('\t' in line):
            print('{0} {1} {2}'.format(filename, i+1, 'tab'))
            tabs = False
        for (j, c) in enumerate(line):
            if ord(c) > 128:
                print('{0} {1} {2} {3} &#{3};'.format(
                        filename, i+1, j+1, ord(c)))
