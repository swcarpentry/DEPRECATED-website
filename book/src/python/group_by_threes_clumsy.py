# Combine successive triples of data.
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
result = []
for i in range(0, len(data), 3):
    sum = data[i]
    if (i+1) < len(data):
        sum += data[i+1]
    if (i+2) < len(data):
        sum += data[i+2]
    result.append(sum)
print "grouped data:", result
