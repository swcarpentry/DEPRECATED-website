'''Count lines in files.  If no filename arguments given,
read from standard input.'''
 
import sys

def count_lines(reader):
  '''Return number of lines in text read from reader.'''
  return len(reader.readlines())

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print count_lines(sys.stdin)
  else:
    r = open(sys.argv[1], 'r')
    print count_lines(r)
    r.close()
