import numpy as np
first = np.array([[1, 2, 3],
                  [4, 5, 6]])
print first
t = first.transpose()
print t
first[1, 1] = 999
print t
