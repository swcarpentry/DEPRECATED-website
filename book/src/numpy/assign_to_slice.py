import numpy as np
block = np.array([[10, 20, 30, 40], [110, 120, 130, 140], [210, 220, 230, 240]])
print block
block[1, 1:3] = 0
print block
