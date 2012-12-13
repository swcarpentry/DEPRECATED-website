from math import pi

def area(r):
    return pi * r * r

def circumference(r):
    return 2 * pi * r

def do_all(func, values):
    result = []
    for v in values:
        temp = func(v)
        result.append(temp)
    return result

print do_all(area, [1.0, 2.0, 3.0])

def slim(text):
    return text[1:-1]

print do_all(slim, ['abc', 'defgh'])
