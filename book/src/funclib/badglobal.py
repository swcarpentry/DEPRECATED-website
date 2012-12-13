largest = 0

def fixup(values):
    global largest
    for i in range(len(values)):
        if values[i] < 0.0:
            values[i] = 0.0
        if values[i] > largest:
            largest = values[i]

def scale(values):
    for i in range(len(values)):
        values[i] = values[i] / largest

rows = [1.0, 4.0, -2.5, 3.5]
fixup(rows)
scale(rows)
print rows

columns = [1.5, 1.5, -2.0, 3.0]
fixup(columns)
scale(columns)
print columns
