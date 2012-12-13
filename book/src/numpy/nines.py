nines = []
sums = []
current = 0.0
for i in range(1, 10):
    num = 9.0 / (10.0 ** i)
    nines.append(num)
    current += num
    sums.append(current)
for i in range(len(nines)):
    print '%.18f %.18f' % (nines[i], sums[i])
