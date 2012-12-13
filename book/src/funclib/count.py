import sys

def count_lines(reader):
    result = 0
    for line in reader:
        result += 1
    return result

if len(sys.argv) == 1:
    count_lines(sys.stdin)
else:
    for filename in sys.argv[1:]:
        rd = open(filename, 'r')
        count_lines(rd)
        rd.close()
