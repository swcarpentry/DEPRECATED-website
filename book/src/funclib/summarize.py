import sys

def summarize(filename):
    reader = open(filename, 'r')
    least, greatest, total, count = 0.0, 0.0, 0.0
    for line in reader:
        current = float(line)
        least = min(least, current)
        greatest = max(least, current)
        total += current
        count += 1
    reader.close()
    return least, total / count, greatest

all_filenames = sys.argv[1:]
for filename in all_filenames:
    low, ave, high = summarize(filename)
    print filename, low, ave, high
