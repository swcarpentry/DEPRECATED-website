# Sum up in groups of three.
test_cases = [[],
              [10],
              [10, 20],
              [10, 20, 30],
              [10, 20, 30, 40],
              [10, 20, 30, 40, 50, 60],
              [10, 20, 30, 40, 50, 60, 70, 80]]

for data in test_cases:
    result = []
    for i in range(0, len(data), 3):
        limit = min(i+3, len(data))
        sum = 0
        for i in range(i, limit):
            sum += data[i]
        result.append(sum)
    print data, "=>", result
