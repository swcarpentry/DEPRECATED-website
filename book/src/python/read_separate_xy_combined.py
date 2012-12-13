x_values = []
y_values = []
reader = open('data.txt', 'r')
for line in reader:
    x, y = line.split()
    x_values.append(float(x))
    y_values.append(float(y))
reader.close()
