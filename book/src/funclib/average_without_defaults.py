def average_list_range(values, start, end):
    result = 0.0
    i = start
    while i < end:
        result += values[i]
        i += 1
    return result / (end - start)

def average_list_from(values, start):
    return average_list_range(values, start, len(values))

def average_list_all(values):
    return average_list_range(values, 0, len(values))
