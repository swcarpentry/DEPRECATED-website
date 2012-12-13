#!/usr/bin/env python

'''Invasion Percolation Simulation

usage: invperc.py grid_size value_range random_seed

grid_size:   the width/height of the grid
             must be a positive odd integer

value_range: number of distinct values in grid
             must be a positive integer
             values will be selected randomly in 1..value_range

random_seed:   random number generation seed
             must be a positive integer
'''

import sys, random

FILLED = -1    # Used to mark filled cells.

def fail(msg):
    '''Print error message and halt program.'''
    print >> sys.stderr, msg
    sys.exit(1)

def create_grid(N):
    '''Return an NxN grid of zeros.'''

    assert N > 0, 'Grid size must be positive'
    assert N%2 == 1, 'Grid size must be odd'
    grid = []
    for x in range(N):
        grid.append([])
        for y in range(N):
            grid[-1].append(0)
    return grid

def fill_random_grid(grid, Z):
    '''Fill a grid with random values in 1..Z.
    Assumes the RNG has already been seeded.'''

    size = len(grid)
    assert size > 0, 'Grid size must be positive'
    assert size%2 == 1, 'Grid size must be odd'
    assert Z > 0, 'Random range must be positive'
    for x in range(N):
        for y in range(N):
            grid[x][y] = random.randint(1, Z)
    return grid

def mark_filled(grid, x, y):
    '''Mark a grid cell as filled.'''

    assert 0 <= x < len(grid), \
           'X coordinate out of range (%d vs %d)' % \
           (x, len(grid))
    assert 0 <= y < len(grid), \
           'Y coordinate out of range (%d vs %d)' % \
           (y, len(grid))

    grid[x][y] = FILLED

def is_candidate(grid, x, y):
    '''Is a cell a candidate for filling?'''

    return (x > 0) and (grid[x-1][y] == FILLED) \
        or (x < N-1) and (grid[x+1][y] == FILLED) \
        or (y > 0) and (grid[x][y-1] == FILLED) \
        or (y < N-1) and (grid[x][y+1] == FILLED)

def find_candidates(grid):
    '''Find low-valued neighbor cells.'''

    N = len(grid)
    min_val = sys.maxint
    min_set = set()
    for x in range(N):
        for y in range(N):
            if grid[x][y] == FILLED:
                pass
            elif is_candidate(grid, x, y):
                if grid[x][y] == min_val:
                    min_set.add((x, y))
                elif grid[x][y] < min_val:
                    min_val = grid[x][y]
                    min_set = set([(x, y)])

    return min_set

def fill_grid(grid):
    '''Fill an NxN grid until filled region hits boundary.'''

    N = len(grid)
    num_filled = 0
    while True:
        candidates = find_candidates(grid)
        assert candidates, 'No fillable cells found!'
        x, y = random.choice(list(candidates))
        mark_filled(grid, x, y)
        num_filled += 1
        if x in (0, N-1) or y in (0, N-1):
            break

    return num_filled

def do_random(arguments):
    '''Run a random simulation.'''

    # Parse arguments.
    try:
        grid_size = int(arguments[1])
        value_range = int(arguments[2])
        random_seed = int(arguments[3])
    except IndexError:
        fail('Expected 3 arguments, got %d' % len(arguments))
    except ValueError:
        fail('Expected integer arguments, got %s' % str(arguments))

    # Run simulation.
    random.seed(random_seed)
    grid = create_grid(grid_size)
    fill_random_grid(grid, value_range)
    mark_filled(grid, grid_size/2, grid_size/2)
    num_filled_cells = fill_grid(grid) + 1
    print '%d cells filled' % num_filled_cells

def main(scenario, arguments):
    '''Run the simulation.'''

    if scenario == 'random':
        do_random(arguments[1:])
    else:
        fail('Unknown scenario "%s"' % scenario)

# Main driver.
if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Must have at least a scenario name'
    main(sys.argv[1], sys.argv[2:])
