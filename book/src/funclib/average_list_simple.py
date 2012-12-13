def average_list(values):
    result = 0.0
    for v in values:
        result += v
    return result / len(values)

for test in [[1.0], [1.0, 2.0], [1.0, 2.0, 5.0]]:
    print test, '=>', average_list(test)
