# Loops can run inside loops.
for i in range(4):
    for j in range(i):
        print i, j
