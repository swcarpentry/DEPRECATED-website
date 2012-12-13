def average_list(values):

    # The average of no values is 0.0.
    if len(values) == 0:
        return 0.0

    # Handle actual values.
    result = 0.0
    for v in values:
        result += v
    return result / len(values)

def average_list(values):

    # The average of no values is 0.0.
    if len(values) == 0:
        result = 0.0

    # Handle actual values.
    else:
        result = 0.0
        for v in values:
            result += v
        result /= len(values)

    # Return final result.
    return result

def average_list(values):
    result = 0.0
    if len(values) > 0:
        for v in values:
            result += v
        result /= len(values)
    return result
