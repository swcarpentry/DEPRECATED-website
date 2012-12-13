import sys

def count_lines(source):
    if type(source) == str:
        reader = open(source, 'r')
    result = 0
    for line in reader:
        result += 1
    if type(source) == str:
        reader.close()
    return result

if len(sys.argv) == 1:
    count_lines(sys.stdin)
else:
    for filename in sys.argv[1:]:
        count(filename)
