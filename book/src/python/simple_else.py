data = [0, 3, 2, -1, 1, 4, 4, 6, 5, 5, 6]
num_outliers = 0
num_valid = 0
for n in data:
    if 0 <= n <= 5:
        num_valid = num_valid + 1
    else:
        num_outliers = num_outliers + 1
print num_valid, "in range and", num_outliers, "outliers"
