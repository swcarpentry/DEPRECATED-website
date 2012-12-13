import sys

def count_atoms(lines):
  '''Count unique lines of text, returning dictionary.'''

    result = {}
    for atom in lines:
        atom = atom.strip()
        if atom not in result:
            result[atom] = 1
        else:
            result[atom] = result[atom] + 1

    return result

if __name__ == '__main__':
    reader = open(sys.argv[1], 'r')
    lines = reader.readlines()
    reader.close()
    count = count_atoms(lines)
    for atom in count:
        print atom, count[atom]
