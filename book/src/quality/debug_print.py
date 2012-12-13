import sys

def insert_or_increment(counts, species, number):
    # Look for species in list.
    print 'insert_or_increment(', counts, ',', species, ',', number, ')'
    for (s, n) in counts:
        print '...checking against', s, n
        # If we have seen it before, add to its count and exit.
        if s == species:
            n += number
            print '...species matched, so returning with', counts
            return
    # Haven't seen it before, so add it.
    counts.append([species, number])
    print 'new species, so returning with', counts

source = open(sys.argv[1], 'r')
counts = []
for line in source:
    species, number = line.strip().split(',')
    insert_or_increment(counts, species, int(number))
counts.sort()
for (s, n) in counts:
    print '%s: %d' % (s, n)
