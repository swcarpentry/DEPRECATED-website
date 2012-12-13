# Double the values in a list in place.
data = [1, 4, 2, 3, 3, 4, 3, 4, 1]
length = len(data) # 9
indices = range(length) # [0, 1, 2, 3, 4, 5, 6, 7, 8]
for i in indices:
    data[i] = 2 * data[i]
print "doubled data is:", data
