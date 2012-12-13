data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
for i in range(len(data)):
    if data[i] < data[i-1]:
        print "failure at index:", i
    i = i + 1
