import sys

total = 0
for value in sys.argv[1:]:
    total += float(value)
print total
