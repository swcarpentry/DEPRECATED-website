# Find the mean.
reader = open("data.txt", "r")
total = 0.0
number = 0
for line in reader:
    value = float(line)
    total = total + value
    number = number + 1
reader.close()
print "mean is", total / number
