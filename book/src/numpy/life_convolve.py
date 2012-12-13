import sys
import numpy as np
from scipy.signal import convolve

FILTER = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)

def evolve(length, generations):
    current = np.zeros((length, length), np.uint8)  # create the initial world
    current[length/2, 1:(length-1)] = 1             # initialize the world
    next = np.zeros_like(current)                   # hold the world's next state

    # advance through each time step
    show(current)
    for i in range(generations):
        advance(current, next)
        current, next = next, current
        show(current)

def advance(current, next):
    assert current.shape[0] == current.shape[1], \
           'Expected square universe'
    next[:, :] = 0
    neighbors = convolve(current, FILTER, mode='same')
    next[(current == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    next[(current == 0) & (neighbors == 3)] = 1

def show(board):
    nx, ny = board.shape
    dashes = '+' + ('-' * nx) + '+'
    print dashes
    for y in range(ny-1, -1, -1):
        line = '|'
        for x in range(0, nx):
            if board[x, y]:
                line += '*'
            else:
                line += ' '
        line += '|'
        print line
    print dashes

def main(args):
    length = int(args[1])
    if len(args) > 2:
        generations = int(args[2])
    else:
        generations = length - 1
    evolve(length, generations)

if __name__ == '__main__':
    main(sys.argv)
