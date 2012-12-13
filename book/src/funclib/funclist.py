from math import pi

def area(r):
    return pi * r * r

def circumference(r):
    return 2 * pi * r

funcs = [area, circumference]

for f in funcs:
    print f(1.0)
