expected = [ [4.0, 2.0], [3.0, 5.0], [1.0, 6.0] ]
actual   = [ [4.2, 1.7], [3.1, 5.0], [0.8, 6.1] ]
x_diff, y_diff = 0.0,  0.0
for i in range(len(actual)):
    e = expected[i]
    a = actual[i]
    x_diff += abs(e[0] - a[0])
    y_diff += abs(e[1] - a[1])
print "average errors:", x_diff / len(actual), y_diff / len(actual)
