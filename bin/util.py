"""
Utilities used in Software Carpentry tools.
"""

import sys
import html5lib
from html5lib import treebuilders
from lxml import etree as ET
from lxml.html import html5parser

#-------------------------------------------------------------------------------

def read_xml(filename, mangle_entities=False):
    """
    Read in a document, returning the ElementTree doc node.
    """
    tree = treebuilders.getTreeBuilder('lxml')
    parser = html5lib.HTMLParser(strict=False, tree=tree)
    doc = html5parser.parse(filename, parser=parser)

    if parser.errors:
        sys.stderr.write('errors in {}\n'.format(filename))
        for e in parser.errors:
            sys.stderr.write('    {}\n'.format(e))

    return doc

#-------------------------------------------------------------------------------

def write_xml(filename, doc, unmangle_entities=False):
    """
    Write out a document.
    """
    with open(filename, 'w') as writer:
        writer.write(ET.tostring(doc.getroot()))

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    if len(sys.argv) not in (2, 3):
        sys.stderr.write('usage: util.py infile [outfile]\n')
    doc = read_xml(sys.argv[1])
    if len(sys.argv) == 3:
        write_xml(sys.argv[2], doc)
