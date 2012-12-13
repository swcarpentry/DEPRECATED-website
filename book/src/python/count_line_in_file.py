reader = open("data.txt", "r")
number = 0
for line in reader:
    number = number + 1
reader.close()
print number, "values in file"
