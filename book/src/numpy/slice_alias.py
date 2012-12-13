import numpy as np
original = np.ones((3, 2))
print original
slice = original[0:2, 0:2]
print slice
slice[:,:] = 0
print slice
print original
