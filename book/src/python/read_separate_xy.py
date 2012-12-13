x_values = []
y_values = []
reader = open('data.txt', 'r')
for line in reader:
    x, y = line.split()
    x = float(x)
    x_values.append(x)
    y = float(y)
    y_values.append(y)
reader.close()
