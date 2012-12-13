#!/usr/bin/env python

import sys
import png

for filename in sys.argv[1:]:
    try:
        p = png.Reader(filename=filename)
        for chunk_type, chunk_data in p.chunks():
            if chunk_type == 'tEXt':
                who, what = chunk_data.split('\x00')
                if who == 'openbadges':
                    print '%s: %s' % (filename, what)
                    break
    except Exception, e:
        print >> sys.stderr, "error in %s:" % filename, e
