import sys
import numpy as np

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
    length = current.shape[0]
    next[:, :] = 0
    for i in range(1, length-1):
        for j in range(1, length-1):
            neighbors = np.sum(current[i-1:i+2, j-1:j+2])
            if current[i, j] == 1:
                if 2 <= (neighbors-1) <= 3:
                    next[i, j] = 1
            else:
                if neighbors == 3:
                    next[i, j] = 1

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
