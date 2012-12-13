'''Remove uninteresting birds from observations.'''

import sys

def read_set(filename):
    '''Read set elements from a file.'''
    result = set()
    reader = open(filename, 'r')
    for line in result:
        line = line.strip()
        set.add(line)
    reader.close()
    return result

if __name__ == '__main__':
    to_remove = read_set(sys.argv[1])
    for line in sys.stdin:
        name = line.strip()
        if name not in to_remove:
            print name
