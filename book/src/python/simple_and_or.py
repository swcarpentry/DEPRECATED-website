data = [0, 3, 2, -1, 1, 4, 4, 6, 5, 5, 6]
num_outliers = 0
for n in data:
    if (n < 0) or (n > 5):
        num_outliers = num_outliers + 1
print num_outliers, "values out of range"
