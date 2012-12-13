def positive(x):
    return x > 0

print filter(positive, [-5, 3, -2, 9, 0])

def bump(x):
    return x + 10

print map(bump, [-5, 3, -2, 9, 0])

def add(x, y):
    return x + y

print reduce(add, [-5, 3, -2, 9, 0])

print reduce(add, map(bump, filter(positive, [-5, 3, -2, 9, 0])))

total = 0
for val in [-5, 3, -2, 9, 0]:
    if val > 0:
        total += (val + 10)
print total
