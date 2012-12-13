import sys

def read_observations(filename):
    '''Read data, return [(date, time, bird)...].'''

    reader = open(filename, 'r')
    result = []

    for line in reader:
        fields = line.split('#')[0].strip().split()
        assert len(fields) == 3, 'Bad line "%s"' % line
        result.append(fields)

    return result

def birds_by_date(data):
    '''Which birds were seen on each day?'''

    result = {}
    for (date, time, bird) in data:
        if date not in result:
            result[date] = {bird}
        else:
            result[date].add(bird)

    return result

if __name__ == '__main__':
    observations = read_observations(sys.argv[1])
    seen = earliest_observation(observations)
    print seen
