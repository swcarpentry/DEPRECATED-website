# Count number of values out of range.
data = [0, 3, 2, -1, 1, 4, 4, 6, 5, 5, 6]
num_outliers = 0
for value in data:
    if value < 0:
        num_outliers = num_outliers + 1
    if value > 5:
        num_outliers = num_outliers + 1
print num_outliers, "values out of range"
