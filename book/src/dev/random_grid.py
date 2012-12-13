from random import seed, randint
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
assert Z > 0, "Range must be positive"
seed(S)
grid = []
for x in range(N):
    grid.append([])
    for y in range(N):
        grid[-1].append(randint(1, Z))
