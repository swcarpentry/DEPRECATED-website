reader = open("data.txt", "r")
total = 0.0
number = 0
for line in reader:
    total = total + line
    number = number + 1
reader.close()
print "mean is", total / number
