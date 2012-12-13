# Count the number of lines in a file
reader = open("data.txt", "r")
number = 0
for line in reader:
    number = number + 1
reader.close()
print number, "lines in file"
