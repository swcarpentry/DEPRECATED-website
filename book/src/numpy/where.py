import numpy as np
vector = np.array([10, 20, 30, 40])
print vector
print np.where(vector < 25, vector, 0)
print np.where(vector > 25, vector/10, vector)
