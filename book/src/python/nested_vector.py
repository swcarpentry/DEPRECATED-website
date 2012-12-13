values = []
reader = open('data.txt', 'r')
for line in reader:
    x, y = line.split()
    coord = [float(x), float(y)]
    values.append(coord)
reader.close()
