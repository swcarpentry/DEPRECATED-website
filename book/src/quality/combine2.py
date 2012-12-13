def combine_values(func, values):
    assert len(values) > 0, 'Cannot combine values from empty list'
    current = values[0]
    for i in range(1, len(values)):
        current = func(current, values[i])
    return current

print combine_values(add, [])
