# Find the mean.
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
total = 0
number = 0
for value in data:
    total = total + value
    number = number + 1
mean = float(total) / number
print "mean is", mean
