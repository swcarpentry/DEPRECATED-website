# Sum up at most the first three values.
test_cases = [[],                     # no data at all
              [10],                   # just one value
              [10, 20],               # two values
              [10, 20, 30],           # three
              [10, 20, 30, 40]]       # more than enough

for data in test_cases:
    limit = min(3, len(data))
    sum = 0
    for i in range(limit):
        sum += data[i]
    print data, "=>", sum
