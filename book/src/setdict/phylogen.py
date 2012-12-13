def combos(species):
    '''Generate all combinations of species in normalized order.'''

    result = []
    for i in range(len(species)):
        for j in range(i+1, len(species)):
            result.append((species[i], species[j]))
    return result

def find_min_pair(species, scores):
    '''Find a minimum-value pair of species in the scores table.'''

    min_pair, min_val = None, None
    for pair in combos(species):
        assert pair in scores, 'Pair (%s, %s) not in scores' % pair
        if (min_val is None) or (scores[pair] < min_val):
            min_pair, min_val = pair, scores[pair]
    assert min_val is not None, 'No minimum value found in scores'
    return min_pair

def create_new_parent(scores, pair):
    '''Create record for new parent.'''

    parent = '[%s %s]' % pair
    height = scores[pair] / 2.
    return parent, height

def remove_entries(species, scores, pair):
    '''Get combined species out of species list and scores.'''

    left, right = pair
    species.remove(left)
    species.remove(right)
    old_score = scores[pair]
    del scores[pair]
    return old_score

def make_pair(left, right):
    '''Make an ordered pair.'''

    if left < right:  return (left, right)
    else:             return (right, left)

# Pull entry combining half of new pair with something else.
def tidy_up(scores, old, other):
    pair = make_pair(old, other)
    score = scores[pair]
    del scores[pair]
    return score

def update(species, scores, pair, parent, old_parent_score):
    '''Remove two species from the scores table.'''

    left, right = pair
    for other in species:
        old_left_score = tidy_up(scores, left, other)
        old_right_score = tidy_up(scores, right, other)
        new_pair = make_pair(parent, other)
        new_score = (old_left_score + old_right_score - old_parent_score) / 2.
        scores[new_pair] = new_score
    
    species.append(parent)
    species.sort()

if __name__ == '__main__':

    species = ['human', 'mermaid', 'vampire', 'werewolf']

    scores = {
        ('human',   'mermaid')  : 12,
        ('human',   'vampire')  : 13,
        ('human',   'werewolf') :  5,
        ('mermaid', 'vampire')  : 15,
        ('mermaid', 'werewolf') : 29,
        ('vampire', 'werewolf') :  6
    }

    while len(scores) > 0:
        min_pair = find_min_pair(species, scores)
        parent, height = create_new_parent(scores, min_pair)
        print parent, height
        old_score = remove_entries(species, scores, min_pair)
        update(species, scores, min_pair, parent, old_score)
