import numpy

data = [x.strip().split(',') for x in open('infection.csv', 'r').readlines()]
data = [float(x[1])/float(x[2]) for x in data[1:]]
coeff = numpy.polyfit(range(len(data)), data, 1)
print '%8.6f x + %8.6f' % (coeff[0], coeff[1])
