# Report where values are not monotonically inreasing
data = [1, 2, 2, 3, 4, 4, 5, 6, 5, 6, 7, 7, 8]
i = 2
for i in range(2, len(data)):
    if data[i] < data[i-1]:
        print "failure:", i
    i = i + 1
