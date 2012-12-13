import numpy as np
vec = np.array([0, 1, 2, 3])
print vec
vec[vec < 2] = 100
print vec
