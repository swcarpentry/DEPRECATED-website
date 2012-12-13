def median3(a, b, c):
    if (a < b < c) or (c < b < a):
        return b
    elif (a < c < b) or (b < c < a):
        return c
    elif (b < a < c) or (c < a < b):
        return a

print 1, 2, 3, '=>', median3(1, 2, 3)
print 20, 10, 30, '=>', median3(20, 10, 30)
print 300, 200, 100, '=>', median3(300, 200, 100)
