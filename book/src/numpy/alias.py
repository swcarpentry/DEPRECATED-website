import numpy as np
first = np.ones((2, 2))
print first
second = first
print second
second[0, 0] = 9
print first

print first
second = first.copy()
second[0, 0] = 9
print first
