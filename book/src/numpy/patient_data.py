import numpy as np
data = np.array([
    [1, 3, 3, 5, 12, 10, 9],
    [0, 1, 2, 4, 8, 7, 8],
    [0, 4, 11, 15, 21, 28, 37],
    [2, 2, 2, 3, 3, 2, 1],
    [1, 3, 4, 5, 10, 8, 6]
])
print data
print data[:, 0]
print data[0, :]
print data.mean()
print data.mean(0)
print data.mean(1)

print data[:, 0]
print data[:, 0] == 0.
print data[ data[:, 0] == 0. ]
print data[ data[:, 0] == 0. ].mean(0)
