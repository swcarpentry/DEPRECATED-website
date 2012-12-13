data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
result = []
for i in range(0, len(data), 3):
    upper_bound = min(i+3, len(data))
    sum = 0
    for j in range(i, upper_bound):
        sum += data[j]
    result.append(sum)
print "grouped data:", result
