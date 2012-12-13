# Double the values in a list in place.
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
for i in range(len(data)):
    data[i] = 2 * data[i]
print "doubled data is:", data
