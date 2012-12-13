def threshold(signal):
    return 1.0 / sum(signal)

data = [0.1, 0.4, 0.2]
print threshold(data)
t = threshold
print t(data)
