#!/usr/bin/env python

"""
Quick and dirty link checker.  Please use a real one for production checks.
"""

import sys
import os
from util import read_xml

#-------------------------------------------------------------------------------

def normalize(root_dir, filename, raw):
    """
    Massage the link, returning normalized and raw links as a pair, or None.
    """

    # Non-local.
    if raw.startswith(('http:', 'https:', 'mailto:', 'ftp:')):
        return None

    # In-file references to anchor.
    norm = raw.split('#')[0]
    if not norm:
        return None

    # Reference to index file in directory.
    if norm.endswith('/'):
        norm = norm + 'index.html'

    # Reference is from web site root.
    if norm.startswith(root_dir):
        pass
    elif norm.startswith('/'):
        norm = root_dir + norm

    # Make absolute.  Cannot use os.path.join because
    # os.path.join('/a/b', '/c/d') is '/c/d'.
    else:
        d = os.path.split(filename)[0]
        norm = os.path.abspath(d + '/' + norm)

    # Hand back the normalized link and the original link.
    return (filename, norm, raw)

#-------------------------------------------------------------------------------

def get_links(root_dir, filenames):
    """
    Extract links from files, return a set of (filename, normalized, raw) links.
    """
    links = set()
    for f in filenames:
        doc = read_xml(f)
        links.update(set(normalize(root_dir, f, r.attrib['href'])
                         for r in doc.findall('.//a[@href]')))
    return set(lnk for lnk in links if lnk)  # filter out None's

#-------------------------------------------------------------------------------

def show_missing(all_files, links):
    """
    Which links are missing?
    """
    for (source, normalized, raw) in links:
        if normalized not in all_files:
            print('{0}: {1} ({2})'.format(source, raw, normalized))

#-------------------------------------------------------------------------------

def main(root_dir):
    """
    Main command-line driver.
    """
    filenames = set(os.path.abspath(f.strip()) for f in sys.stdin)
    links = get_links(root_dir, [f for f in filenames if f.endswith('.html')])
    show_missing(filenames, links)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    assert len(sys.argv) == 2, \
           'Usage: links.py root_dir (filenames in stdin)'
    main(sys.argv[1])
