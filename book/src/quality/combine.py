def combine_values(func, values):
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current

def add(a, b):
    return a + b

numbers = [1, 3, 6, 7, 9]
print combine_values(add, numbers)

print combine_values(add, [])
