data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
width = 3
result = []
for i in range(0, len(data), width):
    upper_bound = min(i+width, len(data))
    sum = 0
    for j in range(i, upper_bound):
        sum += data[j]
    result.append(sum)
print "grouped data:", result
