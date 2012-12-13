# Incorrect code
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
grid = []
EMPTY = []
for x in range(N):
    grid.append(EMPTY)
    for y in range(N):
        grid[-1].append(1)
