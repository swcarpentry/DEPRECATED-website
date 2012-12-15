"""
Number figures.  Sucks to do this with regular expressions, but trying
to read and write XML with character entities using ElementTree while
preserving comments is just too hard.
"""

import sys
import re

DEF_P = re.compile(r'<figure\s+id="(f:[^"]+)"[^>]*>')
REF_P = re.compile(r'<a\s+href="#(f:[^"]+)">.*?</a>')
FIG_P = re.compile(r'<figure\s+id="(f:[^"]+)"[^>]*>(\s+)<img\s+src="([^"]+)"\s+alt="([^"]+)"\s*/>(\s+)</figure>',
                   re.MULTILINE)
FORMATTED_FIG = '<figure id="%(id)s">%(ws_1)s<img src="%(img)s" alt="%(cap)s" />%(ws_1)s<caption>Figure %(chap_num)d.%(fig_num)d: %(cap)s</caption>%(ws_2)s</figure>'

#-------------------------------------------------------------------------------

def extract_defs(data):
    """
    Extract figure definitions, returning a dict mapping the anchor tag to
    the figure number.
    """
    return dict((m, i+1) for (i, m) in enumerate(DEF_P.findall(data)))

#-------------------------------------------------------------------------------

def update_refs(data, file_num, refs):
    """
    Update references, returning new data.
    """
    def repl(m):
        return '<a class="figref" href="#%s">Figure %d.%d</a>' % \
               (m.group(1), file_num, refs[m.group(1)])

    return REF_P.sub(repl, data)

#-------------------------------------------------------------------------------

def update_figs(data, file_num, refs):
    """
    Update figures, returning new data.
    """
    def repl(m):
        vals = {
            'id'       : m.group(1),
            'ws_1'     : m.group(2),
            'img'      : m.group(3),
            'cap'      : m.group(4),
            'ws_2'     : m.group(5),
            'chap_num' : file_num,
            'fig_num'  : refs[m.group(1)]
        }
        id_stem = vals['id'].split(':')[1]
        file_stem = vals['img'].split('/')[-1].split('.')[0]
        assert id_stem == file_stem, \
               '%s != %s' % (vals['id'], vals['img'])
        return FORMATTED_FIG % vals

    return FIG_P.sub(repl, data)

#-------------------------------------------------------------------------------

def main(filenames):
    for (i, f) in enumerate(filenames):
        file_num = i + 1
        with open(f, 'r') as reader:
            data = reader.read()
        refs = extract_defs(data)
        data = update_refs(data, file_num, refs)
        data = update_figs(data, file_num, refs)
        with open(f, 'w') as writer:
            writer.write(data)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:])
