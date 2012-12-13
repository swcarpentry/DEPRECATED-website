# Create an NxN grid of random integers in 1..Z.
assert N > 0, "Grid size must be positive"
assert N%2 == 1, "Grid size must be odd"
grid = []
for x in range(N):
    grid.append([])
    for y in range(N):
        grid[-1].append(1) # FIXME: need a random value
