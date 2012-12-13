import sys

def count_names(lines):
  '''Count unique lines of text, returning dictionary.'''

    result = {}
    for name in lines:
        name = name.strip()
        if name not in result:
            result[name] = 1
        else:
            result[name] = result[name] + 1

    return result

if __name__ == '__main__':
    reader = open(sys.argv[1], 'r')
    lines = reader.readlines()
    reader.close()
    count = count_names(lines)
    for name in count:
        print name, count[name]
