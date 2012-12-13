def combine_values(func, values):
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current

def add(x, y):
    return x + y

def mul(x, y):
    return x * y

print combine_values(add, [1, 3, 5])

print combine_values(mul, [1, 3, 5])

