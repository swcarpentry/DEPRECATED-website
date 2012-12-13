'''Calculate how many molecules of each type can be made with the atoms on hand.'''

import sys

def read_lines(filename):
    '''Read lines from file, stripping out blank lines and comments.'''

    reader = open(filename, 'r')
    lines = []
    for line in reader:
        line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    reader.close()

    return lines

def read_inventory(filename):
    '''Read inventory of available atoms.'''

    result = {}
    for line in read_lines(filename):
        name, count = line.split(' ')
        result[name] = int(count)

    return result

def read_formulas(filename):
    '''Read molecular formulas from file.'''

    result = {}                                        # 1
    for line in read_lines(filename):

        name, atoms = line.split(':')                  # 2
        name = name.strip()

        atoms = atoms.strip().split(' ')               # 3
        formula = {}
        for i in range(0, len(atoms), 2):              # 4
            formula[atoms[i]] = int(atoms[i+1])        # 5

        result[name] = formula                         # 6

    return result                                      # 7

def dict_divide(inventory, molecule):
    '''Calculate how much of a single molecule can be made with inventory.'''

    number = None
    for atom in molecule:
        required = molecule[atom]
        available = inventory.get(atom, 0)
        limit = available / required
        if (number is None) or (limit &lt; number):
            number = limit

    return number

def calculate_counts(inventory, formulas):
    '''Calculate how many of each molecule can be made with inventory.'''

    counts = {}
    for name in formulas:
        counts[name] = dict_divide(inventory, formulas[name])

    return counts

def show_counts(counts):
    '''Show how many of each kind of molecule we can make.'''

    names = counts.keys()
    names.sort()
    for name in names:
        print name, counts[name]

if __name__ == '__main__':
    inventory = read_inventory(sys.argv[1])
    formulas = read_formulas(sys.argv[2])
    counts = calculate_counts(inventory, formulas)
    show_counts(counts)
