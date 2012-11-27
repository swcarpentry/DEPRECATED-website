#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
import htmlentitydefs

ENTITIES = htmlentitydefs.entitydefs

for filename in sys.argv[1:]:
    try:
        parser = ET.XMLParser()
        parser.parser.UseForeignDTD(True)
        parser.entity.update(ENTITIES)
        reader = open(filename, 'r')
        tree = ET.parse(reader, parser=parser)
        reader.close()
    except ET.ParseError as e:
        print 'Unable to parse %s: %s' % (filename, e)
    except Exception as e:
        print 'Unable to read %s: %s' % (filename, e)
