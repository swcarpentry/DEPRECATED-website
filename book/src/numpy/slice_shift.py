import numpy as np
vector = np.array([10, 20, 30, 40])
vector[0:3] = vector[1:4]
print vector
vector = np.array([10, 20, 30, 40])
vector[1:4] = vector[0:3]
print vector
