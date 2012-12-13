# Find the mean.
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
total = 0
for value in data:
    total = total + value
mean = float(total) / len(data)
print "mean is", mean
