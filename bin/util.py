"""
Utilities used in Software Carpentry tools.
"""

import re
import cStringIO
import xml.etree.ElementTree as ET
import htmlentitydefs

#-------------------------------------------------------------------------------

def read_xml(filename, mangle_entities=False):
    """
    Read in a document, returning the ElementTree doc node.
    """
    try:
        if mangle_entities:
            with open(filename, 'r') as reader:
                data = reader.read()
                data = data.replace('&', '@@@@')
                wrapper = cStringIO.StringIO(data)
                return ET.parse(wrapper)
        else:
            with open(filename, 'r') as reader:
                parser = ET.XMLParser()
                parser.parser.UseForeignDTD(True)
                parser.entity.update(htmlentitydefs.entitydefs)
                return ET.parse(reader, parser=parser)
    except ET.ParseError as e:
        assert False, \
               'Unable to parse %s: %s' % (filename, e)

#-------------------------------------------------------------------------------

def write_xml(filename, doc, unmangle_entities=False):
    """
    Write out a document.
    """
    def _prettify(match):
        entity_num = match.group(1)
        pretty_entity = ORD_TO_ENTITY.get(entity_num)
        return "&" + (pretty_entity or "#" + entity_num) + ";"

    raw = ET.tostring(doc.getroot())
    if unmangle_entities:
        cooked = raw.replace('@@@@', '&')
    else:
        cooked = re.sub(r'&#(.*?);', _prettify, raw).replace('&amp;#', '&')
    with open(filename, 'w') as writer:
        writer.write(cooked)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        doc = read_xml(sys.argv[1])
    if len(sys.argv) == 2:
        write_xml(sys.argv[2], doc)
