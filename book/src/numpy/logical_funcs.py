import numpy as np
vector = np.array([0, 10, 20, 30])
print np.logical_and(vector <= 20, vector >= 20)
print vector[np.logical_and(vector <= 20, vector >= 20)]
print vector[(vector <= 20) & (vector >= 20)]
