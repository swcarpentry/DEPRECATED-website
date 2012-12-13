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

def earliest_observation(data):
    '''How early did we see each bird?'''

    result = {}
    for (date, time, bird) in data:
        if bird not in result:
            result[bird] = time
        else:
          result[bird] = min(result[bird], time)

    return result

if __name__ == '__main__':
    observations = read_observations(sys.argv[1])
    earliest = earliest_observation(observations)
    print earliest
